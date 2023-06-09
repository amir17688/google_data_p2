# Copyright 2012-2016 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, pickle, re
from .. import build
from .. import dependencies
from .. import mesonlib
import json
import subprocess
from ..mesonlib import MesonException

class InstallData():
    def __init__(self, source_dir, build_dir, prefix):
        self.source_dir = source_dir
        self.build_dir= build_dir
        self.prefix = prefix
        self.targets = []
        self.headers = []
        self.man = []
        self.data = []
        self.po_package_name = ''
        self.po = []
        self.install_scripts = []
        self.install_subdirs = []

class TestSerialisation:
    def __init__(self, name, suite, fname, is_cross, exe_wrapper, is_parallel, cmd_args, env,
                 should_fail, valgrind_args, timeout, workdir, extra_paths):
        self.name = name
        self.suite = suite
        self.fname = fname
        self.is_cross = is_cross
        self.exe_runner = exe_wrapper
        self.is_parallel = is_parallel
        self.cmd_args = cmd_args
        self.env = env
        self.should_fail = should_fail
        self.valgrind_args = valgrind_args
        self.timeout = timeout
        self.workdir = workdir
        self.extra_paths = extra_paths

# This class contains the basic functionality that is needed by all backends.
# Feel free to move stuff in and out of it as you see fit.
class Backend():
    def __init__(self, build):
        self.build = build
        self.environment = build.environment
        self.processed_targets = {}
        self.dep_rules = {}
        self.build_to_src = os.path.relpath(self.environment.get_source_dir(),
                                            self.environment.get_build_dir())
        for t in self.build.targets:
            priv_dirname = self.get_target_private_dir_abs(t)
            os.makedirs(priv_dirname, exist_ok=True)

    def get_compiler_for_lang(self, lang):
        for i in self.build.compilers:
            if i.language == lang:
                return i
        raise RuntimeError('No compiler for language ' + lang)

    def get_compiler_for_source(self, src):
        for i in self.build.compilers:
            if i.can_compile(src):
                return i
        if isinstance(src, mesonlib.File):
            src = src.fname
        raise RuntimeError('No specified compiler can handle file ' + src)

    def get_target_filename(self, target):
        targetdir = self.get_target_dir(target)
        fname = target.get_filename()
        if isinstance(fname, list):
            # FIXME FIXME FIXME: build.CustomTarget has multiple output files
            # and get_filename() returns them all
            fname = fname[0]
        filename = os.path.join(targetdir, fname)
        return filename

    def get_target_filename_for_linking(self, target):
        # On some platforms (msvc for instance), the file that is used for
        # dynamic linking is not the same as the dynamic library itself. This
        # file is called an import library, and we want to link against that.
        # On platforms where this distinction is not important, the import
        # library is the same as the dynamic library itself.
        return os.path.join(self.get_target_dir(target), target.get_import_filename())

    def get_target_dir(self, target):
        if self.environment.coredata.get_builtin_option('layout') == 'mirror':
            dirname = target.get_subdir()
        else:
            dirname = 'meson-out'
        return dirname

    def get_target_private_dir(self, target):
        dirname = os.path.join(self.get_target_dir(target), target.get_basename() + target.type_suffix())
        return dirname

    def get_target_private_dir_abs(self, target):
        dirname = os.path.join(self.environment.get_build_dir(), self.get_target_private_dir(target))
        return dirname

    def generate_unity_files(self, target, unity_src):
        langlist = {}
        abs_files = []
        result = []
        for src in unity_src:
            comp = self.get_compiler_for_source(src)
            language = comp.get_language()
            suffix = '.' + comp.get_default_suffix()
            if language not in langlist:
                outfilename = os.path.join(self.get_target_private_dir_abs(target), target.name + '-unity' + suffix)
                outfileabs = os.path.join(self.environment.get_build_dir(), outfilename)
                outfileabs_tmp = outfileabs + '.tmp'
                abs_files.append(outfileabs)
                outfileabs_tmp_dir = os.path.dirname(outfileabs_tmp)
                if not os.path.exists(outfileabs_tmp_dir):
                    os.makedirs(outfileabs_tmp_dir)
                outfile = open(outfileabs_tmp, 'w')
                langlist[language] = outfile
                result.append(outfilename)
            ofile = langlist[language]
            ofile.write('#include<%s>\n' % src)
        [x.close() for x in langlist.values()]
        [mesonlib.replace_if_different(x, x + '.tmp') for x in abs_files]
        return result

    def relpath(self, todir, fromdir):
        return os.path.relpath(os.path.join('dummyprefixdir', todir),\
                               os.path.join('dummyprefixdir', fromdir))

    def flatten_object_list(self, target, proj_dir_to_build_root=''):
        obj_list = []
        for obj in target.get_objects():
            if isinstance(obj, str):
                o = os.path.join(proj_dir_to_build_root,
                                 self.build_to_src, target.get_subdir(), obj)
                obj_list.append(o)
            elif isinstance(obj, build.ExtractedObjects):
                obj_list += self.determine_ext_objs(obj, proj_dir_to_build_root)
            else:
                raise MesonException('Unknown data type in object list.')
        return obj_list

    def serialise_tests(self):
        test_data = os.path.join(self.environment.get_scratch_dir(), 'meson_test_setup.dat')
        datafile = open(test_data, 'wb')
        self.write_test_file(datafile)
        datafile.close()
        benchmark_data = os.path.join(self.environment.get_scratch_dir(), 'meson_benchmark_setup.dat')
        datafile = open(benchmark_data, 'wb')
        self.write_benchmark_file(datafile)
        datafile.close()

    def has_source_suffix(self, target, suffix):
        for s in target.get_sources():
            if s.endswith(suffix):
                return True
        return False

    def has_vala(self, target):
        return self.has_source_suffix(target, '.vala')

    def has_rust(self, target):
        return self.has_source_suffix(target, '.rs')

    def has_cs(self, target):
        return self.has_source_suffix(target, '.cs')

    def has_swift(self, target):
        return self.has_source_suffix(target, '.swift')

    def determine_linker(self, target, src):
        if isinstance(target, build.StaticLibrary):
            return self.build.static_linker
        if len(self.build.compilers) == 1:
            return self.build.compilers[0]
        # Currently a bit naive. C++ must
        # be linked with a C++ compiler, but
        # otherwise we don't care. This will
        # become trickier if and when Fortran
        # and the like become supported.
        cpp = None
        for c in self.build.compilers:
            if c.get_language() == 'cpp':
                cpp = c
                break
        if cpp is not None:
            for s in src:
                if c.can_compile(s):
                    return cpp
        for c in self.build.compilers:
            if c.get_language() == 'vala':
                continue
            for s in src:
                if c.can_compile(s):
                    return c
        raise RuntimeError('Unreachable code')

    def object_filename_from_source(self, target, source):
        return source.fname.replace('/', '_').replace('\\', '_') + '.' + self.environment.get_object_suffix()

    def determine_ext_objs(self, extobj, proj_dir_to_build_root=''):
        result = []
        targetdir = self.get_target_private_dir(extobj.target)
        for osrc in extobj.srclist:
            # If extracting in a subproject, the subproject
            # name gets duplicated in the file name.
            pathsegs = osrc.subdir.split(os.sep)
            if pathsegs[0] == 'subprojects':
                pathsegs = pathsegs[2:]
            fixedpath = os.sep.join(pathsegs)
            objname = os.path.join(proj_dir_to_build_root, targetdir,
                                   self.object_filename_from_source(extobj.target, osrc))
            result.append(objname)
        return result

    def get_pch_include_args(self, compiler, target):
        args = []
        pchpath = self.get_target_private_dir(target)
        includeargs = compiler.get_include_args(pchpath, False)
        for lang in ['c', 'cpp']:
            p = target.get_pch(lang)
            if len(p) == 0:
                continue
            if compiler.can_compile(p[-1]):
                header = p[0]
                args += compiler.get_pch_use_args(pchpath, header)
        if len(args) > 0:
            args = includeargs + args
        return args

    def generate_basic_compiler_args(self, target, compiler):
        commands = []
        commands += compiler.get_always_args()
        commands += compiler.get_warn_args(self.environment.coredata.get_builtin_option('warning_level'))
        commands += compiler.get_option_compile_args(self.environment.coredata.compiler_options)
        commands += self.build.get_global_args(compiler)
        commands += self.environment.coredata.external_args[compiler.get_language()]
        commands += target.get_extra_args(compiler.get_language())
        commands += compiler.get_buildtype_args(self.environment.coredata.get_builtin_option('buildtype'))
        if self.environment.coredata.get_builtin_option('werror'):
            commands += compiler.get_werror_args()
        if isinstance(target, build.SharedLibrary):
            commands += compiler.get_pic_args()
        for dep in target.get_external_deps():
            # Cflags required by external deps might have UNIX-specific flags,
            # so filter them out if needed
            commands += compiler.unix_compile_flags_to_native(dep.get_compile_args())
            if isinstance(target, build.Executable):
                commands += dep.get_exe_args()

        # Fortran requires extra include directives.
        if compiler.language == 'fortran':
            for lt in target.link_targets:
                priv_dir = os.path.join(self.get_target_dir(lt), lt.get_basename() + lt.type_suffix())
                incflag = compiler.get_include_args(priv_dir, False)
                commands += incflag
        return commands

    def build_target_link_arguments(self, compiler, deps):
        args = []
        for d in deps:
            if not isinstance(d, build.StaticLibrary) and\
            not isinstance(d, build.SharedLibrary):
                raise RuntimeError('Tried to link with a non-library target "%s".' % d.get_basename())
            args.append(self.get_target_filename_for_linking(d))
            # If you have executable e that links to shared lib s1 that links to shared library s2
            # you have to specify s2 as well as s1 when linking e even if e does not directly use
            # s2. Gcc handles this case fine but Clang does not for some reason. Thus we need to
            # explictly specify all libraries every time.
            args += self.build_target_link_arguments(compiler, d.get_dependencies())
        return args

    def determine_windows_extra_paths(self, target):
        '''On Windows there is no such thing as an rpath.
        We must determine all locations of DLLs that this exe
        links to and return them so they can be used in unit
        tests.'''
        if not isinstance(target, build.Executable):
            return []
        prospectives = target.get_transitive_link_deps()
        result = []
        for ld in prospectives:
            if ld == '' or ld == '.':
                continue
            dirseg = os.path.join(self.environment.get_build_dir(), self.get_target_dir(ld))
            if dirseg not in result:
                result.append(dirseg)
        return result

    def write_benchmark_file(self, datafile):
        self.write_test_serialisation(self.build.get_benchmarks(), datafile)

    def write_test_file(self, datafile):
        self.write_test_serialisation(self.build.get_tests(), datafile)

    def write_test_serialisation(self, tests, datafile):
        arr = []
        for t in tests:
            exe = t.get_exe()
            if isinstance(exe, dependencies.ExternalProgram):
                fname = exe.fullpath
            else:
                fname = [os.path.join(self.environment.get_build_dir(), self.get_target_filename(t.get_exe()))]
            is_cross = self.environment.is_cross_build() and self.environment.cross_info.need_cross_compiler()
            if is_cross:
                exe_wrapper = self.environment.cross_info.config['binaries'].get('exe_wrapper', None)
            else:
                exe_wrapper = None
            if mesonlib.is_windows():
                extra_paths = self.determine_windows_extra_paths(exe)
            else:
                extra_paths = []
            cmd_args = []
            for a in t.cmd_args:
                if isinstance(a, mesonlib.File):
                    a = os.path.join(self.environment.get_build_dir(), a.rel_to_builddir(self.build_to_src))
                cmd_args.append(a)
            ts = TestSerialisation(t.get_name(), t.suite, fname, is_cross, exe_wrapper,
                                   t.is_parallel, cmd_args, t.env, t.should_fail, t.valgrind_args,
                                   t.timeout, t.workdir, extra_paths)
            arr.append(ts)
        pickle.dump(arr, datafile)


    def generate_depmf_install(self, d):
        if self.build.dep_manifest_name is None:
            return
        ifilename = os.path.join(self.environment.get_build_dir(), 'depmf.json')
        ofilename = os.path.join(self.environment.get_prefix(), self.build.dep_manifest_name)
        mfobj = {'type': 'dependency manifest',
                 'version': '1.0'}
        mfobj['projects'] = self.build.dep_manifest
        open(ifilename, 'w').write(json.dumps(mfobj))
        d.data.append([ifilename, ofilename])

    def get_regen_filelist(self):
        '''List of all files whose alteration means that the build
        definition needs to be regenerated.'''
        deps = [os.path.join(self.build_to_src, df) \
                for df in self.interpreter.get_build_def_files()]
        if self.environment.is_cross_build():
            deps.append(os.path.join(self.build_to_src,
                                     self.environment.coredata.cross_file))
        deps.append('meson-private/coredata.dat')
        if os.path.exists(os.path.join(self.environment.get_source_dir(), 'meson_options.txt')):
            deps.append(os.path.join(self.build_to_src, 'meson_options.txt'))
        for sp in self.build.subprojects.keys():
            fname = os.path.join(self.environment.get_source_dir(), sp, 'meson_options.txt')
            if os.path.isfile(fname):
                deps.append(os.path.join(self.build_to_src, sp, 'meson_options.txt'))
        return deps

    def exe_object_to_cmd_array(self, exe):
        if self.environment.is_cross_build() and \
                isinstance(exe, build.BuildTarget) and exe.is_cross:
            if 'exe_wrapper'  not in self.environment.cross_info:
                s = 'Can not use target %s as a generator because it is cross-built\n'
                s += 'and no exe wrapper is defined. You might want to set it to native instead.'
                s = s % exe.name
                raise MesonException(s)
        if isinstance(exe, build.BuildTarget):
            exe_arr = [os.path.join(self.environment.get_build_dir(), self.get_target_filename(exe))]
        else:
            exe_arr = exe.get_command()
        return exe_arr

    def replace_extra_args(self, args, genlist):
        final_args = []
        for a in args:
            if a == '@EXTRA_ARGS@':
                final_args += genlist.get_extra_args()
            else:
                final_args.append(a)
        return final_args

    def get_custom_target_provided_libraries(self, target):
        libs = []
        for t in target.get_generated_sources():
            if not isinstance(t, build.CustomTarget):
                continue
            for f in t.output:
                if self.environment.is_library(f):
                    libs.append(os.path.join(self.get_target_dir(t), f))
        return libs

    def eval_custom_target_command(self, target, absolute_paths=False):
        if not absolute_paths:
            ofilenames = [os.path.join(self.get_target_dir(target), i) for i in target.output]
        else:
            ofilenames = [os.path.join(self.environment.get_build_dir(), self.get_target_dir(target), i) \
                          for i in target.output]
        srcs = []
        outdir = self.get_target_dir(target)
        # Many external programs fail on empty arguments.
        if outdir == '':
            outdir = '.'
        if absolute_paths:
            outdir = os.path.join(self.environment.get_build_dir(), outdir)
        for i in target.sources:
            if hasattr(i, 'held_object'):
                i = i.held_object
            if isinstance(i, str):
                fname = os.path.join(self.build_to_src, target.subdir, i)
            elif isinstance(i, build.BuildTarget):
                fname = self.get_target_filename(i)
            else:
                fname = i.rel_to_builddir(self.build_to_src)
            if absolute_paths:
                fname = os.path.join(self.environment.get_build_dir(), fname)
            srcs.append(fname)
        cmd = []
        for i in target.command:
            if isinstance(i, build.Executable):
                cmd += self.exe_object_to_cmd_array(i)
                continue
            if isinstance(i, build.CustomTarget):
                # GIR scanner will attempt to execute this binary but
                # it assumes that it is in path, so always give it a full path.
                tmp = i.get_filename()[0]
                i = os.path.join(self.get_target_dir(i), tmp)
            for (j, src) in enumerate(srcs):
                i = i.replace('@INPUT%d@' % j, src)
            for (j, res) in enumerate(ofilenames):
                i = i.replace('@OUTPUT%d@' % j, res)
            if i == '@INPUT@':
                cmd += srcs
            elif i == '@OUTPUT@':
                cmd += ofilenames
            else:
                if '@OUTDIR@' in i:
                    i = i.replace('@OUTDIR@', outdir)
                elif '@PRIVATE_OUTDIR_' in i:
                    match = re.search('@PRIVATE_OUTDIR_(ABS_)?([-a-zA-Z0-9.@:]*)@', i)
                    source = match.group(0)
                    if match.group(1) is None and not absolute_paths:
                        lead_dir = ''
                    else:
                        lead_dir = self.environment.get_build_dir()
                    target_id = match.group(2)
                    i = i.replace(source,
                                  os.path.join(lead_dir,
                                               outdir))
                cmd.append(i)
        cmd = [i.replace('\\', '/') for i in cmd]
        return (srcs, ofilenames, cmd)

    def run_postconf_scripts(self):
        env = {'MESON_SOURCE_ROOT' : self.environment.get_source_dir(),
               'MESON_BUILD_ROOT' : self.environment.get_build_dir()
              }
        child_env = os.environ.copy()
        child_env.update(env)

        for s in self.build.postconf_scripts:
            cmd = s['exe'].get_command() + s['args']
            subprocess.check_call(cmd, env=child_env)

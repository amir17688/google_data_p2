#!/usr/bin/env python

"""
Given a Galaxy tools directory, look for env.sh files and use the directory
structure and the PATH settings to build module files. These env.sh files are
usually created by the Galaxy Toolshed.
Any old module files with a whatis string indicating they were created by this
script will be removed before creating the new files, so that tools deleted from
the Toolshed will be cleaned up.
"""

##
# Clare Sloggett, VLSCI, University of Melbourne
# Authored as part of the Genomics Virtual Laboratory project
##

import re
import os
import argparse
import sys
import logging
from collections import defaultdict

# Initialise logging to print info to screen
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--tools_dir', default='/mnt/galaxy/tools', help='directory in which Galaxy Toolshed tools are installed')
parser.add_argument('--modules_dir', default=None, help='destination directory in which to create module files')
parser.add_argument('--force', action='store_true', help="do not ask for confirmation before deleting old files.")
args = parser.parse_args()

if args.modules_dir is None:
    modules_home = os.environ.get('MODULESHOME')
    if modules_home is None:
        raise Exception("Environment variable $MODULESHOME does not appear to be set; Modules may not be installed. If it is you may need to specify the destination directory manually using --modules_dir.")
    args.modules_dir = os.path.join(modules_home, 'modulefiles')

def get_tool_version(dir_string):
    """
    Strip off tools_dir and take the first two names in the directory hierarchy to
    be the tool name and version. Return (tool, version).
    """
    match = re.match('{0}/(.+)'.format(args.tools_dir), os.path.normpath(dir_string))
    if not match:
        raise Exception("Could not parse env.sh path: " + dir_string + "\n")
    directories = match.group(1).split('/')  #note normpath removes trailing '/'
    if len(directories) < 2:
        raise Exception("Module name does not appear to have a version: " + match.group(1) + "\n")
    tool, version = directories[:2]
    return (tool, version)

# Delete any old module files, i.e. which contain the expected whatis regex
# First build a list and warn the user
delete_list = []
delete_regex = re.compile("^module-whatis\s+Module automatically generated by GVL scripts")
for (dir, subdirs, files) in os.walk(args.modules_dir):
    for file in files:
        filepath = os.path.join(dir,file)
        for line in open(filepath,'rb'):
            if delete_regex.search(line):
                # We matched the regex; delete this file
                delete_list.append(filepath)
                break
if len(delete_list) > 0:
    print "The following old module files will be deleted before creating new ones:"
    print "\n".join(delete_list)
    if not args.force:
        print "Ok? [y/N]"
        if raw_input().lower() != 'y':
            sys.exit()
        logging.info("Deleting old module files")
        for file in delete_list:
            os.remove(file)

# For each tool version, find all relevant env.sh files
tool_shells = defaultdict(list)
for (dir, subdirs, files) in os.walk(args.tools_dir):
    for file in files:
        if file=='env.sh':
            tool, version = get_tool_version(dir)
            tool_shells[(tool, version)].append(dir)

# Parse out paths and add to module files
for ((tool_name, tool_version), dirs) in tool_shells.iteritems():
    module_lines = []
    for dir in dirs:
        env_path = os.path.join(dir, 'env.sh')
        logging.debug("Parsing "+env_path)
        with open(env_path) as f:
            for row in f:
                # if this script is an if-fi block that just sources another env.sh script,
                #  ignore this whole row
                ifmatch = re.match("^if.*\;\s*then\s+\.\s+.*env\.sh\s*\;\s*fi$", row.strip())
                if ifmatch:
                    continue
                # Handle the case where multiple bash rows are on one line
                # This also means we will see and should handle the except statements separately
                for line in row.split(';'):
                    # Look for any environment variable setting, ie ^PATH= ...
                    # Ignore lines which are just export statements
                    # Explicitly complain if we see lines that don't look like this
                    envmatch = re.match("^(\w+)\s*=\s*([^\;=]+)$", line.strip())
                    exportmatch = re.match("^export\s+\$?\w+", line.strip())
                    if envmatch:
                        variable = envmatch.group(1).strip()
                        parts = [x.strip() for x in envmatch.group(2).split(':')]
                        # Drop any empty strings
                        parts = [x for x in parts if x != '']
                        logging.debug("Parsed variable: "+str(variable)+", list "+str(parts))
                        # We have to translate to modulefiles.
                        # Handle four cases:
                        # - the variable does not appear in the list; use setenv
                        # - the variable is at the start of the list; use append-path
                        # - the variable is at the end of the list; use prepend-path
                        # - the variable is in the middle of the list; complain; what silliness is this
                        bashvar = '$'+variable
                        if bashvar not in set(parts):
                            module_lines.append("setenv  {0}  {1}\n".format(variable,
                                                                        ':'.join(parts)))
                        elif bashvar == parts[0]:
                            module_lines.append("append-path  {0}  {1}\n".format(variable,
                                                                        ':'.join(parts[1:])))
                        elif bashvar == parts[-1]:
                            module_lines.append("prepend-path  {0}  {1}\n".format(variable,
                                                                        ':'.join(parts[:-1])))
                        else:
                            logging.warn("Line for environment variable {0} could not be "\
                                    "parsed in {1}".format(variable, env_path))
                    elif exportmatch:
                        # An export statement; ignore
                        pass
                    elif len(line.strip())==0:
                        # An empty line; ignore
                        pass
                    else:
                        # No regex match at all, we don't know what this is
                        logging.warn("Some lines could not be parsed in "+env_path)
                        logging.debug("Unparsed line: "+line.strip())
    module_contents = "#%Module\n"
    module_contents += "# Built automatically from Galaxy env.sh tool setup files\n\n"
    module_contents += "".join(module_lines)
    module_contents += "module-whatis  Module automatically generated by GVL scripts, for tool {0}, version {1}. Paths sourced from Galaxy env.sh tool setup files.\n".format(tool_name, tool_version)

    # Write out the module file
    module_tool_path = os.path.join(args.modules_dir, tool_name)
    if not os.path.exists(module_tool_path):
        os.makedirs(module_tool_path)

    module_full_path = os.path.join(module_tool_path, tool_version)

    logging.info("Writing module to " + module_full_path)

    f = open(module_full_path, 'wb')
    f.write(module_contents)
    f.close()

#TODO it would be nice to grab some extra module-whatis information and inter-module dependencies from the xml files

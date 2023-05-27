#
# This file is autogenerated during plugin quickstart and overwritten during
# plugin makedist. DO NOT CHANGE IT if you plan to use plugin makedist to update 
# the distribution.
#

from setuptools import setup, find_packages

kwargs = {'author': '',
 'author_email': '',
 'classifiers': ['Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering'],
 'description': '',
 'download_url': '',
 'entry_points': '[openmdao.component]\nhyperloop.geometry.air_bearing.AirBearing=hyperloop.geometry.air_bearing:AirBearing\nhyperloop.cycle.heat_exchanger.HeatBalance=hyperloop.cycle.heat_exchanger:HeatBalance\nhyperloop.geometry.battery.Battery=hyperloop.geometry.battery:Battery\nhyperloop.cycle.pump.Pump=hyperloop.cycle.pump:Pump\nhyperloop.aero.Aero=hyperloop.aero:Aero\nhyperloop.test.test_tube_temp.TubeHeatBalance=hyperloop.test.test_tube_temp:TubeHeatBalance\nhyperloop.tube_wall_temp.TubeHeatBalance=hyperloop.tube_wall_temp:TubeHeatBalance\nhyperloop.tube_wall_temp.TubeWallTemp=hyperloop.tube_wall_temp:TubeWallTemp\nhyperloop.mission.Mission=hyperloop.mission:Mission\nhyperloop.hyperloop_sim.HyperloopPod=hyperloop.hyperloop_sim:HyperloopPod\nhyperloop.geometry.inlet.InletGeom=hyperloop.geometry.inlet:InletGeom\nhyperloop.geometry.passenger_capsule.PassengerCapsule=hyperloop.geometry.passenger_capsule:PassengerCapsule\nhyperloop.geometry.pod.Pod=hyperloop.geometry.pod:Pod\nhyperloop.geometry.tube_structure.TubeStructural=hyperloop.geometry.tube_structure:TubeStructural\nhyperloop.cycle.heat_exchanger_sizing.HeatExchangerSizing=hyperloop.cycle.heat_exchanger_sizing:HeatExchangerSizing\nhyperloop.tube_limit_flow.TubeLimitFlow=hyperloop.tube_limit_flow:TubeLimitFlow\nhyperloop.cycle.compression_system.CompressionSystem=hyperloop.cycle.compression_system:CompressionSystem\n\n[openmdao.container]\nhyperloop.geometry.air_bearing.AirBearing=hyperloop.geometry.air_bearing:AirBearing\nhyperloop.cycle.heat_exchanger.HeatBalance=hyperloop.cycle.heat_exchanger:HeatBalance\nhyperloop.geometry.battery.Battery=hyperloop.geometry.battery:Battery\nhyperloop.aero.Aero=hyperloop.aero:Aero\nhyperloop.test.test_tube_temp.TubeHeatBalance=hyperloop.test.test_tube_temp:TubeHeatBalance\nhyperloop.tube_wall_temp.TubeHeatBalance=hyperloop.tube_wall_temp:TubeHeatBalance\nhyperloop.tube_wall_temp.TubeWallTemp=hyperloop.tube_wall_temp:TubeWallTemp\nhyperloop.mission.Mission=hyperloop.mission:Mission\nhyperloop.hyperloop_sim.HyperloopPod=hyperloop.hyperloop_sim:HyperloopPod\nhyperloop.geometry.inlet.InletGeom=hyperloop.geometry.inlet:InletGeom\nhyperloop.geometry.passenger_capsule.PassengerCapsule=hyperloop.geometry.passenger_capsule:PassengerCapsule\nhyperloop.geometry.pod.Pod=hyperloop.geometry.pod:Pod\nhyperloop.geometry.tube_structure.TubeStructural=hyperloop.geometry.tube_structure:TubeStructural\nhyperloop.cycle.heat_exchanger_sizing.HeatExchangerSizing=hyperloop.cycle.heat_exchanger_sizing:HeatExchangerSizing\nhyperloop.cycle.pump.Pump=hyperloop.cycle.pump:Pump\nhyperloop.tube_limit_flow.TubeLimitFlow=hyperloop.tube_limit_flow:TubeLimitFlow\nhyperloop.cycle.compression_system.CompressionSystem=hyperloop.cycle.compression_system:CompressionSystem',
 'include_package_data': True,
 'install_requires': ['openmdao.main', 'openmdao.lib', 'pycycle'],
 'keywords': ['openmdao'],
 'license': '',
 'maintainer': '',
 'maintainer_email': '',
 'name': 'hyperloop',
 'package_data': {'hyperloop': ['sphinx_build/html/modeling.html',
                                'sphinx_build/html/py-modindex.html',
                                'sphinx_build/html/searchindex.js',
                                'sphinx_build/html/genindex.html',
                                'sphinx_build/html/contribute.html',
                                'sphinx_build/html/objects.inv',
                                'sphinx_build/html/baseline.html',
                                'sphinx_build/html/search.html',
                                'sphinx_build/html/usage.html',
                                'sphinx_build/html/srcdocs.html',
                                'sphinx_build/html/future.html',
                                'sphinx_build/html/io.html',
                                'sphinx_build/html/index.html',
                                'sphinx_build/html/pkgdocs.html',
                                'sphinx_build/html/.buildinfo',
                                'sphinx_build/html/_sources/usage.txt',
                                'sphinx_build/html/_sources/pkgdocs.txt',
                                'sphinx_build/html/_sources/baseline.txt',
                                'sphinx_build/html/_sources/srcdocs.txt',
                                'sphinx_build/html/_sources/future.txt',
                                'sphinx_build/html/_sources/contribute.txt',
                                'sphinx_build/html/_sources/index.txt',
                                'sphinx_build/html/_sources/modeling.txt',
                                'sphinx_build/html/_sources/io.txt',
                                'sphinx_build/html/_modules/index.html',
                                'sphinx_build/html/_modules/hyperloop/mission.html',
                                'sphinx_build/html/_modules/hyperloop/aero.html',
                                'sphinx_build/html/_modules/hyperloop/geometry/tube_structure.html',
                                'sphinx_build/html/_modules/hyperloop/geometry/inlet.html',
                                'sphinx_build/html/_modules/hyperloop/geometry/passenger_capsule.html',
                                'sphinx_build/html/_modules/hyperloop/geometry/air_bearing.html',
                                'sphinx_build/html/_modules/hyperloop/geometry/pod.html',
                                'sphinx_build/html/_modules/hyperloop/geometry/battery.html',
                                'sphinx_build/html/_modules/hyperloop/cycle/heat_exchanger_sizing.html',
                                'sphinx_build/html/_modules/hyperloop/cycle/pump.html',
                                'sphinx_build/html/_images/tube_flow_limits.png',
                                'sphinx_build/html/_images/hyperloop.png',
                                'sphinx_build/html/_images/compressor_schematic.png',
                                'sphinx_build/html/_images/compress_assembly_xdsm.png',
                                'sphinx_build/html/_images/heat_effectiveness.png',
                                'sphinx_build/html/_images/pod_assembly_xdsm.png',
                                'sphinx_build/html/_images/velocity_profile.png',
                                'sphinx_build/html/_images/mach_vs_energy.png',
                                'sphinx_build/html/_images/hyperloop_assembly_xdsm.png',
                                'sphinx_build/html/_images/mach_vs_rad.png',
                                'sphinx_build/html/_static/up.png',
                                'sphinx_build/html/_static/ajax-loader.gif',
                                'sphinx_build/html/_static/basic.css',
                                'sphinx_build/html/_static/minus.png',
                                'sphinx_build/html/_static/underscore.js',
                                'sphinx_build/html/_static/jquery.js',
                                'sphinx_build/html/_static/searchtools.js',
                                'sphinx_build/html/_static/file.png',
                                'sphinx_build/html/_static/doctools.js',
                                'sphinx_build/html/_static/down-pressed.png',
                                'sphinx_build/html/_static/default.css',
                                'sphinx_build/html/_static/sidebar.js',
                                'sphinx_build/html/_static/comment-bright.png',
                                'sphinx_build/html/_static/pygments.css',
                                'sphinx_build/html/_static/up-pressed.png',
                                'sphinx_build/html/_static/plus.png',
                                'sphinx_build/html/_static/_static',
                                'sphinx_build/html/_static/down.png',
                                'sphinx_build/html/_static/websupport.js',
                                'sphinx_build/html/_static/comment-close.png',
                                'sphinx_build/html/_static/comment.png',
                                'test/__init__.py',
                                'test/test_tube_temp.py']},
 'package_dir': {'': 'src'},
 'packages': ['hyperloop',
              'hyperloop.geometry',
              'hyperloop.test',
              'hyperloop.cycle'],
 'url': '',
 'version': '0.5',
 'zip_safe': False}


setup(**kwargs)

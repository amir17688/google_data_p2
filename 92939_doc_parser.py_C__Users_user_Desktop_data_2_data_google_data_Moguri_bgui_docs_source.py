import os
import sys
import inspect

API_DOC_HEADER = """
.. Doc page generated by doc_parser.py

.. _api-docs-label:

Auto-Generated API Docs
=======================

.. toctree::
	:maxdepth: 2

"""

AUTODOC_STRING = """
.. automodule:: %s
	
"""

def doc_parser(modules, dst):
	parsed = []

	# Create our api.rst file
	api_rst = open("api.rst", 'w')
	api_rst.write(API_DOC_HEADER)

	# Create api folder
	api_dir = os.path.join(dst, 'api')
	try:
		os.makedirs(api_dir)
	except os.error:
		pass
	
	# Now create rst files for the modules
	for module in modules:
		for i in [getattr(module, i) for i in dir(module) if inspect.ismodule(getattr(module, i))]:
			if not i.__name__.startswith(module.__name__+'.'):
				continue

			if i.__name__ in parsed:
				continue

			parsed.append(i.__name__)

			name = i.__name__.split('.')[1]
			
			api_rst.write('\tapi/'+name+'\n')
			with open(os.path.join(api_dir, name+'.rst'), 'w') as f:
				f.write(name+'\n')
				f.write('='*len(name)+'\n\n')
				f.write(AUTODOC_STRING%i.__name__)				
				
	# Close the api.rst file
	api_rst.close()

from setuptools import setup
from cycli import __version__

setup(name='cycli',
      version=__version__,
      description='A Command Line Interface for Cypher.',
      long_description='Syntax highlighting and autocomplete.',
      keywords='neo4j cypher cli syntax autocomplete',
      url='https://github.com/nicolewhite/cycli',
      author='Nicole White',
      author_email='nicole@neo4j.com',
      license='MIT',
      packages=['cycli'],
      install_requires=[
        'click==4.1',
        'prompt-toolkit==0.57',
        'Pygments==2.0.2',
        'py2neo>=2.0,<3.0',
      ],
      include_package_data=True,
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'cycli = cycli.main:run'
        ]
    })
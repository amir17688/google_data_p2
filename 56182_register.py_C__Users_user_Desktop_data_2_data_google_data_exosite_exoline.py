import pandoc
import os

pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'

doc = pandoc.Document()
doc.markdown = open('README.md').read() + open('HISTORY.md').read()
f = open('README.txt','w+')
f.write(doc.rst)
f.close()
os.system("python setup.py register")
os.remove('README.txt')

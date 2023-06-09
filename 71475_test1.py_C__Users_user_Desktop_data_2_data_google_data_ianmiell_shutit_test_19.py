#Copyright (C) 2014 OpenBet Limited
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from shutit_module import ShutItModule
import thing

class test1(ShutItModule):

	def is_installed(self, shutit):
		return False

	def build(self, shutit):
		thing.thing()
		shutit.send_and_expect('touch /tmp/container_touched',note='touching the container')
		# to test email if desired
		#e = shutit.get_emailer(self.module_id)
		#for line in ['your message line 1', 'your message line 2']:
		#	e.add_line(line)
		#for attach in ['/tmp/container_touched']:
		#		e.attach(attach)
		#e.send()
		shutit.run_script('''
#asd
ls
''')
		return True

def module():
	return test1('shutit.tk.test.test1',1, depends=['shutit.tk.setup'])


#!/home/www/.virtualenvs/income_bot/bin/python

import os
import sys
import pkg_resources

activate_this = str(os.path.dirname(sys.executable)) + '/activate_this.py'
with open(activate_this) as f:
        code = compile(f.read(), activate_this, 'exec')
        exec(code, dict(__file__=activate_this))

import yagmail

print ("Content-type:text/html\r\n\r\n")
print ('<html>')
print ('<head>')
print ('<title>Virtualenv test</title>')
print ('</head>')
print ('<body>')
print ('<h3>If you see this, the module import was successful</h3>')
print ('Python version: ' + sys.version)
print ('<br/>')
print ('Python executable: ' + str(sys.executable))
print ('<br/>')
print ('Installed modules: ')
print ([p.project_name for p in pkg_resources.working_set])
print ('<br/>')
print ('</body>')
print ('</html>')

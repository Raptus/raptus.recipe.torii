# -*- coding: utf-8 -*-
import os, stat
import raptus.torii
import twisted
"""Recipe recipe"""


REQUIRED_IMPORTS = [raptus.torii, twisted]

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.buildout_var = buildout['buildout']
        self.torii_path = os.path.join(self.buildout_var['bin-directory'],options.name)
        self.required_paths = []
        for req in REQUIRED_IMPORTS:
            path = req.__path__[0]
            for i in range(req.__name__.count('.')+1):
                path, tail = os.path.split(path)
            self.required_paths.append(path)
        
        self.instance = []
        for part,opt in buildout.items():
            if opt.has_key('recipe') and opt['recipe'] == 'plone.recipe.zope2instance' and not opt.has_key('zope-conf'):
                self.instance.append(part)

        for part in self.instance:
            self.required_paths.append('%s/lib/python' % buildout[part]['zope2-location'])

        self.vars = dict(python_path = self.buildout_var['executable'],
                    raptus_torii_paths = "',\n'".join(self.required_paths),
                    socket_path = self.options['socket-path'])

        template = template_zope_conf % self.vars
        for part in self.instance:
            if buildout[part].has_key('zope-conf-additional'):
                buildout[part]['zope-conf-additional'] += template
            else:
                buildout[part]['zope-conf-additional'] = template
        if not self.instance:
            print   """
                         Warning: plone.recipe.zope2instace not found.
                         zope.conf is not configured for torii.
                    """
        
        
    def install(self):
        self.update()
        return self.torii_path

    def update(self):
        
        template = template_torii % self.vars
        try:
            fd = open(self.torii_path, 'w+')
            fd.write(template)
        finally:
            fd.close()
            os.chmod(self.torii_path, 0755)
        
            
template_torii = """#!%(python_path)s

import sys
sys.path[0:0] = [
'%(raptus_torii_paths)s']


from raptus.torii.client import Client

PATH ='%(socket_path)s'
Client(PATH).main()
"""


template_zope_conf = """
# configuration for torii server, installed via raptus.recipe.torii

%%import raptus.torii
<torii>
  path %(socket_path)s
</torii>

"""
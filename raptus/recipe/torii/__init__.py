# -*- coding: utf-8 -*-
import os, stat
import raptus.torii

"""Recipe recipe"""

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.buildout_var = buildout['buildout']
        self.torii_path = os.path.join(self.buildout_var['bin-directory'],options.name)

        self.path_egg = raptus.torii.__path__[0]
        index = self.path_egg.rfind(raptus.torii.__name__) + len(raptus.torii.__name__)
        self.path_egg = self.path_egg[:index]
        
        self.vars = dict(python_path = self.buildout_var['executable'],
                    raptus_torii_path = self.path_egg,
                    socket_path = self.options['socket-path'])

        template = template_zope_conf % self.vars
        self.instance = []
        for part,opt in buildout.items():
            if opt.has_key('recipe') and opt['recipe'] == 'plone.recipe.zope2instance' and not opt.has_key('zope-conf'):
                self.instance.append(part)
        for part in self.instance:
            if buildout[part].has_key('zope-conf-additional'):
                buildout[part]['zope-conf-additional'] += template
            else:
                buildout[part]['zope-conf-additional'] = template
        if not self.instance:
            """
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
sys.path.append('%(raptus_torii_path)s')
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
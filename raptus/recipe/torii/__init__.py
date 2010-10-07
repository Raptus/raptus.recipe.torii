# -*- coding: utf-8 -*-
import os
import zc.buildout.easy_install
import zc.recipe.egg


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        
        self.vars = dict(socket_path = self.options['socket-path'],
                         threaded = self.options.get('threaded',False),
                         extends = self.options.get('extends','').strip().replace('\n',';'),
                         params = self.options.get('params','').strip().replace('\n',';'))


        extends = self.options.get('extends','') + '\nraptus.torii'
        options.update({'additional-conf':template_zope_conf % self.vars})
        options.update(eggs=extends)
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)


    def install(self):
        self.update()
        self.requirements, self.working_set = self.egg.working_set()
        runnable = 'Client("%s").main' % self.options['socket-path']
        torii_path = zc.buildout.easy_install.scripts([(self.name,'raptus.torii.client',runnable)],
                                                      self.working_set,
                                                      self.options['executable'],
                                                      self.options['bin-directory'],
                                                      extra_paths = [])
        return torii_path

    def update(self):
        pass



template_zope_conf = """
# configuration for torii server, installed via raptus.recipe.torii

%%import raptus.torii
<torii>
  path %(socket_path)s
  threaded %(threaded)s
  extends %(extends)s
  params %(params)s
</torii>

"""

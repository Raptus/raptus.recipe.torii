Introduction
============
Torii allow the access to a running zope server over a unix-domain-socket. Torii make
also possible to run scripts from the command line to the server. In addition it's provide a python-
prompt connected to the zope-server. It means the full access of the Zope and ZODB at the runtime.


The simplest way to install torii is to use raptus.recipe.torii with a buildout for your
project. This will add the required information in the zope.conf and build a startup
script.

`more information at raptus.torii <http://pypi.python.org/pypi/raptus.torii>`_

Copyright and credits
=====================

raptus.torii is copyright 2010 by raptus_ , and is licensed under the GPL. 
See LICENSE.txt for details.

.. _raptus: http://www.raptus.ch/ 
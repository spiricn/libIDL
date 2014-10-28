#!/usr/bin/env python

from distutils.core import setup

import idl

setup(
      name = 'libIDL',
      
      version = idl.__version__,
      
      description = 'IDL parser tool',
      
      author = 'Nikola Spiric',
      
      author_email = 'nikola.spiric.ns@gmail.com',
      
      package_dir = {'idl' : 'idl'},
      
      packages = ['idl', 'idl.lexer', 'idl.parser'],
)

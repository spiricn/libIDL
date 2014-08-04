#!/usr/bin/env python

from distutils.core import setup

setup(
      name = 'libIDL',
      
      version = '1.0',
      
      description = 'IDL parser tool',
      
      author = 'Nikola Spiric',
      
      author_email = 'nikola.spiric.ns@gmail.com',
      
      package_dir = {'idl' : 'idl'},
      
      packages = ['idl', 'idl.lexer'],
)

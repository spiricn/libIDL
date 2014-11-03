import os
import unittest

from idl.Environment import Environment 
from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError

from test.TestBase import TestBase


class MiscTest(TestBase):
    def test_fileCopmile(self):
        '''
        compileFile method test
        '''
        
        env = Environment()
        
        module = env.compileFile(os.path.join(TestBase.RESOURCE_DIR, "module1.idl"))
        
        iface = module.getInterface('Module1Interface')

        # Interface created        
        self.assertNotEqual(iface, None)
        
        # Method created
        self.assertEqual(len(iface.methods), 1)
        
    def test_forwardCompile(self):
        env = Environment()
        
        sourceFiles = [
            # Compile module 3 first (uses module 2 type)
            os.path.join(TestBase.RESOURCE_DIR, "module3.idl"),
            
            # Compile module 2 second
            os.path.join(TestBase.RESOURCE_DIR, "module2.idl")
        ]
        
        env.compileFiles(sourceFiles)
        
        self.assertNotEqual(env.getModule('module3'), None)
        
        self.assertNotEqual(env.getModule('module2'), None)
        
    def test_errors(self):
        '''
        Test lexer/parser errors.
        '''
        
        # Multiple type definition
        src = '''\
            package com.test;
        
            typedef type;
            typedef type;
        ''' 
        
        try:
            Environment().compileSource(src, 'testModule')
            self.fail()
        except IDLTypeError as e:
            self.assertEqual(e.line, 3)        
            
        # Unrecognized token
        src = '''\
            package com.test;
            
            unrecognized
        ''' 
        
        try:
            Environment().compileSource(src, 'testModule')
            self.fail()
        except IDLSyntaxError as e:
            self.assertEqual(e.line, 2)        
    
if __name__ == '__main__':
    unittest.main()

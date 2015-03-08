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
    
    def test_serialization(self):
        packageName = ['com', 'test']
        
        interfaceName = 'TestInterface'
        
        
        structName = 'TestStruct'
        
        enumName = 'TestEnum'
        
        src = ''' \
        package %s;
        
        
        enum %s{
            a,
            b,
            c
        };
        
        struct %s{
            float32 testField;
        };
        
        interface %s{
            void testMethod();
        }; ''' % ('.'.join(packageName), enumName, structName, interfaceName)
        
        env = Environment()
        
        moduleName = 'testModule'
        
        env.compileSource(src, moduleName)
        
        
        filePath = os.path.join(TestBase.RESOURCE_DIR, '.__MiscTest_SavedEnvironment')
        
        env.save(filePath)
        
        loadedEnv = Environment.load(filePath)
        
        os.remove(filePath)
        
        self.assertEqual(isinstance(loadedEnv, Environment), True)
        
        self.assertEqual(len(loadedEnv.types), 3)

                
        self.assertEqual(loadedEnv.types[0].package.path, packageName)
        
        self.assertEqual(loadedEnv.types[0].name, enumName)
        
        self.assertEqual(loadedEnv.types[1].name, structName)
        
        self.assertEqual(loadedEnv.types[2].name, interfaceName)
        
        
if __name__ == '__main__':
    unittest.main()

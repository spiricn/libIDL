import os
import unittest

from idl.Environment import Environment 
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
        
        self.assertNotEqual(env.getModuleByName('module3'), None)
        
        self.assertNotEqual(env.getModuleByName('module2'), None)
    
if __name__ == '__main__':
    unittest.main()

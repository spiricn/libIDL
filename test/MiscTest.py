import os
import unittest

from idl.Environment import Environment 
from test.TestBase import TestBase


class MiscTest(TestBase):
    def test_fileCopmile(self):
        env = Environment()
        
        module = env.compileFile(os.path.join(TestBase.RESOURCE_DIR, "module1.idl"))
        
        iface = module.getInterface('Module1Interface')

        # Interface created        
        self.assertNotEqual(iface, None)
        
        # Method created
        self.assertEqual(len(iface.methods), 1)
    
if __name__ == '__main__':
    unittest.main()

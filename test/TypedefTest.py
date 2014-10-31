import unittest

from idl.Type import Type

from idl.Environment import Environment 
from test.TestBase import TestBase


class TypedefTest(TestBase):
    def test_typedef(self):
        '''
        Basic typedef test
        '''
        
        src = '''\
        package com.test;
        
        typedef DummyType1;

        typedef DummyType2;
        
        interface TestInterface{
            DummyType2 test(DummyType1 arg);
        };
        
        struct TestStruct{
            DummyType1 field1;
        };
'''

        env = Environment()
        
        module = env.compileSource(src, 'testModule')
        
        self.assertEqual(len(module.package.types), 4)
        
        # Defined ok ?
        self.assertEqual(module.package.types[0].id, Type.TYPEDEF)
        self.assertEqual(module.package.types[0].name, "DummyType1")
        
        # Defined ok?
        self.assertEqual(module.package.types[1].id, Type.TYPEDEF)
        self.assertEqual(module.package.types[1].name, "DummyType2")
        
        iface = module.package.getInterface("TestInterface")
        
        # Typedefs can be return types ?
        self.assertEqual(iface.methods[0].ret.type, Type.TYPEDEF)
        
        # Typedefs can be method args ?
        self.assertEqual(iface.methods[0].args[0].type, Type.TYPEDEF)
    
if __name__ == '__main__':
    unittest.main()

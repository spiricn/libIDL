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
        
        types = env.compileSource(src).types
        
        self.assertEqual(len(types), 4)
        
        # Defined ok ?
        self.assertEqual(types[0].id, Type.TYPEDEF)
        self.assertEqual(types[0].name, "DummyType1")
        
        # Defined ok?
        self.assertEqual(types[1].id, Type.TYPEDEF)
        self.assertEqual(types[1].name, "DummyType2")
        
        iface = env.getInterface("TestInterface")
        
        # Typedefs can be return types ?
        self.assertEqual(iface.methods[0].returnType.id, Type.TYPEDEF)
        
        # Typedefs can be method args ?
        self.assertEqual(iface.methods[0].args[0].type.id, Type.TYPEDEF)
    
if __name__ == '__main__':
    unittest.main()

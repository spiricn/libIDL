from idl.Environment import Environment
from idl.IDLSyntaxError import IDLSyntaxError
from idl.Type import Type
import os
import unittest


RESOURCE_DIR = os.path.abspath('./rsrc')

class EnumTest(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_enum(self):
        '''
        Basic enum test 
        '''
        
        source = '''\
        package com.test;

        enum TestEnum{
            first
            second
            third
            fourth(42)
            fifth(0b11111111)
            sixth(0xC2Ab3)
        }; // </TestEnum>
        
        struct TestStruct{
            int32 field1;
            TestEnum field2;
            string field3;
        }; // </TestStruct>
        
        interface TestInterface{
            TestEnum method1(TestEnum arg1, int32 arg2);
        };
'''
        env = Environment()
        
        module = env.compileSource(source, 'testModule')
        
        self.assertEqual(len(module.types), 3)
        
        enum = module.types[0]
        
        # Test enum
        self.assertEqual(enum.id, Type.ENUM);
        
        self.assertEqual(enum.name, 'TestEnum')
        
        self.assertEqual(len(enum.fields), 6)
        
        self.assertEqual(enum.fields[0].name, "first")
        self.assertEqual(enum.fields[0].value, 0)
        
        self.assertEqual(enum.fields[1].name, "second")
        self.assertEqual(enum.fields[1].value, 1)
        
        self.assertEqual(enum.fields[2].name, "third")
        self.assertEqual(enum.fields[2].value, 2)
        
        self.assertEqual(enum.fields[3].name, "fourth")
        self.assertEqual(enum.fields[3].value, 42)
        
        self.assertEqual(enum.fields[4].name, "fifth")
        self.assertEqual(enum.fields[4].value, 0b11111111)
        
        self.assertEqual(enum.fields[5].name, "sixth")
        self.assertEqual(enum.fields[5].value, 0xC2Ab3)
        
        # Test interface
        iface = module.getInterface("TestInterface")
        self.assertNotEqual(iface, None)
        
        # Can enums be method args ?
        self.assertEqual(iface.methods[0].args[0].type.id, Type.ENUM)
        
        # Can enums be method return types ?
        self.assertEqual(iface.methods[0].ret.type, Type.ENUM)
        
        struct = module.getStructure("TestStruct")
        self.assertNotEqual(struct, None)

        # Can enums be struct fields ?
        self.assertEqual(struct.fields[1].type.id, Type.ENUM)

    def test_errors(self):
        '''
        Enum related error tests.
        '''
        
        # Duplicate field name
        src = '''\
            package com.test;
            
            enum Test{
                a a
            };
        '''
        
        try:
            Environment().compileSource(src, 'testModule')
            self.fail()
        except IDLSyntaxError as e:
            self.assertEqual(e.line, 3)
            
        # Duplicate field value
        src = '''\
            package com.test;
        
            enum Test{
                a(5) 
                b(5)
            };
        '''
        
        try:
            Environment().compileSource(src, 'testModule')
            self.fail()
        except IDLSyntaxError as e:
            self.assertEqual(e.line, 4)
        

if __name__ == '__main__':
    unittest.main()

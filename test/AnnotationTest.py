import os
import unittest

from idl.Environment import Environment 


RESOURCE_DIR = os.path.abspath('./rsrc')

class AnnotationTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_annotations(self):
        '''
        Basic structures test.
        '''
        
        source = '''\
        package com.test;
        
        @Enum
        enum TestEnum{
        @Val
        VAL1
        };
        
        @Struct
        struct TestStruct{
            @Field
            int32 field;
        };
        
        @Interface
        interface TestIface{
        
            @Method
            void method();
        };
        
        @name=value
        typedef dummyType;
        
        @stringValue='stringValue'
        typedef dummyType2;

'''
        env = Environment()
        
        module = env.compileSource(source, 'testModule')
        

        # Enum
        self.assertEqual(module.getType("TestEnum").annotations[0].name, "Enum")

        
        self.assertEqual(module.getType("TestEnum").fields[0].annotations[0].name, "Val")
        
        # Struct
        self.assertEqual(module.getType("TestStruct").annotations[0].name, "Struct")
        
        # Field
        self.assertEqual(module.getType("TestStruct").fields[0].annotations[0].name, "Field")
        
        # Interface
        self.assertEqual(module.getType("TestIface").annotations[0].name, "Interface")
        
        # Method
        self.assertEqual(module.getType("TestIface").methods[0].annotations[0].name, "Method")
        
        # Annotation values
        self.assertEqual(module.getType('dummyType').annotations[0].name, "name")
        
        self.assertEqual(module.getType('dummyType').annotations[0].value, "value")
        
        self.assertEqual(module.getType('dummyType').getAnnotation('name'), module.getType('dummyType').annotations[0])
        
        self.assertEqual(module.getType('dummyType').getAnnotationVal('name'), module.getType('dummyType').annotations[0].value)
        
        self.assertEqual(module.getType('dummyType2').getAnnotationVal('stringValue'), 'stringValue')
        
if __name__ == '__main__':
    unittest.main()

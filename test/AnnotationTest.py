import os
import unittest

from idl.Method import Method
from idl.Environment import Environment 
from idl.Type import Type


RESOURCE_DIR = os.path.abspath('./rsrc')

class AnnotationTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_annotations(self):
        '''
        Basic structures test.
        '''
        
        source = '''\
        
        @Enum
        enum TestEnum{
        @Val
        VAL1,
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

'''
        env = Environment()
        
        env.compile(source)
        
        # Enum
        self.assertEqual(env.getType("TestEnum").annotations[0].text, "Enum")
        
        self.assertEqual(env.getType("TestEnum").fields[0].annotations[0].text, "Val")
        
        # Struct
        self.assertEqual(env.getType("TestStruct").annotations[0].text, "Struct")
        
        # Field
        self.assertEqual(env.getType("TestStruct").fields[0].annotations[0].text, "Field")
        
        # Interface
        self.assertEqual(env.getType("TestIface").annotations[0].text, "Interface")
        
        # Method
        self.assertEqual(env.getType("TestIface").methods[0].annotations[0].text, "Method")
        
        
if __name__ == '__main__':
    unittest.main()

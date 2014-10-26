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
        typedef dummyValue2;

'''
        env = Environment()
        
        env.compileSource(source)
        
        # Enum
        self.assertEqual(env.getType("TestEnum").annotations[0].name, "Enum")

        
        self.assertEqual(env.getType("TestEnum").fields[0].annotations[0].name, "Val")
        
        # Struct
        self.assertEqual(env.getType("TestStruct").annotations[0].name, "Struct")
        
        # Field
        self.assertEqual(env.getType("TestStruct").fields[0].annotations[0].name, "Field")
        
        # Interface
        self.assertEqual(env.getType("TestIface").annotations[0].name, "Interface")
        
        # Method
        self.assertEqual(env.getType("TestIface").methods[0].annotations[0].name, "Method")
        
        # Annotation values
        self.assertEqual(env.getType('dummyType').annotations[0].name, "name")
        
        self.assertEqual(env.getType('dummyType').annotations[0].value, "value")
        
        self.assertEqual(env.getType('dummyType').getAnnotation('name'), env.getType('dummyType').annotations[0])
        
        self.assertEqual(env.getType('dummyType').getAnnotationVal('name'), env.getType('dummyType').annotations[0].value)
        
if __name__ == '__main__':
    unittest.main()

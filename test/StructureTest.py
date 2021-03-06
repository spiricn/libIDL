import unittest

from idl.Environment import Environment 
from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError
from idl.Type import Type

from test.TestBase import TestBase


class StructureTest(TestBase):
    def setUp(self):
        pass
    
    def test_structures(self):
        '''
        Basic structures test.
        '''
        
        source = '''\
package com.test;

// First structure
struct Struct1 {
    int32 f1;
    float64 f2;
};

// Second structure containing the first one
struct Struct2 {
    float32 f3;
    string f4;
    Struct1 f5;
};

interface TestInterface{
    // Method taking structure arguments
    Struct1 testMethod(Struct1 arg1, Struct2 arg2, int32 arg3);
}; // </TestInterface>

'''
        env = Environment()
        
        module = env.compileSource(source, 'testModule')
        
        # Structure number
        structs = module.getTypes(Type.STRUCTURE)
        self.assertEqual(len(structs), 2)
        s1,s2= structs
        f1,f2 = s1.fields, s2.fields
        
        # Verify first structure
        self.assertEqual(s1.name, 'Struct1')
        
        # Field number
        self.assertEqual(len(f1), 2)
        
        # Fields
        self.assertEqual(f1[0].type, Type.INT32)
        self.assertEqual(f1[0].name, 'f1')
        
        self.assertEqual(f1[1].type, Type.FLOAT64)
        self.assertEqual(f1[1].name, 'f2')
        
        
        # Verify second structure
        self.assertEqual(s2.name, 'Struct2')

        # Field number
        self.assertEqual(len(f2), 3)
        
        # Fields
        self.assertEqual(f2[0].type, Type.FLOAT32)
        self.assertEqual(f2[0].name, 'f3')
        
        self.assertEqual(f2[1].type, Type.STRING)
        self.assertEqual(f2[1].name, 'f4')
        
        self.assertEqual(f2[2].type, Type.STRUCTURE)
        self.assertEqual(f2[2].name, 'f5')
        self.assertEqual(f2[2].type.name, 'Struct1')
        
        
        # Verify method
        interface = module.getTypes(Type.INTERFACE)[0]
        
        methods = interface.methods
        self.assertEqual(len(methods), 1)
        
        method = methods[0]

        # Name        
        self.assertEqual(method.name, 'testMethod')

        # Return type
        self.assertEqual(method.ret.type, Type.STRUCTURE)
        self.assertEqual(method.ret.type.name, "Struct1")
                
        # Arguments
        args = method.args
        self.assertEqual(len(args), 3)
        
        self.assertEqual(args[0].type, Type.STRUCTURE)
        self.assertEqual(args[0].type.name, 'Struct1')
        
        
        self.assertEqual(args[1].type, Type.STRUCTURE)
        self.assertEqual(args[1].type.name, 'Struct2')
        
        self.assertEqual(args[2].type, Type.INT32)
        
    def test_arrays(self):
        '''
        Basic arrays in structures test.
        '''
        
        source = '''\
        package com.test;

        struct A{
        };
        
        struct B{
            A[] field;
        };
        '''
        
        env = Environment()
        
        module = env.compileSource(source, 'testModule')
        
        types = module.types
        
        # Array type created
        self.assertEqual(len(types), 2)
        
        # Array field created
        self.assertEqual(types[1].fields[0].type, Type.STRUCTURE)
        
        # Array of structures
        self.assertEqual(types[1].fields[0].type, types[0])

    def test_errors(self):
        '''
        Structure related syntax errors.
        '''
        
        # Duplicate field name test
        src = '''\
            package com.test;
            
            struct Test{
                void dup;
                void dup;
            };
        '''
        
        try:
            Environment().compileSource(src, 'testModule')
            self.fail()
        except IDLSyntaxError as e:
            self.assertEqual(e.line, 4)
            
        # Unresolved field type test
        src = '''\
            package com.test;
            
            struct Test{
                unresolved dup;
            };
        '''
        
        try:
            Environment().compileSource(src, 'testModule')
            self.fail()
        except IDLTypeError as e:
            self.assertEqual(e.line, 3)
            
    def test_dependencies(self):
        '''
        Structure dependency property test.
        '''
        
        src ='''\
        package com.test;
        
        typedef TypeA;
        
        interface TypeB{
        };
        
        struct TypeC{
        };
        
        struct TestStruct{
            TypeA fieldA;
            TypeB fieldB;
            TypeC fieldC;
        };
        '''
        
        module = Environment().compileSource(src, 'module')
        
        deps = module.getType('TestStruct').dependencies
        
        self.assertEqual(len(deps), 3)

if __name__ == '__main__':
    unittest.main()

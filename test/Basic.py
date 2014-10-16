from idl.Module import Module 
from idl.Type import Type
from idl.Project import Project
import unittest
import os

RESOURCE_DIR = './rsrc'

class Basic(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_comments(self):
        '''
        Basic comment stripping test.
        '''
        
        source = '''\
interface = BasicInterface;

/*
test
comment block 2
test
*/

// Comment 1
interface TestInterface{
    void methodName(int32 arg1, uint32 arg2, /* comment block 1 */string arg3);
};
// Comment 2
'''
        module = Module(source)
        
        self.assertEqual(module.params['interface'], 'BasicInterface')
        
        interfaces = module.getTypes(Type.INTERFACE)
        
        self.assertEqual(len(interfaces), 1)
        
        interface = interfaces[0]
        
        self.assertEqual(len(interface.methods), 1)
        
        self.assertEqual(interface.methods[0].name, 'methodName')
     
    def test_basic(self):
        '''
        Basic method creation test.
        '''
         
        source = '''\
interface BasicInterface{
    void methodName(int32 arg1, uint32 arg2, string arg3);
};
'''
         
        module = Module(source)
         
        # Check the interface name
        interface = module.getTypes(Type.INTERFACE)
        self.assertEqual(len(interface), 1)
        
        interface = interface[0]
        
        
        self.assertEqual(interface.name, 'BasicInterface')
         
        # Check the method
        method = interface.methods
        self.assertEqual(len(method), 1)
         
        method = method[0]
         
        # Name
        self.assertEqual(method.name, "methodName")
         
        # Number of arguments
        self.assertEqual(len(method.args), 3)
         
        # Arguments
        arg1, arg2, arg3 = method.args
         
        self.assertEqual(arg1.name, "arg1")
        self.assertEqual(arg2.name, "arg2")
        self.assertEqual(arg3.name, "arg3")
         
        self.assertEqual(arg1.type, Type.INT32)
        self.assertEqual(arg2.type, Type.UINT32)
        self.assertEqual(arg3.type, Type.STRING)
         
        # Return value
        self.assertEqual(method.returnType, Type.VOID)
         
         
    def test_callback(self):
        '''
        Callback declaration/register/unregister methods test.
        '''

        source = '''\
         
interface TestInterface{
    void callbackMethod(int32 arg1) callback;
     
    void callbackRegister(callbackMethod arg1) callback_register;
     
    void callbackUnregister(callbackMethod arg1) callback_unregister;
     
    float32 method(int64 arg1, int32 arg2, float32 arg3, string arg4);
}; // </TestInterace>
'''
 
        module = Module(source)
        
        interface = module.getInterface("TestInterface")
        self.assertTrue( interface != None )
         
        # Check the callback declaration
        calblackDec = interface.getMethod('callbackMethod')
        self.assertTrue( calblackDec != None )
        self.assertTrue(calblackDec.id == Type.CALLBACK)
         
        # Check the callback register
        callbackReg = interface.getMethod('callbackRegister')
        self.assertTrue( callbackReg != None )
        self.assertTrue(callbackReg.id == Type.CALLBACK_REGISTER)
        
        # Check the callback unregister
        callbackUnreg = interface.getMethod('callbackUnregister')
        self.assertTrue(callbackUnreg != None)
        self.assertTrue(callbackUnreg.id == Type.CALLBACK_UNREGISTER)
        
        # Check the method
        method = interface.getMethod('method')
        self.assertTrue(method != None)
         
    def test_params(self):
        '''
        Parameters definition test.
        '''

        source = '''\
interface = ParamInterface;
 
param1 = value1;
 
param2 = value2;
'''

        module = Module(source)
         
        self.assertEqual(len(module.params), 3)
         
        self.assertEqual(module.params['interface'], 'ParamInterface')
         
        self.assertEqual(module.params['param1'], 'value1')
         
        self.assertEqual(module.params['param2'], 'value2')
         
         
    def test_project(self):
        '''
        Basic project management test.
        '''

        project = Project()
         
        # Add first module
        project.addModule('module1', os.path.join(RESOURCE_DIR, 'module1.idl'))
         
        # Add second module
        project.addModule('module2', os.path.join(RESOURCE_DIR, 'module2.idl'))
         
        try:
            # Attempt to add second module again (should fail)
            project.addModule('module2', os.path.join(RESOURCE_DIR, 'module2.idl'))
            self.fail()
        except:
            pass

        # Check number of added modules
        self.assertEqual(len(project.modules), 2)

        # Check the first module
        self.assertTrue('module1' in project.modules)
        interface = project.modules['module1'].getTypes(Type.INTERFACE)[0]
        self.assertEqual(len(interface.methods), 1)
         
        # Check the second module
        self.assertTrue('module2' in project.modules)
        interface = project.modules['module2'].getTypes(Type.INTERFACE)[0]
        self.assertEqual(len(interface.methods), 4)
        
    def test_structures(self):
        '''
        Basic structures test.
        '''
        
        source = '''\
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
        module = Module(source)
        
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
        self.assertEqual(method.returnType, Type.STRUCTURE)
        self.assertEqual(method.returnType.name, "Struct1")
                
        # Arguments
        args = method.args
        self.assertEqual(len(args), 3)
        
        self.assertEqual(args[0].type, Type.STRUCTURE)
        self.assertEqual(args[0].type.name, 'Struct1')
        
        
        self.assertEqual(args[1].type, Type.STRUCTURE)
        self.assertEqual(args[1].type.name, 'Struct2')
        
        self.assertEqual(args[2].type, Type.INT32)


    def test_multiInterface(self):
        '''
        Same method names in different interfaces test. 
        '''
        
        source = '''\
    interface A{
        void method();
    };
    
    
    interface B{
        void method();
    };
    
    interface C {
        void method(A arg1);
    };
'''
        module = Module(source)
        
        i1 = module.getInterface('A')
        self.assertTrue(i1 != None)
        
        i2 = module.getInterface('B')
        self.assertTrue(i2 != None)
        
        self.assertEqual(i1.methods[0].name, i2.methods[0].name)
        
        # Can methods have interfaces as types ?
        self.assertEqual(module.getInterface("C").methods[0].args[0].type.name, "A")
        
    def test_enum(self):
        '''
        Basic enum test 
        '''
        
        source = '''\
        enum TestEnum{
            first,
            second,
            third,
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
        module = Module()
        
        types = module.execute(source)
        
        self.assertEqual(len(types), 3)
        
        enum = types[0]
        
        # Test enum
        self.assertEqual(enum.id, Type.ENUM);
        
        self.assertEqual(enum.name, 'TestEnum')
        
        self.assertEqual(len(enum.fields), 3)
        
        self.assertEqual(enum.fields[0].name, "first")
        self.assertEqual(enum.fields[0].value, 0)
        
        self.assertEqual(enum.fields[1].name, "second")
        self.assertEqual(enum.fields[1].value, 1)
        
        self.assertEqual(enum.fields[2].name, "third")
        self.assertEqual(enum.fields[2].value, 2)
        
        # Test interface
        iface = module.getInterface("TestInterface")
        self.assertNotEqual(iface, None)
        
        # Can enums be method args ?
        self.assertEqual(iface.methods[0].args[0].type.id, Type.ENUM)
        
        # Can enums be method return types ?
        self.assertEqual(iface.methods[0].returnType.id, Type.ENUM)
        
        struct = module.getStructure("TestStruct")
        self.assertNotEqual(struct, None)

        # Can enums be struct fields ?
        self.assertEqual(struct.fields[1].type.id, Type.ENUM)

if __name__ == '__main__':
    unittest.main()

from idl.IDLModule import IDLModule 
from idl.IDLMethod import IDLMethod
from idl.IDLType import IDLType
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
        module = IDLModule(source)
        
        self.assertEqual(module.params['interface'], 'BasicInterface')
        
        interfaces = module.getTypes(IDLType.INTERFACE)
        
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
         
        module = IDLModule(source)
         
        # Check the interface name
        interface = module.getTypes(IDLType.INTERFACE)
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
         
        self.assertEqual(arg1.type, IDLType.INT32)
        self.assertEqual(arg2.type, IDLType.UINT32)
        self.assertEqual(arg3.type, IDLType.STRING)
         
        # Return value
        self.assertEqual(method.returnType, IDLType.VOID)
         
         
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
 
        module = IDLModule(source)
        
        interface = module.getInterface("TestInterface")
        self.assertTrue( interface != None )
         
        # Check the callback declaration
        calblackDec = interface.getMethod('callbackMethod')
        self.assertTrue( calblackDec != None )
        self.assertTrue(calblackDec.type == IDLType.CALLBACK)
         
        # Check the callback register
        callbackReg = interface.getMethod('callbackRegister')
        self.assertTrue( callbackReg != None )
        self.assertTrue(callbackReg.type == IDLType.CALLBACK_REGISTER)
        
        # Check the callback unregister
        callbackUnreg = interface.getMethod('callbackUnregister')
        self.assertTrue(callbackUnreg != None)
        self.assertTrue(callbackUnreg.type == IDLType.CALLBACK_UNREGISTER)
        
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

        module = IDLModule(source)
         
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
        interface = project.modules['module1'].getTypes(IDLType.INTERFACE)[0]
        self.assertEqual(len(interface.methods), 1)
         
        # Check the second module
        self.assertTrue('module2' in project.modules)
        interface = project.modules['module2'].getTypes(IDLType.INTERFACE)[0]
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
    void testMethod(Struct1 arg1, Struct2 arg2, int32 arg3);
}; // </TestInterface>

'''
        module = IDLModule(source)
        
        # Structure number
        structs = module.getTypes(IDLType.STRUCTURE)
        self.assertEqual(len(structs), 2)
        s1,s2= structs
        f1,f2 = s1.fields, s2.fields
        
        # Verify first structure
        self.assertEqual(s1.name, 'Struct1')
        
        # Field number
        self.assertEqual(len(f1), 2)
        
        # Fields
        self.assertEqual(f1[0].type, IDLType.INT32)
        self.assertEqual(f1[0].name, 'f1')
        
        self.assertEqual(f1[1].type, IDLType.FLOAT64)
        self.assertEqual(f1[1].name, 'f2')
        
        
        # Verify second structure
        self.assertEqual(s2.name, 'Struct2')

        # Field number
        self.assertEqual(len(f2), 3)
        
        # Fields
        self.assertEqual(f2[0].type, IDLType.FLOAT32)
        self.assertEqual(f2[0].name, 'f3')
        
        self.assertEqual(f2[1].type, IDLType.STRING)
        self.assertEqual(f2[1].name, 'f4')
        
        self.assertEqual(f2[2].type, IDLType.STRUCTURE)
        self.assertEqual(f2[2].name, 'f5')
        self.assertEqual(f2[2].type.name, 'Struct1')
        
        
        # Verify method
        interface = module.getTypes(IDLType.INTERFACE)[0]
        
        methods = interface.methods
        self.assertEqual(len(methods), 1)
        
        method = methods[0]

        # Name        
        self.assertEqual(method.name, 'testMethod')
        
        # Arguments
        args = method.args
        self.assertEqual(len(args), 3)
        
        self.assertEqual(args[0].type, IDLType.STRUCTURE)
        self.assertEqual(args[0].type.name, 'Struct1')
        
        
        self.assertEqual(args[1].type, IDLType.STRUCTURE)
        self.assertEqual(args[1].type.name, 'Struct2')
        
        self.assertEqual(args[2].type, IDLType.INT32)


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
'''
        module = IDLModule(source)
        
        i1 = module.getInterface('A')
        self.assertTrue(i1 != None)
        
        i2 = module.getInterface('B')
        self.assertTrue(i2 != None)
        
        self.assertEqual(i1.methods[0].name, i2.methods[0].name)
        

if __name__ == '__main__':
    unittest.main()

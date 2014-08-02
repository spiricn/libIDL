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
void methodName(int32 arg1, uint32 arg2, /* comment block 1 */string arg3);
// Comment 2
'''
        module = IDLModule(source)
        
        self.assertEqual(module.params['interface'], 'BasicInterface')
        
        self.assertEqual(len(module.methods), 1)
        
        self.assertEqual(module.methods[0].name, 'methodName')
     
    def test_basic(self):
        '''
        Basic method creation test.
        '''
         
        source = '''\
interface = BasicInterface;
 
void methodName(int32 arg1, uint32 arg2, string arg3);
'''
         
        module = IDLModule(source)
         
        # Check the interface name
        self.assertEqual('BasicInterface', module.params['interface'])
         
        # Check the method
        method = module.getMethods(IDLMethod.TYPE_METHOD)
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
         
interface = InterfaceName;
 
void callbackMethod(int32 arg1) callback;
 
void callbackRegister(callbackMethod arg1) callback_register;
 
void callbackUnregister(callbackMethod arg1) callback_unregister;
 
float32 method(int64 arg1, int32 arg2, float32 arg3, string arg4);
'''
 
        module = IDLModule(source)
         
        # Check the interface name
        self.assertEqual('InterfaceName', module.params['interface'])
         
        # Check the callback declaration
        calblackDec = module.getMethods(IDLMethod.TYPE_CALLBACK_DECLARATION)
        self.assertEqual(len(calblackDec), 1)
         
        # Check the callback register
        callbackReg = module.getMethods(IDLMethod.TYPE_CALLBACK_REGISTER)
        self.assertEqual(len(callbackReg), 1)
        
        callbackReg = callbackReg[0]
        self.assertTrue(callbackReg != None)
        
        self.assertTrue(callbackReg.callbackType.name == 'callbackMethod')
         
        # Check the callback unregister
        callbackUnreg = module.getMethods(IDLMethod.TYPE_CALLBACK_UNREGISTER)
        self.assertEqual(len(callbackUnreg), 1)
        
        callbackUnreg = callbackUnreg[0]
        self.assertTrue(callbackUnreg != None)
        
        self.assertTrue(callbackUnreg.callbackType.name == 'callbackMethod')
         
        # Check the method
        method = module.getMethods(IDLMethod.TYPE_METHOD)
        self.assertEqual(len(method), 1)
         
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
        self.assertEqual(len(project.modules['module1'].methods), 1)
         
        # Check the second module
        self.assertTrue('module2' in project.modules)
        self.assertEqual(len(project.modules['module2'].methods), 4)

if __name__ == '__main__':
    unittest.main()

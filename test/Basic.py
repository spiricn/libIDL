from idl.IDLModule import IDLModule 
from idl.IDLMethod import IDLMethod
from idl.IDLType import IDLType

import unittest

class Basic(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_basic(self):
        '''
        Basci method creation test.
        '''
        
        source = '''\
interface = BasicInterface;

void methodName(int32 arg1, uint32 arg2, string arg3);
'''
        
        module = IDLModule(source)
        
        # Check the interface name
        self.assertEqual('BasicInterface', module.interfaceName)
        
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

void callbackUnregister() callback_unregister;

float32 method(int64 arg1, int32 arg2, float32 arg3, string arg4);
'''

        module = IDLModule(source)
        
        # Check the interface name
        self.assertEqual('InterfaceName', module.interfaceName)
        
        # Check the callback declaration
        calblackDec = module.getMethods(IDLMethod.TYPE_CALLBACK_DECLARATION)
        self.assertEqual(len(calblackDec), 1)
        
        # Check the callback register
        callbackReg = module.getMethods(IDLMethod.TYPE_CALLBACK_REGISTER)
        self.assertEqual(len(callbackReg), 1)
        
        # Check the callback unregister
        callbackUnreg = module.getMethods(IDLMethod.TYPE_CALLBACK_UNREGISTER)
        self.assertEqual(len(callbackUnreg), 1)
        
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

if __name__ == '__main__':
    unittest.main()

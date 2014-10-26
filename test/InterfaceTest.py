import unittest

from idl.Environment import Environment
from idl.Method import Method
from idl.Module import Module 
from idl.Type import Type

from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError
from test.TestBase import TestBase


class InterfaceTest(TestBase):
    def test_comments(self):
        '''
        Basic comment stripping test.
        '''
        
        source = '''\
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
        env = Environment()
        
        env.compileSource(source)
        
        interfaces = env.getTypes(Type.INTERFACE)
        
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
         
        env = Environment()
        
        env.compileSource(source)
         
        # Check the interface name
        interface = env.getTypes(Type.INTERFACE)
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
        
        interface CallbackInterface{
            void onCallback(int32 arg1);
        };
         
        interface TestCallbackInterface{
            void registerCallback(callback_register CallbackInterface arg1);
            
            void unregisterCallback(callback_unregister CallbackInterface arg1);
        };
'''
 
        types = Environment().compileSource(source).types 
        
        self.assertEqual(len(types), 2)
        
        callbackIface, iface = types
        
        # Callback register/unregister methods created
        self.assertEqual(len(iface.methods), 2)
        
        # Register created
        self.assertEqual(iface.methods[0].type, Method.CALLBACK_REGISTER)
        
        # Unregister created
        self.assertEqual(iface.methods[1].type, Method.CALLBACK_UNREGISTER)
        
        # References created
        self.assertEqual(iface.methods[0].callbackType, callbackIface)
        self.assertEqual(iface.methods[1].callbackType, callbackIface)
        
    def test_callbackDeduction(self):
        '''
        Invalid callback type deduction test
        '''
        
        source = '''\
        
        interface Test{
            void brokenRegister(int32 callback) callback_register;
        };
        
        '''
        
        try:
            Module().execute(source)
            self.fail("Invalid callback type detection failed")
            
        except:
            # Failed as expected
            pass
        
    def test_arrays(self):
        '''
        Test array support for method return types or arguments
        '''
        
        source = '''\
        interface TestInterface1{
            void test();
        };
        
        interface TestInterface2{
            int32[45] testMethod(int32[56] arg1, TestInterface1[] arg2);
        };
        '''
        
        env = Environment()
        
        types = env.compileSource(source).types
        
        self.assertEqual(len(types), 2)
        
        iface1 = env.getInterface('TestInterface1')
        
        iface2 = env.getInterface('TestInterface2')
        
        # Array of interfaces
        self.assertEqual(iface2.methods[0].args[1].type, iface1)

        # Array return type
        self.assertTrue(iface2.methods[0].returnType.isArray)

        # Array size test (should probably be moved elswhere)        
        self.assertEqual(iface2.methods[0].returnType.arraySize, 45)
        
        self.assertEqual(iface2.methods[0].args[0].type.arraySize, 56)
        
        
        self.assertEqual(iface2.methods[0].args[1].type.arraySize, -1)

    def test_errors(self):
        '''
        Test interface related syntax errors.
        '''
        
        # Duplicate method name test
        src = '''\
            interface Test{
                void test();
                void test();
            };
        '''
        
        try:
            Environment().compileSource(src)
            self.fail()
        except IDLSyntaxError as e:
            self.assertEqual(e.line, 2)
            
        # Duplicate argument name test
        src = '''\
            interface Test{
                void test(void dup, void dup);
            };
        '''
        
        try:
            Environment().compileSource(src)
            self.fail()
        except IDLSyntaxError as e:
            self.assertEqual(e.line, 1)
            
        # Unresolved return type
        src = '''\
            interface Test{
                unresolved test();
            };
        '''
        
        try:
            Environment().compileSource(src)
            self.fail()
        except IDLTypeError as e:
            self.assertEqual(e.line, 1)
        
        # Unresolved argument type
        src = '''\
            interface Test{
                void test(unresolved arg);
            };
        '''
        
        try:
            Environment().compileSource(src)
            self.fail()
        except IDLTypeError as e:
            self.assertEqual(e.line, 1)
            
        # Duplicate return type modifier
        src = '''\
            interface Test{
                in in void test(unresolved arg);
            };
        '''
        
        try:
            Environment().compileSource(src)
            self.fail()
        except IDLSyntaxError as e:
            self.assertEqual(e.line, 1)
            
        # Duplicate argument modifier
        src = '''\
            interface Test{
                in void test(in in void arg);
            };
        '''
        
        try:
            Environment().compileSource(src)
            self.fail()
        except IDLSyntaxError as e:
            self.assertEqual(e.line, 1)
            
if __name__ == '__main__':
    unittest.main()

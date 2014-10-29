'''
Example demonstrating the usage of callbacks ('callback_register' & 'callback_unregister' method modifiers).
'''
 
from idl.Method import Method

from idl.Environment import Environment


def sampleMain():
    '''
    Sample main function
    '''
    # IDL source code
    inputSource = '''\
    package com.example.callback;

    interface CallbackInterface{
        // Callback method
        void onCallback(int32 arg1);
    };
    
    interface TestInterface{
        // Callback registration method
        void registerCallback(callback_register CallbackInterface arg);

        // Callback unregistration method
        void unregisterCallback(callback_unregister CallbackInterface arg);
        
        int32 dummyMethod(float32 arg);
    };
    
    '''
    # Create an environment
    env = Environment()
    
    # Compile the IDL source as a module
    module = env.compileSource( inputSource, 'CallbackExample' )
    
    # Get the test interface
    iface = module.getInterface('TestInterface')
    
    # Iterate over the methods and print the callback related ones
    for method in iface.methods:
        if method.type == Method.CALLBACK_REGISTER:
            # Found a callback register method
            print('Callback register found (%s): callback interface = %s' % (method.name, method.callbackType.name))
            
        
        elif method.type == Method.CALLBACK_UNREGISTER:
            # Found a callback urnegister method
            print('Callback uregister found (%s): callback interface = %s' % (method.name, method.callbackType.name))

if __name__ == '__main__':
    sampleMain()

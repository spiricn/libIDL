'''
Example demonstrating the usage of callbacks ('callback_register' & 'callback_unregister' method modifiers).
'''
 
from idl.Module import Module 
from idl.Type import Type


def sampleMain():
    '''
    Sample main function
    '''
    # IDL source code
    inputSource = '''\

    interface CallbackInterface{
        // Callback method
        void onCallback(int32 arg1);
    };
    
    interface TestInterface{
        // Callback registration method
        void registerCallback(CallbackInterface arg) callback_register;

        // Callback unregistration method
        void unregisterCallback(CallbackInterface arg) callback_unregister;
        
        int32 dummyMethod(float32 arg);
    };
    
    '''
    
    # Compile the source code into a module
    module = Module( inputSource )
    
    
    # Get the test interface
    iface = module.getInterface('TestInterface')
    
    # Iterate over the methods and print the callback related ones
    for method in iface.methods:
        
        if method == Type.CALLBACK_REGISTER:
            # Found a callback register method
            print('Callback register found (%s): callback interface = %s' % (method.name, method.callbackType.name))
            
        
        elif method == Type.CALLBACK_UNREGISTER:
            # Found a callback urnegister method
            print('Callback uregister found (%s): callback interface = %s' % (method.name, method.callbackType.name))

if __name__ == '__main__':
    sampleMain()
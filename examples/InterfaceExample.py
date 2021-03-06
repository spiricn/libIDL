'''
Example demonstrating the usage of interfaces ('interface' type).
'''
 

from idl.Environment import Environment


def sampleMain():
    '''
    Sample main function
    '''
    
    # IDL source code
    inputSource = '''\
    package com.example.iface;
    
    interface TestInterface {
        void testMethod1(int32 arg1, int32 arg2);
        
        string testMethod2(float32 arg1);
    };
    '''
    
    # Create an environment
    env = Environment()
    
    # Compile the IDL source as a module
    module = env.compileSource( inputSource, 'InterfaceExample' )
    
    # Get the interface object from the module
    interface = module.getInterface('TestInterface')
    
    # Print name
    print('Interface name: %r' % interface.name)
    
    # Print methods
    print('Interface methods:')
    
    for method in interface.methods:
        # Method name
        print('\tName: %r' % method.name)
        
        # Method return type
        print('\tType: %r' % method.ret.type.name)
        
        # Arguments
        for arg in method.args:
            print('\tArg name=%r ; Arg type=%r' % (arg.name, arg.type.name))
            
        print('\n')

if __name__ == '__main__':
    sampleMain()

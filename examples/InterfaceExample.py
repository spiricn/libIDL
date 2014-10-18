'''
Example demonstrating the usage of interfaces ('interface' type).
'''
 
from idl.Module import Module 
from idl.Type import Type


def sampleMain():
    '''
    Sample main function
    '''
    # IDL source code
    inputSource = '''\
    
    interface TestInterface {
        void testMethod1(int32 arg1, int32 arg2);
        
        string testMethod2(float32 arg1);
    };
    '''
    
    # Compile the source code into a module
    module = Module( inputSource )
    
    # Get the interface from the module
    interface = module.getInterface('TestInterface')
    
    # Print the name
    print('Interface name: %r' % interface.name)
    
    # Print the methods
    print('Interface methods:')
    for method in interface.methods:
        # Method name
        print('\tName: %r' % method.name)
        
        # Method return type
        print('\tType: %r' % method.returnType.name)
        
        # Arguments
        for arg in method.args:
            print('\tArg name=%r ; Arg type=%r' % (arg.name, arg.type.name))
            
        print('\n')


if __name__ == '__main__':
    sampleMain()

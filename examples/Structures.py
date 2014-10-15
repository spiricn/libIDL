'''
Basic libIDL example showing basic interface compilation. As a demonstration
the compiled module is used to generate a C++ class.
'''
 
from idl.Module import Module 
from idl.Type import Type

def sampleMain():
    '''
    Sample main function
    '''
    # IDL source code
    inputSource = '''\
    
    // Basic structure with couple of fields
    struct SampleStruct1{
    
        int32 field1;
        
        float32 field2;
        
        string field3;
    };
    
    // Structure using another structure as a field
    struct SampleStruct2{
    
        boolean field1;
        
        SampleStruct1 field2;
        
        SampleStruct1 field3;
    };
    
    
    // Interface using previously defined structure as a method argument
    interface SampleInterface{
    
        SampleStruct1 testMethod( SampleStruct2 arg1 );
        
    };
    
    
    '''
    
    # Compile the source code into a module
    module = Module( inputSource )

        
    # Get the interface method
    method = module.getInterface("SampleInterface").getMethod('testMethod')
    
    # Get the argument ( of type SampleStruct2 )
    arg = method.args[0]
    
    print('Argument name: %s' % arg.name )
    
    print('Argument type: %s' % arg.type.name)
    
    print('Structure fields: ')
    
    # Print its fields
    for c, field in enumerate(arg.type.fields):
        print('\t%d. Type id=%s, name = %s' % (c+1, field.type.id, field.name))
    


if __name__ == '__main__':
    sampleMain()

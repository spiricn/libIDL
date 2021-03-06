'''
Example demonstrating the usage of structures ('struct' type)
'''
 

from idl.Environment import Environment


def sampleMain():
    '''
    Sample main function
    '''
    # IDL source code
    inputSource = '''\
    package com.example.structure;
    
    // Basic structure with couple of fields
    struct SampleStruct{
        int32 field1;
        
        float32 field2;
        
        string field3;
    };
    
    '''
    
    # Create an environment
    env = Environment()
    
    # Compile the IDL source as a module
    module = env.compileSource( inputSource, 'StructExample')
    
    # Get the structure from the module
    struct = module.getStructure('SampleStruct')
    
    # Print its name
    print('Structure name: %r\n' % struct.name)
    
    # Print its fields
    print('Structure fields:')
    for field in struct.fields:
        print('\tField type=%r ; Field name=%r' % (field.type.name, field.name))
    
if __name__ == '__main__':
    sampleMain()

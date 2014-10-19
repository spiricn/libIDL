'''
Example demonstrating the usage of enumerations ('enum' type).
'''
 

from idl.Environment import Environment


def sampleMain():
    '''
    Sample main function
    '''
    # IDL source code
    inputSource = '''\
    
    enum Animals {
        CAT,
        DOG(42),        // explicit (decimal) enum value
        COW(0xAA),    // explicit (hexa-decimal) enum value
        HORSE,
    };
    '''
    
    # Create an environment
    env = Environment()
    
    # Compile the IDL source as a module
    module = env.compile( inputSource )
    
    # Get the enum object from the module
    enum = module.getEnum('Animals')
    
    # Print the enum name
    print('Enum name %r' % enum.name)
    
    # Print the enum fields
    print('Enum fields:')
    
    for field in enum.fields:
        print( '\t %r = %d' % (field.name, field.value) )

if __name__ == '__main__':
    sampleMain()

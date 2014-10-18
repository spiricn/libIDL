'''
Example demonstrating the usage of enumerations ('enum' type).
'''
 
from idl.Module import Module 
from idl.Type import Type


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
    
    # Compile the source code into a module
    module = Module( inputSource )
    
    enum = module.getEnum('Animals')
    
    print('Enum name %r' % enum.name)
    
    print('Enum fields:')
    
    for field in enum.fields:
        print( '\t %r = %d' % (field.name, field.value) )


if __name__ == '__main__':
    sampleMain()

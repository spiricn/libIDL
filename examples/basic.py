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
    
    // Basic interface with a couple of methods
    
    interface SampleInterface{
    
        void method_1(int32 arg1);
    
        int32 method_2(float32 arg1, string arg2, boolean arg3);
        
    };
    
    
    '''
    
    # Compile the source code into a module
    module = Module( inputSource )
    
    # Get the interface object from the module
    interface = module.getInterface("SampleInterface")
    
    # Use it to generate a C++ stub class
    cppSource = generateClass(interface)
    
    print('Generated C++ code: \n')
    
    print(cppSource)


def idlToCppType(idlType):
    '''
    Maps an IDL type ID to C++ type string
    '''
    
    return {
        Type.VOID : 'void',
        Type.BOOL : 'bool',
        Type.FLOAT32 : 'float',
        Type.STRING : 'std::string',
        Type.INT32 : 'int',
    }[ idlType ]
    

def generateClass(interface):
    '''
    Generate a C++ class code from the given interface
    '''
    
    # We'll store the C++ source code here 
    cppSource = ''
    
    # Class name declaration
    cppSource += 'class %s { \n' % interface.name
    cppSource += 'public:\n'

    for method in interface.methods:
        cppSource += '\t'
        
        # Return type
        cppSource += idlToCppType(method.returnType.type)
        
        # Method name
        cppSource += ' %s' % method.name
        
        # Method arguments
        
        cppSource += ' ('
        
        for arg in method.args:
            # Argument type
            cppSource += idlToCppType(arg.type.type)
            
            # Argument name
            cppSource += ' %s, ' % arg.name
            
        
        # Remove the last ", " and add the closing bracket
        cppSource = cppSource[:-2] + '){\n'
        
        # Method body
        cppSource += '\t\t// TODO Method code goes here\n'
        
        cppSource += '\t}\n\n'
        
    cppSource += '};\n'
    
    return cppSource


if __name__ == '__main__':
    sampleMain()

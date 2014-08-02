from idl.Processor import Processor
from idl.FragmentType import FragmentType
from idl.IDLMethod import IDLMethod
from idl.Utils import *

class IDLModule:
    PARAM_INTERFACE_NAME = 'interface'
    
    def __init__(self, source):
        # Create fragments from source
        fragments = Processor.process(source)
        
        self.methods = []
        
        self.params = {}
        
        # Create initial method & parameter objects
        for fragment in fragments:
            if fragment.type == FragmentType.METHOD:
                self.methods.append( IDLMethod(self, fragment ) )
                
        for fragment in fragments:
            if fragment.type == FragmentType.PARAMETER:
                self.__addParam(fragment)
                
        # Process the methods
        self.__processMethods()
        
        # Process the parameters
        self.__processParams()

    def __processMethods(self):
        # Check for duplicate methods
        for method in self.methods:
            for i in self.methods:
                if i != method and i.name == method.name:
                    raise RuntimeError('Duplicate method name detected "%s"' % method.name)

        # Create argument list for each method.
        # This has to be done after the initial method list compile since certain methods
        # may depend on other ones.
        for method in self.methods:
            method.createArgList()
            
    def __processParams(self):
        if IDLModule.PARAM_INTERFACE_NAME not in self.params:
            raise RuntimeError('Malformed IDL module; missing "%s" parameter' % IDLModule.PARAM_INTERFACE_NAME)
        else:
            self.interfaceName = self.params[IDLModule.PARAM_INTERFACE_NAME]
    
    def getMethods(self, methodType):
        return [i for i in self.methods if i.type == methodType]

    def __addParam(self, fragment):
        key, value = fragment.body.split('=')
        
        self.params[key.strip()] = value.split(';')[0].strip()
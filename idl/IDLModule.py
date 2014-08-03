from idl.Processor import Processor
from idl.FragmentType import FragmentType
from idl.IDLMethod import IDLMethod
from idl.IDLType import IDLType
from idl.IDLVariable import IDLVariable
from idl.RawVariable import RawVariable
from idl.IDLStruct import IDLStruct
from idl.Utils import *

class IDLModule:
    PARAM_INTERFACE_NAME = 'interface'
    
    def __init__(self, source):
        # Create fragments from source
        fragments = Processor.process(source)
        
        # Using list instead of dict since ordering is important (think of a better way prehaps?)
        self.types = []
        
        self.params = {}
        
        self.__processFragments(fragments)
                
        # Process the methods
        self.__processMethods()
        
    def __addType(self, type):
        if [i for i in self.types if i.name == type.name]:
            raise RuntimeError('Type named "%s" already defined' % type.name)
        
        self.types.append( type )
        
    def __processFragments(self, fragments):
        while fragments:
            fragment = fragments[0]
            
            if fragment.type == FragmentType.METHOD:
                self.__addType( IDLMethod(self, fragment ) )
                fragments.pop(0)
                
            elif fragment.type == FragmentType.PARAMETER:
                self.__addParam(fragment)
                fragments.pop(0)
            
            elif fragment.type == FragmentType.STRUCT_BEGIN:
                self.__createStruct(fragments)
                
            elif fragment.type == FragmentType.CLOSING_BRACKET:
                raise RuntimeError('Unexpected closing bracket')
                
            else:
                raise RuntimeError('Unhandled fragment type %d', fragment.type)
            
    def createVariable(self, rawArg):
        argType = IDLType(rawArg.type)
            
        # Not a primitive type ?
        if argType == IDLType.INVALID:
            # Is it a callback?
            for method in self.getTypes(IDLType.CALLBACK):
                if method.name == rawArg.type:
                    # It's a callback
                    argType = method
                    break
                
            # Is it a structure ?
            if argType == IDLType.INVALID:
                for struct in self.getTypes(IDLType.STRUCTURE):
                    if struct.name == rawArg.type:
                        # It's a structure
                        argType = struct
                        break
                        
            if argType == IDLType.INVALID:
                # Could not resolve type
                return None

        return IDLVariable(argType, rawArg.name)

    def __createStruct(self, fragments):
        begin = fragments.pop(0)
        
        # Sanity check
        assert(begin.type == FragmentType.STRUCT_BEGIN)

        fields = []
        
        while fragments:
            fragment = fragments.pop(0)
            
            if fragment.type == FragmentType.CLOSING_BRACKET:
                # Reached end
                break
            
            elif fragment.type == FragmentType.STRUCT_FIELD:
                fields.append(fragment)
            
            else:
                raise RuntimeError('Unexpected fragment found whlie parsing structure: "%s"' % fragment.body)
            
        self.__addType( IDLStruct(self, begin, fields) )

    def __processMethods(self):
        # Create argument list for each method.
        # This has to be done after the initial method list compile since certain methods
        # may depend on other ones.
        for type in self.types:
            type.create()
            
    def getTypes(self, type):
        return [i for i in self.types if i.type == type]

    def __addParam(self, fragment):
        key, value = fragment.body.split('=')
        
        self.params[key.strip()] = value.split(';')[0].strip()
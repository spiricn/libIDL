from idl.Processor import Processor
from idl.FragmentType import FragmentType
from idl.IDLMethod import IDLMethod
from idl.IDLType import IDLType
from idl.IDLVariable import IDLVariable
from idl.RawVariable import RawVariable
from idl.IDLStruct import IDLStruct
from idl.Interface import IDLInterface
from idl.Utils import *

# TODO each interface should have it's local methods (at the moment no two interfaces can have the same named method)

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
            
            if fragment.type == FragmentType.PARAMETER:
                self.__addParam(fragment)
                fragments.pop(0)
            
            elif fragment.type == FragmentType.STRUCT_BEGIN:
                self.__createStruct(fragments)
                
            elif fragment.type == FragmentType.INTERFACE_BEGIN:
                self.__createInterface(fragments)
                
            elif fragment.type == FragmentType.CLOSING_BRACKET:
                raise RuntimeError('Unexpected closing bracket')
            
            elif fragment.type == FragmentType.METHOD:
                raise RuntimeError('Method found outside interface body "%s"' % fragment.body)
                
            else:
                raise RuntimeError('Unhandled fragment type %d', fragment.type)
            
    def __createInterface(self, fragments):
        interface = IDLInterface(self, fragments)
        
        self.__addType(interface)
        
    def createVariable(self, context, rawArg):
        argType = IDLType(rawArg.type)
            
        # Not a primitive type ?
        if argType == IDLType.INVALID:
            # If it's not a primitive, it can only be a structure in module's context
            for struct in self.getTypes(IDLType.STRUCTURE):
                if struct.name == rawArg.type:
                    # It's a structure
                    argType = struct
                    break
                
            if isinstance(context, IDLInterface):
                # If it's not a primitive, it can be a callback in interface context
                for method in context.methods:
                    if method.name == rawArg.type:
                        # It's a callback
                        argType = method
                        break
            
            if argType == IDLType.INVALID:
                # Could not resolve type
                return None

        return IDLVariable(argType, rawArg.name)
    
    def getInterface(self, name):
        return self.getType(name, IDLType.INTERFACE)
        
    def getStructure(self, name):
        return self.getType(name, IDLType.STRUCTURE)

    def getType(self, name, typeID):
        for i in self.types:
            if i.name == name and i.type == typeID:
                return i
            
        return None
            
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
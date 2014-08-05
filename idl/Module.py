from idl.lexer.Lexer import Lexer
from idl.lexer.TokenType import TokenType
from idl.Method import Method
from idl.Type import Type
from idl.Variable import Variable
from idl.lexer.VariableToken import VariableToken
from idl.Struct import Struct
from idl.Interface import Interface
from idl.lexer.Utils import *

class Module:
    PARAM_INTERFACE_NAME = 'interface'
    
    def __init__(self, source):
        # Create fragments from source
        fragments = Lexer.tokenize(source)
        
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
            
            if fragment.type == TokenType.PARAMETER:
                self.__addParam(fragment)
                fragments.pop(0)
            
            elif fragment.type == TokenType.STRUCT_BEGIN:
                self.__addType( Struct.generate(self, fragments) )
                
            elif fragment.type == TokenType.INTERFACE_BEGIN:
                self.__createInterface(fragments)
                
            elif fragment.type == TokenType.CLOSING_BRACKET:
                raise RuntimeError('Unexpected closing bracket')
            
            elif fragment.type == TokenType.METHOD:
                raise RuntimeError('Method found outside interface body "%s"' % fragment.body)
                
            else:
                raise RuntimeError('Unhandled fragment type %d', fragment.type)
            
    def __createInterface(self, fragments):
        interface = Interface(self, fragments)
        
        self.__addType(interface)
        
    def createVariable(self, context, rawArg):
        argType = Type(rawArg.type)
            
        # Not a primitive type ?
        if argType == Type.INVALID:
            # If it's not a primitive, it can only be a structure in module's context
            for struct in self.getTypes(Type.STRUCTURE):
                if struct.name == rawArg.type:
                    # It's a structure
                    argType = struct
                    break
                
            if isinstance(context, Interface):
                # If it's not a primitive, it can be a callback in interface context
                for method in context.methods:
                    if method.name == rawArg.type:
                        # It's a callback
                        argType = method
                        break
            
            if argType == Type.INVALID:
                # Could not resolve type
                return None

        return Variable(argType, rawArg.name)
    
    def getInterface(self, name):
        return self.getType(name, Type.INTERFACE)
        
    def getStructure(self, name):
        return self.getType(name, Type.STRUCTURE)

    def getType(self, name, typeID):
        for i in self.types:
            if i.name == name and i.type == typeID:
                return i
            
        return None

    def __processMethods(self):
        # Create argument list for each method.
        # This has to be done after the initial method list compile since certain methods
        # may depend on other ones.
        for i in self.types:
            i.create()
            
    def getTypes(self, type):
        return [i for i in self.types if i.type == type]

    def __addParam(self, fragment):
        key, value = fragment.body.split('=')
        
        self.params[key.strip()] = value.split(';')[0].strip()
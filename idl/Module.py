from idl.lexer.Lexer import Lexer
from idl.lexer.TokenType import TokenType
from idl.Type import Type
from idl.Variable import Variable
from idl.Struct import Struct
from idl.Interface import Interface
from idl.Enum import Enum
from idl.Typedef import Typedef

class Module:
    PARAM_INTERFACE_NAME = 'interface'
    
    def __init__(self, source=None):
        # Using list instead of dict since ordering is important (think of a better way prehaps?)
        self.types = []
        
        self.params = {}
        
        if source:
            self.execute(source)
        
    def execute(self, source):
        # Types created from this source
        self.sourceTypes = []
        
        # Create tokens from source
        tokens = Lexer.tokenize(source)
                
        self.__processTokens(tokens)
                
        # Process the methods
        self.__processTypes()

        return self.sourceTypes
        
    def __addType(self, typeObj):
        '''
        Adds a new type object to the list of types 
        '''
        
        # Type already defined ?
        if [i for i in self.types if i.name == typeObj.name]:
            raise RuntimeError('Type named "%s" already defined' % typeObj.name)
        
        # Store it
        self.types.append( typeObj )
        
        self.sourceTypes.append( typeObj )
        
    def __processTokens(self, tokens):
        '''
        First processing pass.
        Processes tokens generated by the lexer.
        '''
        
        while tokens:
            # Take a token and process it
            token = tokens[0]
            
            # Parameter token
            if token.type == TokenType.PARAMETER:
                # Add a parameter
                self.__addParam(token)
                tokens.pop(0)
            
            # Start of struct definition
            elif token.type == TokenType.STRUCT_BEGIN:
                # Create a struct
                self.__addType( Struct.generate(self, tokens) )

            # Start of interface definition
            elif token.type == TokenType.INTERFACE_BEGIN:
                self.__createInterface(tokens)
                
            # Unexpected (should be handled by either the interface or the struct)
            elif token.type == TokenType.CLOSING_BRACKET:
                raise RuntimeError('Unexpected closing bracket')
            
            # Unexpected (should be handled by the interace)
            elif token.type == TokenType.METHOD:
                raise RuntimeError('Method found outside interface body "%s"' % token.body)
                
            elif token.type == TokenType.ENUM_BEGIN:
                self.__createEnum(tokens)
                
            elif token.type == TokenType.TYPEDEF:
                self.__createTypedef(tokens)
            
            # Unrecognized token
            else:
                raise RuntimeError('Unhandled token type %d', token.type)
            
    def __createTypedef(self, tokens):
        self.__addType( Typedef(tokens) )
            
    def __createEnum(self, tokens):
        self.__addType( Enum(tokens) )
    
    def __createInterface(self, tokens):
        '''
        Creates an interface object from the list of
        tokens and stores it. (consumes tokens)
        '''
        
        interface = Interface(self, tokens)
        
        self.__addType(interface)
        
    def resolveType(self, context, typeName):
        argType = Type(typeName)
            
        # Not a primitive type ?
        if argType == Type.INVALID:
            # If it's not a primitive, it can only be a structure in module's context
            for struct in self.getTypes(Type.STRUCTURE):
                if struct.name == typeName:
                    # It's a structure
                    return struct
                
            for enum in self.getTypes(Type.ENUM):
                if enum.name == typeName:
                    # It's a structure
                    return enum
                
            for iface in self.getTypes(Type.INTERFACE):
                if iface.name == typeName:
                    # It's an interface
                    return iface
                
            if isinstance(context, Interface):
                # If it's not a primitive, it can be a callback in interface context
                for method in context.methods:
                    if method.name == typeName:
                        # It's a callback
                        return method
            
            if argType == Type.INVALID:
                # Could not resolve 
                return None
        else:
            return argType
    
    def createVariable(self, context, rawArg):
        resolvedType = self.resolveType(context, rawArg.type)
        
        if resolvedType:
            return Variable(resolvedType, rawArg.name)
        else:
            return None
            
    
    def getInterface(self, name):
        '''
        Gets the interface object with given name.
        '''
        
        return self.getType(name, Type.INTERFACE)
        
    def getStructure(self, name):
        '''
        Gets structure object with given name.
        '''
        
        return self.getType(name, Type.STRUCTURE)

    def getType(self, name, typeID):
        '''
        Gets object with given type ID and name.
        Helper function used by getXY()
        '''
        
        for i in self.types:
            if i.name == name and i.id == typeID:
                return i
            
        return None

    def __processTypes(self):
        '''
        Second processing pass.
        Preforms per-type creation (e.g. type to object linking etc.) 
        '''
        
        # Create argument list for each method.
        # This has to be done after the initial method list compile since certain methods
        # may depend on other ones.
        for i in self.types:
            i.create()
            
    def getTypes(self, objType):
        '''
        Gets a list of all the objects of specific type
        '''
        
        return [i for i in self.types if i.id == objType]

    def __addParam(self, token):
        '''
        Creates a parameter object type. Consumes tokens.
        '''
        
        key, value = token.body.split('=')
        
        self.params[key.strip()] = value.split(';')[0].strip()
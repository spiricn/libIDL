
import re

from idl.Array import Array
from idl.Enum import Enum
from idl.Interface import Interface
from idl.Struct import Struct
from idl.Type import Type
from idl.Typedef import Typedef
from idl.Variable import Variable
from idl.lexer.Lexer import Lexer
from idl.lexer.TokenType import TokenType
from idl.lexer.Utils import PARAM_NAME_MATCH, NUMBER_MATCH

from idl.Annotation import Annotation


class Module:
    PARAM_INTERFACE_NAME = 'interface'
    
    def __init__(self, source=None):
        # Using list instead of dict since ordering is important (think of a better way prehaps?)
        self.types = []
        
        for i in Type.primitives:
            self.types.append(Type(self, i))
        
        if source:
            self.execute(source)
        
    def execute(self, source):
        # Types created from this source
        self.sourceTypes = []
        
        # Create tokens from source
        tokens = Lexer.tokenize(source)
                
        self.__compile(tokens)
        
        # Process the methods
        self.__link()

        return self.sourceTypes
        
    def __addType(self, typeObj):
        '''
        Adds a new type object to the list of types 
        '''
        
        # TODO two types may have the same name (e.g. methods and interfaces) so this check should probably be revised
        
        # Type already defined ?
#         if [i for i in self.types if i.name == typeObj.name]:
#             raise RuntimeError('Type named "%s" already defined' % typeObj.name)
        
        # Store it
        self.types.append( typeObj )
        
        self.sourceTypes.append( typeObj )
    
    def __compile(self, tokens):
        '''
        First processing pass.
        Processes tokens generated by the lexer.
        '''
        
        tokenProcessors = {
            TokenType.STRUCT_BEGIN : Struct,
            TokenType.INTERFACE_BEGIN : Interface,
            TokenType.ENUM_BEGIN : Enum,
            TokenType.TYPEDEF : Typedef,
        }
        
        annotations = []
        
        while tokens:
            # Take a token and process it
            token = tokens[0]
            
            if token.type == TokenType.ANNOTATION:
                annotations.append( Annotation(tokens) )
                continue
            
            if token.type in tokenProcessors:
                typeObj = tokenProcessors[token.type](self, tokens )
                
                typeObj.annotations += annotations
                
                annotations = []
                
                self.__addType( typeObj )
            else:
                raise RuntimeError("Unexpected token type %d" % token.type)
        
    def __findTypesByName(self, name):
        '''
        Find all types with the given name.
        '''
        
        return [i for i in self.types if i.name == name]
    
    def resolveType(self, typeName):
        '''
        Resovles a type name to a type object
        '''
        
        # Is it an array ?
        if typeName.endswith(']'):
            # Resolve its base type first
            baseTypeName = re.compile(PARAM_NAME_MATCH).search(typeName).group(0)
            
            baseType = self.resolveType( baseTypeName )
            
            # Optional size
            try:            
                sizeStr = re.compile('(\[' + NUMBER_MATCH + '\])').search(typeName).group(0)[1:-1]
            except:
                raise RuntimeError("Invalid array size %r" % typeName)
            
            size = -1
            
            if sizeStr:
                size = int(sizeStr)

            if not baseType:
                # Could not resolve base type
                return None
            
            # Create an array type with this base
            return  Array(self, baseType, size)
            
        types = self.__findTypesByName(typeName)
        
        if not types:
            return None
        
        if len(types) != 1:
            # Should this even be allowed to happen ?
            raise RuntimeError("TODO: Not implemented")
        
        return types[0]
    
    def createVariable(self, rawArg):
        resolvedType = self.resolveType(rawArg.type)
        
        if resolvedType:
            return Variable(resolvedType, rawArg.name)
        else:
            return None
            
    
    def getEnum(self, name):
        '''
        Gets the enum object with given name.
        '''
        
        return self.getType(name, Type.ENUM)
    
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

    def getType(self, name, typeID=-1):
        '''
        Gets object with given type ID and name.
        Helper function used by getXY()
        '''
        
        for i in self.types:
            if i.name == name and (typeID == -1 or i.id == typeID):
                return i
            
        return None

    def __link(self):
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


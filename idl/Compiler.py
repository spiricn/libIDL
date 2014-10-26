from idl.Enum import Enum
from idl.Interface import Interface
from idl.Struct import Struct
from idl.Typedef import Typedef
from idl.lexer import Lang
from idl.lexer.Token import Token
from idl.lexer.Tokenizer import Tokenizer

from idl.IDLSyntaxError import IDLSyntaxError
from idl.lexer.LexerError import LexerError
from idl.parser.EnumParser import EnumParser
from idl.parser.InterfaceParser import InterfaceParser
from idl.parser.Parser import Parser
from idl.parser.ParserError import ParserError
from idl.parser.StructParser import StructParser
from idl.parser.TypedefParser import TypedefParser


class TypeInfo:
    '''
    Helper class used by the compiler.
    '''
    
    def __init__(self, typeClass, parserClass, startTokenID, startTokenBody):
        self.typeClass = typeClass
        self.parserClass = parserClass
        self.startTokenID = startTokenID
        self.startTokenName = startTokenBody

class Compiler:
    def __init__(self, module):
        self._module = module
    
        self._types = []
        
    def compile(self, source):
        '''
        Compile given source and add types to the module and the associated environment.
        '''
        
        types = [
            TypeInfo(Interface, InterfaceParser, Token.KEYWORD, Lang.KEYWORD_INTERFACE),
            TypeInfo(Enum, EnumParser, Token.KEYWORD, Lang.KEYWORD_ENUM),
            TypeInfo(Struct, StructParser, Token.KEYWORD, Lang.KEYWORD_STRUCT),
            TypeInfo(Typedef, TypedefParser, Token.KEYWORD, Lang.KEYWORD_TYPEDEF),
        ]

        # Tokenize the source
        try:
            tokens = Tokenizer.tokenize(source)
        except LexerError as e:
            # Re-reaise the lexer exception as public IDLSyntaxError
            raise IDLSyntaxError(self._module, e.token.location[0], e.token.locationStr)
        
        # Parser used for generating type annotations
        parser = Parser(tokens)
        
        while tokens:
            foundParser = False
            
            # Consume all annotations before type declaration
            parser.eatAnnotations()
            
            for i in types:
                if i.startTokenID == parser.next.id and i.startTokenName == parser.next.body:
                    # Instantiate a parser class and create type info
                    try:
                        info = i.parserClass(tokens).parse()
                    except ParserError as e:
                        # Re-reaise the parser exception as public IDLSyntaxError
                        raise IDLSyntaxError(self._module, e.token.location[0], e.token.locationStr)
                    
                    # Instantiate associated type object
                    typeObj = i.typeClass(self._module, info)
                    
                    # Assign previously accumulated annotations to the newly created type
                    typeObj._assignAnnotations( parser.getAnnotations() )  
                    
                    foundParser = True
                    
                    # Add type global environment types
                    self._module.env._addType( typeObj )
                    
                    # Add type to our types (used later for linking)
                    self._types.append( typeObj )
                    
                    # Add type to module types
                    self._module.types.append( typeObj )
                    
                    break
                
            if not foundParser:
                # Found an unexpected token (no parsers found)
                raise RuntimeError('Unrecognized token while parsing types %r (%d)' % (parser.next.body, parser.next.id))

    def link(self):
        # Just iterate over all the types we created and link them
        for typeObj in self._types:
            typeObj._link()

    
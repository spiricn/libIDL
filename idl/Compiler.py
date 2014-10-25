from idl.Annotation import Annotation
from idl.Enum import Enum
from idl.Interface import Interface
from idl.Struct import Struct
from idl.Typedef import Typedef
from idl.lexer.Token import Token

from idl.lexer.Keywords import KEYWORD_INTERFACE, KEYWORD_ENUM, KEYWORD_STRUCT, \
    KEYWORD_TYPEDEF
from idl.lexer.Tokenizer import Tokenizer
from idl.parser.EnumParser import EnumParser
from idl.parser.InterfaceParser import InterfaceParser
from idl.parser.Parser import Parser
from idl.parser.StructParser import StructParser
from idl.parser.TypedefParser import TypedefParser


class TypeInfo:
    def __init__(self, typeClass, parserClass, startTokenID, startTokenBody):
        self.typeClass = typeClass
        self.parserClass = parserClass
        self.startTokenID = startTokenID
        self.startTokenName = startTokenBody
        

class Compiler:
    def __init__(self, module):
        self.module = module
    
        self.types = []
        
    def compile(self, source):
        types = [
            TypeInfo(Interface, InterfaceParser, Token.KEYWORD, KEYWORD_INTERFACE),
            TypeInfo(Enum, EnumParser, Token.KEYWORD, KEYWORD_ENUM),
            TypeInfo(Struct, StructParser, Token.KEYWORD, KEYWORD_STRUCT),
            TypeInfo(Typedef, TypedefParser, Token.KEYWORD, KEYWORD_TYPEDEF),
        ]

        tokens = Tokenizer.tokenize(source)
        
        parser = Parser(tokens)
        
        while tokens:
            foundParser = False
            
            parser.eatAnnotations()
            
            token = tokens[0]
            
            for i in types:
                if i.startTokenID == token.id and i.startTokenName == token.body:
                    info = i.parserClass(tokens).parse()
                    
                    typeObj = i.typeClass(self.module, info)
                    
                    typeObj._assignAnnotations( parser.getAnnotations() )  
                    
                    foundParser = True
                    
                    self.module.env._addType( typeObj )
                    
                    self.types.append( typeObj )
                    
                    self.module.types.append( typeObj )
                    
                    break
                
            if not foundParser:
                raise RuntimeError('Unrecognized token while parsing types %s(%d)' % (token.body, token.id))

    def link(self):
        for typeObj in self.types:
            typeObj._link()

    
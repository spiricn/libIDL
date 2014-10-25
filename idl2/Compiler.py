from idl2.Enum import Enum
from idl2.Interface import Interface
from idl2.lexer.Keywords import KEYWORD_INTERFACE, KEYWORD_ENUM
from idl2.lexer.Token import Token
from idl2.lexer.Tokenizer import Tokenizer
from idl2.parser.EnumParser import EnumParser
from idl2.parser.InterfaceParser import InterfaceParser


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
#             TypeInfo(Interface, StructParser, Token.KEYWORD, KEYWORD_STRUCT),
#             TypeInfo(Interface, TypedefParser, Token.KEYWORD, KEYWORD_TYPEDEF),
        ]

        tokens = Tokenizer.tokenize(source)
        
        while tokens:
            token = tokens[0]
            
            foundParser = False
            
            for i in types:
                if i.startTokenID == token.id and i.startTokenName == token.body:
                    info = i.parserClass(tokens).parse()
                    
                    typeObj = i.typeClass(self.module, info)  
                    
                    foundParser = True
                    
                    self.module.env._addType( typeObj )
                    
                    self.types.append( typeObj )
                    
                    break
                
            if not foundParser:
                raise RuntimeError('Did not find parser')

    def link(self):
        for typeObj in self.types:
            typeObj._link()

    
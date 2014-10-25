import re

from idl2.lexer.Keywords import KEYWORD_INTERFACE, KEYWORD_ENUM, KEYWORD_STRUCT, \
    KEYWORD_TYPEDEF
from idl2.lexer.Token import Token
from idl2.lexer.Tokenizer import Tokenizer
from idl2.parser.EnumParser import EnumParser
from idl2.parser.InterfaceParser import InterfaceParser
from idl2.parser.StructParser import StructParser
from idl2.parser.TypedefParser import TypedefParser


source = '''

interface Test{
    void test(int asdf, int ar);
};


enum asdf{
one( 234 )
two tree

};

struct TestStruct {
    int field1;
};

typedef Surface;

'''

class Interface:
    def __init__(self, info):
        self.info = info
        
class Enum:
    def __init__(self, info):
        self.info = info

class TypeInfo:
    def __init__(self, typeClass, parserClass, startTokenID, startTokenBody):
        self.typeClass = typeClass
        self.parserClass = parserClass
        self.startTokenID = startTokenID
        self.startTokenName = startTokenBody
        

class Compiler:
    def __init__(self):
        pass
    
    def compile(self, source):
        types = [
            TypeInfo(Interface, InterfaceParser, Token.KEYWORD, KEYWORD_INTERFACE),
            TypeInfo(Interface, EnumParser, Token.KEYWORD, KEYWORD_ENUM),
            TypeInfo(Interface, StructParser, Token.KEYWORD, KEYWORD_STRUCT),
            TypeInfo(Interface, TypedefParser, Token.KEYWORD, KEYWORD_TYPEDEF),
        ]

        tokens = Tokenizer.tokenize(source)
        
        while tokens:
            token = tokens[0]
            
            foundParser = False
            
            for i in types:
                if i.startTokenID == token.id and i.startTokenName == token.body:
                    info = i.parserClass(tokens).parse()
                    
                    typeObj = i.typeClass(info)  
                    
                    foundParser = True
                    
                    break
                
            if not foundParser:
                raise RuntimeError('Did not find parser')
            
c = Compiler()

c.compile(source)


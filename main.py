import re

from idl.lexer2.Keywords import KEYWORD_INTERFACE, KEYWORD_ENUM, KEYWORD_STRUCT
from idl.lexer2.Token import Token
from idl.lexer2.Tokenizer import Tokenizer
from idl.parser.EnumParser import EnumParser
from idl.parser.InterfaceParser import InterfaceParser
from idl.parser.StructParser import StructParser


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
        
        
types = [
    TypeInfo(Interface, InterfaceParser, Token.KEYWORD, KEYWORD_INTERFACE),
    TypeInfo(Interface, EnumParser, Token.KEYWORD, KEYWORD_ENUM),
    TypeInfo(Interface, StructParser, Token.KEYWORD, KEYWORD_STRUCT),         
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

import re

from idl2.Compiler import Compiler
from idl2.Environment import Environment
from idl2.Interface import Interface
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
    void test(boolean asdf, void asdf);
};


'''

'''

enum asdf{
one( 234 )
two tree

};

struct TestStruct {
    int field1;
};

typedef Surface;
'''

        
class Enum:
    def __init__(self, info):
        self.info = info


env = Environment()
            

env.compileModule('module', source)

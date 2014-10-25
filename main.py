import re

from idl.lexer2.InterfaceParser import InterfaceParser
from idl.lexer2.Keywords import KEYWORD_INTERFACE
from idl.lexer2.Parser import Parser
from idl.lexer2.Token import Token
from idl.lexer2.Tokenizer import Tokenizer


source = '''

interface Test{
    void test(int asdf);
};

'''
tokens = Tokenizer.tokenize(source)

InterfaceParser(tokens).parse() 

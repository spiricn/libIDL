from idl.lexer.Token import Token

from idl.parser.Parser import Parser
from idl.parser.ParserError import ParserError


class MethodInfo:
    class ArgInfo:
        def __init__(self, varInfo, line):
            self.varInfo = varInfo
            self.line = line
        
    def __init__(self, line):
        self.args = []
        self.name = ''
        self.line = line
        self.returnTypeInfo = Parser.TypeInfo()

class MethodParser(Parser):
    class Test:
        def __init__(self):
            pass
        
    def __init__(self, tokens):
        Parser.__init__(self, tokens)
        
    def parse(self):
        self.method = MethodInfo(self.next.location[0])
        
        # Parse return type / name
        self._parseHead()
        
        # Parse parameter list
        self._parseArgs()
        
        # Tail
        self.eat(Token.PUNCTUATION , ';')
        
        return self.method
        

    def _parseHead(self):
        # Return type
        self.method.returnTypeInfo = self.eatTypeInfo()
        
        # Method name
        self.method.name = self.eat(Token.ID).body
        
    def _parseArgs(self):
        # List start
        self.eat(Token.PUNCTUATION, '(')
        
        expectingArg = True
         
        while True:
            token = self.next
            
            if token.id == Token.PUNCTUATION and token.body == ')':
                # End of param list
                self.pop()
                
                break
            
            elif expectingArg:
                argLine = self.next.location[0]
                
                # Argument type
                varInfo = self.eatVariableInfo()
                
                # Create info
                self.method.args.append( MethodInfo.ArgInfo(varInfo, argLine) )
                
                expectingArg = False
                
            elif not expectingArg and token.id == Token.PUNCTUATION and token.body == ',':
                expectingArg = True
                self.pop()
                
            else:
                raise ParserError('Unexpected token while parsing method', token)

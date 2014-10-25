from idl2.lexer.Token import Token
from idl2.parser.Parser import Parser


class MethodInfo:
    class ArgInfo:
        def __init__(self, argTypeName, argName):
            self.typeName = argTypeName
            self.name = argName
        
    def __init__(self):
        self.args = []
        self.name = ''
        self.returnTypeName = ''

class MethodParser(Parser):
    class Test:
        def __init__(self):
            pass
        
    def __init__(self, tokens):
        Parser.__init__(self, tokens)
        
        self.method = MethodInfo()
        
    def parse(self):
        # Parse return type / name
        self._parseHead()
        
        # Parse parameter list
        self._parseArgs()
        
        # Tail
        self.eat(Token.PUNCTUATION , ';')
        
        return self.method
        

    def _parseHead(self):
        # Return type
        self.method.returnTypeName = self.eat(Token.ID).body
        
        # Method name
        self.method.name = self.eat(Token.ID).body
        
    def _parseArgs(self):
        # List start
        self.eat(Token.PUNCTUATION, '(')
        
        expectingArg = True
         
        while True:
            token = self.pop()
            
            if token.id == Token.PUNCTUATION and token.body == ')':
                # End of param list
                break
            
            elif expectingArg and token.id == Token.ID:
                # Argument type
                argType = token.body
                
                # Argument name
                argName = self.eat(Token.ID).body
                
                # Create info
                self.method.args.append( MethodInfo.ArgInfo(argType, argName) )
                
                expectingArg = False
                
            elif not expectingArg and token.id == Token.PUNCTUATION and token.body == ',':
                expectingArg = True
                
            else:
                raise RuntimeError('Invalid token while parsing argument list %d' % token.id)

from idl.lexer2.Parser import Parser
from idl.lexer2.Token import Token

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
        self.assertNext(Token.PUNCTUATION , ';')
        self.pop()
        
        return self.method
        

    def _parseHead(self):
        # Return type
        self.assertNext(Token.ID)
        
        self.method.returnType = self.pop().body
        
        # Method name
        self.assertNext(Token.ID)
        
        self.method.name = self.pop().body
        
    def _parseArgs(self):
        # List start
        self.assertNext(Token.PUNCTUATION, '(')
        self.pop()
        
        while True:
            token = self.pop()
            
            if token.id == Token.PUNCTUATION and token.body == ')':
                # End of param list
                break
            
            elif token.id == Token.ID:
                # Argument type
                argType = token.body
                
                # Argument name
                self.assertNext(Token.ID)
                argName = self.pop().body
                
                # Create info
                self.method.args.append( MethodInfo.ArgInfo(argType, argName) )
                
            else:
                raise RuntimeError('Invalid token while parsing argument list %d' % token.id)
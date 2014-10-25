from idl2.lexer.Token import Token


class Parser(object):
    class TypeInfo:
        def __init__(self, name='', arraySize=None):
            self.name = name
            self.arraySize = arraySize
             
    def __init__(self, tokens):
        self.tokens = tokens
        
    def assertNext(self, typeId, body=None):
        if len(self.tokens) == 0:
            raise RuntimeError('Token missing (expecting %d)' % typeId)
        
        else:
            # Type check
            if self.next().id != typeId:
                raise RuntimeError('Invalid token while parsing; expected %d got %d' % (typeId, self.next().id))
            
            # Body check
            if body != None and body != self.next().body:
                raise RuntimeError('Invalid token while parsing; expected %r got %r' % (body, self.next().body))
            
    def eat(self, typeId, body=None):
        self.assertNext(typeId, body)
        
        return self.pop()
        
    def pop(self):
        return self.tokens.pop(0)
    
    def next(self):
        return self.tokens[0]
    
    def getArraySize(self):
        if self.next().id == Token.PUNCTUATION and self.next().body == '[':
            self.eat(Token.PUNCTUATION)
            
            size = -1
            
            # Evaluate array size if given
            if self.next().id == Token.LIT:
                size = eval(self.pop().body)
                
            self.eat(Token.PUNCTUATION, ']')
            
            return size
        
        else:
            return None
        
    def getTypeInfo(self):
        return Parser.TypeInfo(self.eat(Token.ID).body, self.getArraySize())
    
    def _debug(self, numTokens=1):
        print([str(self.tokens[index]) for index in range(numTokens)])
        
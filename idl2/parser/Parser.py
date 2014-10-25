from idl2.lexer.Token import Token


class Parser(object):
    class TypeInfo:
        def __init__(self, name='', arraySize=None):
            self.name = name
            self.arraySize = arraySize
            
    class AnnotationInfo:
        def __init__(self, name='', value=''):
            self.name = name
            self.value = value
             
    def __init__(self, tokens):
        self.tokens = tokens
        self.annotations = []
        
    def assertNext(self, typeId, body=None):
        if len(self.tokens) == 0:
            raise RuntimeError('Token missing (expecting %d)' % typeId)
        
        else:
            # Type check
            if self.next().id != typeId:
                raise RuntimeError('Invalid token while parsing; expected %s(%d) got %s(%d)' % (str(body), typeId, self.next().body, self.next().id))
            
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
    
    def eatArraySize(self):
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
        
    def getAnnotations(self):
        res = self.annotations
        
        self.annotations = []
        
        return res
    
    def eatAnnotations(self):
        while True:
            annotation = self._eatAnnotation()
            
            if annotation:
                self.annotations.append( annotation  )
            else:
                break

    def _eatAnnotation(self):
        if self.next().id == Token.PUNCTUATION and self.next().body == '@':
            self.pop()
            
            name = self.eat(Token.ID).body
            
            if self.next().id == Token.PUNCTUATION and self.next().body == '=':
                self.pop()
                
                if self.next().id in [Token.ID, Token.LIT]:
                    value = self.pop().body
                
            else:
                value= ''

            return Parser.AnnotationInfo(name, value)
            
        else:
            return None
        
    def eatTypeInfo(self):
        return Parser.TypeInfo(self.eat(Token.ID).body, self.eatArraySize())
    
    def _debug(self, numTokens=1):
        print([str(self.tokens[index]) for index in range(numTokens)])
        
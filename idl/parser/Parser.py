from idl.Trace import Trace
from idl.lexer import Lang
from idl.lexer.Lang import KEYWORD_IMPORT, KEYWORD_PACKAGE
from idl.lexer.Token import Token
from idl.parser.Desc import PackageDesc, ImportDesc, ImportsDesc, VariableDesc, \
    TypeDesc, AnnotationDesc
from idl.parser.ParserError import ParserError


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.annotations = []
        self._prevToken = None
        
    def assertNext(self, typeId, body=None):
        if len(self.tokens) == 0:
            raise ParserError('Missing token', self._prevToken)
    
        # Type check
        if self.next.id != typeId:
            raise ParserError('Unexpected token while parsing', self.next)
        
        # Body check
        if body != None and body != self.next.body:
            raise ParserError('Unexpected token while parsing', self.next)
            
    def eat(self, typeId, body=None):
        self.assertNext(typeId, body)
        
        return self.pop()
        
    def pop(self):
        self._prevToken = self.tokens.pop(0) 
        return self._prevToken
    
    @property
    def next(self):
        if not self.tokens:
            raise ParserError('No tokens left', self._prevToken)
        
        return self.tokens[0]
    
    def eatArraySize(self):
        if self.next.id == Token.PUNCTUATION and self.next.body == '[':
            self.eat(Token.PUNCTUATION)
            
            size = -1
            
            # Evaluate array size if given
            if self.next.id == Token.INT_LIT:
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
            comment = self._eatComment()
            
            if comment:
                self.annotations.append( comment )
                
            annotation = self._eatAnnotation()
            
            if annotation:
                self.annotations.append( annotation  )
            else:
                break
            
    def _eatComment(self):
        if not len(self.tokens):
            return None
        
        if self.next.id == Token.BLOCK_COMMENT:
            return AnnotationDesc(value=self.pop().body, isComment=True)
        
        else:
            return None

    def _eatAnnotation(self):
        if not len(self.tokens):
            return None

        if self.next.id == Token.PUNCTUATION and self.next.body == '@':
            self.pop()
            
            if self.next.id in [Token.ID, Token.STRING_LIT]:
                name = self.pop().body 
            else:
                raise ParserError('Unexpected token while parsing annotation', self.next)
            
            if self.next.id == Token.PUNCTUATION and self.next.body == '=':
                self.pop()
                
                if self.next.id in [Token.ID, Token.INT_LIT, Token.STRING_LIT]:
                    value = self.next.body
                    
                    if self.next.id == Token.STRING_LIT:
                        # Strip the quotations marks
                        value = value[1:-1]
                        
                    self.pop()
                        
                else:
                    raise ParserError('Unexpected token while parsing annotation', self.next)
                
            else:
                value= ''

            return AnnotationDesc(name, value)
            
        else:
            return None
        
    def eatVariableDesc(self):
        # Eat variable type
        typeDesc = self.eatTypeDesc()
        
        # Variable name
        name = self.eat(Token.ID).body
        
        return VariableDesc(name, typeDesc)

    def eatTypePath(self):
        path = []
        
        while True:
            if self.isNext(Token.ID):
                path.append( self.pop().body )
                
                if self.isNext(Token.PUNCTUATION, '.'):
                    self.pop()
                else:
                    break
                 
            else:   
                break
        
        return path
    
    def eatTypeDesc(self):
        keywords = []
            
        # Eat all keywords preceeding the type  
        while True:
            if self.next.id == Token.KEYWORD:
                keywords.append( self.pop() )

            else:
                break
            
        # Type name
        path = self.eatTypePath()
        
        # Is it an array ?
        arraySize = None
        
        if self.next.id == Token.PUNCTUATION and self.next.body == '[':
            arraySize = self.eatArraySize()
                
            if arraySize == None:
                raise ParserError('Unexpected token while parsing type desc', self.next)
            
        # Check keywords
        validKeywords = [
            Lang.KEYWORD_IN,
            Lang.KEYWORD_OUT,
            Lang.KEYWORD_CALLBACK_REG,
            Lang.KEYWORD_CALLBACK_UNREG,
        ]
        
        for keyword in keywords:
            if keyword.body not in validKeywords:
                raise ParserError('Unexpected keyword while parsing type', keyword)
            
            
        return TypeDesc(path, [i.body for i in keywords], arraySize)
    
    def isNext(self, tokenId, body=None):
        if self.tokens:
            if self.next.id == tokenId:
                if body != None:
                    return self.next.body == body
                else:
                    return True
                
        return False
    
    def _eatImportPathDesc(self):
        path = []
        
        while True:
            path.append( self.eat(Token.ID).body )
            
            if self.isNext(Token.PUNCTUATION, '.'):
                self.pop()
                
            elif self.isNext(Token.PUNCTUATION, ';'):
                break
            
            else:
                raise ParserError('Unexpected token while parsing package declaration', self.next)

        return path            
        
    def eatPackageDesc(self):
        if self.tokens and ( self.next.id == Token.KEYWORD and self.next.body == KEYWORD_PACKAGE ):
            # Eat package keyword
            self.pop()

            # Eat the package we're declaring
            package = self._eatImportPathDesc()
            
            # Eat semicolon
            self.eat(Token.PUNCTUATION, ';')
            
            return PackageDesc(package)
        
        else:
            return None
        
    def eatImportsDesc(self):
        desc = ImportsDesc()
        
        while True:
            if self.tokens and ( self.next.id == Token.KEYWORD and self.next.body == KEYWORD_IMPORT ):
                line = self.next.location[0]
                
                # Eat import keyword
                self.pop()
                
                # Eat the package we're importing
                package = self._eatImportPathDesc()
                
                desc.imports.append( ImportDesc(package, line) )
                
                # Eat semicolon
                self.eat(Token.PUNCTUATION, ';')

            else:
                break
            
        return desc
    
    def _debug(self, numTokens=1):
        Trace.debug([str(self.tokens[index]) for index in range(numTokens)])
        

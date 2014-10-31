from idl.lexer import Lang
from idl.lexer.Lang import KEYWORD_PACKAGE, KEYWORD_IMPORT
from idl.lexer.Token import Token
from idl.parser.ParserError import ParserError


class Parser(object):
    class TypeInfo:
        def __init__(self, typeName='', mods=[], arraySize=None):
            self.typeName = typeName
            self.arraySize = arraySize
            self.mods = mods
            
    class VariableInfo:
        def __init__(self, typeInfo, name):
            self.typeInfo = typeInfo
            self.name = name
            
    class AnnotationInfo:
        def __init__(self, name='', value=''):
            self.name = name
            self.value = value
            
    class PackageInfo:
        def __init__(self, package):
            self.package = package
            
    class ImportsInfo:
        def __init__(self, imports):
            self.imports = imports
             
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
            annotation = self._eatAnnotation()
            
            if annotation:
                self.annotations.append( annotation  )
            else:
                break

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

            return Parser.AnnotationInfo(name, value)
            
        else:
            return None
        
    def eatVariableInfo(self):
        # Eat variable type
        typeInfo = self.eatTypeInfo()
        
        # Variable name
        name = self.eat(Token.ID).body
        
        return Parser.VariableInfo(typeInfo, name)
    
    def eatTypeInfo(self):
        keywords = []
            
        # Eat all keywords preceeding the type  
        while True:
            if self.next.id == Token.KEYWORD:
                keywords.append( self.pop() )

            else:
                break
            
        # Type name
        name = self.eat(Token.ID).body
        
        # Is it an array ?
        arraySize = None
        
        if self.next.id == Token.PUNCTUATION and self.next.body == '[':
            arraySize = self.eatArraySize()
                
            if arraySize == None:
                raise ParserError('Unexpected token while parsing type info', self.next)
            
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
            
            
        return Parser.TypeInfo(name, [i.body for i in keywords], arraySize)
    
    def _eatImportPathInfo(self):
        importInfo = []
        
        while True:
            # Eat package component
            importInfo.append( self.eat(Token.ID).body )
            
            if self.next.id == Token.PUNCTUATION:
                if self.next.body == '.':
                    self.pop()
                    
                elif self.next.body == ';':
                    break
                
                else:
                    raise ParserError('Unexpected token while parsing package declaration', self.next)
                
            else:
                raise ParserError('Unexpected token while parsing package declaration', self.next)
            
        return importInfo
        
    def eatPackageInfo(self):
        if self.tokens and ( self.next.id == Token.KEYWORD and self.next.body == KEYWORD_PACKAGE ):
            # Eat package keyword
            self.pop()

            # Eat the package we're declaring
            package = self._eatImportPathInfo()
            
            # Eat semicolon
            self.eat(Token.PUNCTUATION, ';')
            
            return Parser.PackageInfo(package)
        
        else:
            return None
        
    def eatImportsInfo(self):
        imports = []
        
        while True:
            if self.tokens and ( self.next.id == Token.KEYWORD and self.next.body == KEYWORD_IMPORT ):
                # Eat import keyword
                self.pop()
                
                # Eat the package we're importing
                package = self._eatImportPathInfo()
                
                imports.append(package)
                
                # Eat semicolon
                self.eat(Token.PUNCTUATION, ';')

            else:
                break
            
        return Parser.ImportsInfo(imports)
    
    def _debug(self, numTokens=1):
        print([str(self.tokens[index]) for index in range(numTokens)])
        

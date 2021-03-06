from idl.Enum import Enum
from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError
from idl.Interface import Interface
from idl.Struct import Struct
from idl.Typedef import Typedef
from idl.lexer import Lang
from idl.lexer.LexerError import LexerError
from idl.lexer.Token import Token
from idl.lexer.Tokenizer import Tokenizer
from idl.parser.EnumParser import EnumParser
from idl.parser.InterfaceParser import InterfaceParser
from idl.parser.Parser import Parser
from idl.parser.ParserError import ParserError
from idl.parser.StructParser import StructParser
from idl.parser.TypedefParser import TypedefParser

from idl.Preprocessor import Preprocessor


class Compiler:
    class _ParserInfo:
        '''
        Private helper class used by the compiler.
        '''
        
        def __init__(self, typeClass, parserClass, startTokenID, startTokenBody):
            self.typeClass = typeClass
            self.parserClass = parserClass
            self.startTokenID = startTokenID
            self.startTokenName = startTokenBody
            
    PARSERS = [
            # Interface
            _ParserInfo(Interface, InterfaceParser, Token.KEYWORD, Lang.KEYWORD_INTERFACE),
            
            # Enum
            _ParserInfo(Enum, EnumParser, Token.KEYWORD, Lang.KEYWORD_ENUM),
            
            # Struct
            _ParserInfo(Struct, StructParser, Token.KEYWORD, Lang.KEYWORD_STRUCT),
            
            # Typedef
            _ParserInfo(Typedef, TypedefParser, Token.KEYWORD, Lang.KEYWORD_TYPEDEF),
    ]
    
    def __init__(self, env, module):
        self._module = module
        
        self._env = env
    
        self._types = []
        
    def compile(self, source):
        '''
        Compile given source and add types to the module and the associated environment.
        '''
        
        # Tokenize the source
        try:
            tokens = Tokenizer.tokenize(source)
        except LexerError as e:
            # Re-reaise the lexer exception as public IDLSyntaxError
            raise IDLSyntaxError(self._module, e.token.location[0], e.token.locationStr)
        
        # Preprocess
        tokens = Preprocessor.process(self._env, tokens)
        
        # Parser used for generating type annotations & package desc
        self._tokenParser = Parser(tokens)
        
        self._tokenParser.eatAnnotations()
        
        # Parse package
        try:
            PackageDesc = self._tokenParser.eatPackageDesc()
        except ParserError as e:
            raise IDLSyntaxError(self._module, e.token.location[0], e.token.locationStr)

        if not PackageDesc:
            raise IDLSyntaxError(self._module, self._tokenParser.next.location[0] if self._tokenParser.tokens else 0, 'Missing package declaration in module')
        
        # Create or acquire package
        package = self._env._createChildTree(PackageDesc.package)
        
        # Imports
        imports = self._tokenParser.eatImportsDesc()
        
        self._module._setImportsDesc( imports )
        
        # Add the module
        package._addModule(self._module)

        # While there are tokens to compile ..
        while tokens:
            # Consume all annotations before type declaration
            try:
                self._tokenParser.eatAnnotations()
            except ParserError as e:
                # Re-reaise the lexer exception as public IDLSyntaxError
                raise IDLSyntaxError(self._module, e.token.location[0], e.token.locationStr)
            
            # Find a suitable parser for the next token
            typeParser = self._findParser()
            
            if not typeParser:
                # No parser found (probably an unexpected token error)
                raise IDLSyntaxError(self._module, self._tokenParser.next.location[0], self._tokenParser.next.locationStr)
            
            # Save the starting token (we will need it if a type error ocurrs later)
            startToken = self._tokenParser.next
                    
            # Instantiate a parser class and create type desc (consumes tokens)
            try:
                desc = typeParser.parserClass(tokens).parse()
            except ParserError as e:
                # Re-reaise the parser exception as public IDLSyntaxError
                raise IDLSyntaxError(self._module, e.token.location[0], e.token.locationStr)
            
            # Instantiate associated type object
            typeObj = typeParser.typeClass(self._module, desc)
            
            # Assign previously accumulated annotations to the newly created type
            typeObj._assignAnnotations( self._tokenParser.getAnnotations() )  
            
            # Add type global environment types
            try:
                self._module._addType( typeObj )
            except IDLTypeError as e:
                # Re-raise it with added line
                raise IDLTypeError(self._module, startToken.location[0], e.message)
            
            # Add type to our types (used later for linking)
            self._types.append( typeObj )
            
    def link(self):
        '''
        Links type created by self.compile
        '''
        
        # Just iterate over all the types we created and link them
        for typeObj in self._types:
            typeObj._link()
            
    def _findParser(self):
        '''
        Finds a suitable parser for the next token in the queue.
        '''
        
        for parser in Compiler.PARSERS:
            if parser.startTokenID == self._tokenParser.next.id and parser.startTokenName == self._tokenParser.next.body:
                return parser
            
        return None

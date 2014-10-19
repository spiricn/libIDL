from idl.lexer.TokenType import TokenType

class Annotation(object):
    def __init__(self, tokens):
        # Sanity check
        assert(tokens[0].type == TokenType.ANNOTATION)
        
        header = tokens.pop(0)
        
        self.name = header.name
        
        self.value = header.value

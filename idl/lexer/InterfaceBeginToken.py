from idl.lexer.Token import Token

class InterfaceBeginToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

    def __str__(self):
        return '<InterfaceBeginToken>'

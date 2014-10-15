from idl.lexer.Token import Token

class EnumFieldToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

    def __str__(self):
        return '<EnumFieldToken body="%s">' % self.body

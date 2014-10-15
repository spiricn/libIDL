from idl.lexer.Token import Token

class EnumBeginToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

    def __str__(self):
        return '<EnumBeginToken body="%s">' % self.body

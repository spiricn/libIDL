from idl.lexer.Token import Token


class StructBeginToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

    def __str__(self):
        return '<StructBeginToken body="%s">' % self.body

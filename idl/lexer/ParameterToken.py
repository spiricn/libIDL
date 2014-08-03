from idl.lexer.Token import Token

class ParameterToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

    def __str__(self):
        return '<ParameterToken body="%s">' % self.body

from idl.lexer.Token import Token


class AnnotationToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

        text = body.strip().split('@')[1]
        
        if '=' in text:
            self.name, self.value = text.split('=')
        else:
            self.name = text
            self.value = None

    def __str__(self):
        return '<EnumFieldToken body="%s">' % self.body

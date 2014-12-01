class Preprocessor:
    def __init__(self, tokens):
        self._tokens = tokens
        
    @staticmethod
    def process(tokens):
        return Preprocessor(tokens)._process()
    
    def _process(self):
        return self._tokens

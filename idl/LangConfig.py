

class LangConfig:
    def __init__(self, inheritance=True, operatorOverload=True, preprocessor=True):
        self._inheritance = inheritance
        self._operatorOverload = operatorOverload
        self._preprocessor = preprocessor
    
    @property
    def preprocessor(self):
        return self._preprocessor

    @property
    def operatorOverload(self):
        return self._operatorOverload
    
    @property
    def inheritance(self):
        return self._inheritance

    
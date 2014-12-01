

class LangConfig:
    def __init__(self, inheritance=True, operatorOverload=True):
        self._inheritance = inheritance
        self._operatorOverload = operatorOverload
    
    @property
    def operatorOverload(self):
        return self._operatorOverload
    
    @property
    def inheritance(self):
        return self._inheritance

    
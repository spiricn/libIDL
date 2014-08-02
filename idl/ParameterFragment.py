from idl.Fragment import Fragment

class ParameterFragment(object):
    def __init__(self, fragmentType, body):
        Fragment.__init__(self, fragmentType, body)

    def __str__(self):
        return '<ParameterFragment>'

# A string of any length, starting with a letter may contain lower or upper case letters including numbers
PARAM_NAME_MATCH = r'([a-zA-Z]+[a-zA-Z0-9_]*)'

# May be a string containing any letter except ';'
PARAM_VALUE_MATCH = r'([^;]+)'

# Matches zero or more consecutive tabs and/or spaces
WHITESPACE_MATCH = r'[ \t]*'

# Matches one or more consecutive tabs and/or spaces
WHITESPACE_SPLIT_MATCH = r'[ \t]+'

# Matches single number
NUMBER_MATCH = r'([0-9]*)'

WHITESPACE_LINE_MATCH = r'^' + WHITESPACE_MATCH + r'$'

def dprint(obj):
    string = str(obj)
    
    string = string.replace('\n', '\\n').replace('\t', '\\t')
    
    print('"%s"' % string)
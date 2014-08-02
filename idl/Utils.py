# A string of any length, starting with a letter may contain lower or upper case letters including numbers
PARAM_NAME_MATCH = '([a-zA-Z]+[a-zA-Z0-9_]*)'

# May be a string containing any letter except ';'
PARAM_VALUE_MATCH = '([^;]+)'

# Matches zero or more consecutive tabs and/or spaces
WHITESPACE_MATCH = '[ \t]*'

# Matches one or more consecutive tabs and/or spaces
WHITESPACE_SPLIT_MATCH = '[ \t]+'

WHITESPACE_LINE_MATCH = '^' + WHITESPACE_MATCH + '$'

def dprint(object):
    string = str(object)
    
    string = string.replace('\n', '\\n').replace('\t', '\\t')
    
    print('"%s"' % string)
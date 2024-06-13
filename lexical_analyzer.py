import ply.lex as lex

reserved = {

    #Angel Tomalá
    'def' : 'DEF',
    'return': 'RETURN',
    'class' : 'CLASS',
    'if' : 'IF',
    'elsif' : 'ELSIF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE'

    

}


tokens = (

    #Angel Tomalá
    'LOCAL_VAR',
    'INSTANCE_VAR',
    'CLASS_VAR',
    'GLOBAL_VAR',
    'CONSTANT',
    'INTEGER',
    'FLOAT',
    'BIN_INTEGER',
    'OCT_INTEGER',
    'HEX_INTEGER',
    'STRING',
    'BOOLEAN',
    'NIL',
    'SYMBOL'


) + tuple(reserved.values())


#Angel Tomalá

t_INSTANCE_VAR = r'@[a-z_A-Z]\w*'
t_CLASS_VAR = r'@{2}[a-z_A-Z]\w*'
t_GLOBAL_VAR = r'\$[a-z_A-Z]\w*'
t_CONSTANT = r'[A-Z]\w*'
t_STRING = r'"[^"]*"'
t_BOOLEAN = r'\b(true|false)\b'
t_SYMBOL = r':[a-zA-Z_]\w*'


def t_LOCAL_VAR(t):
    r'[_a-z]\w*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'([1-9]\d*|0)\.\d+'
    t.value = float(t.value)
    return t

def t_BIN_INTEGER(t):
    r'0b[01]+'
    t.value = int(t.value, 2)
    return t

def t_OCTAL_INTEGER(t):
    r'0[0-7]+'
    t.value = int(t.value, 8)
    return t

def t_HEX_INTEGER(t):
    r'0x[0-9a-fA-F]+'
    t.value = int(t.value, 16)
    return t

def t_NIL(t):
    r'\bnil\b'
    t.value = None
    return t

def t_error(t):
    print(f"Token no admitido '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

def t_newLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'  # Ignora espacios y tabulaciones

algoritmoAngel = '''
@instance_var
@@class_var
$global_var
CONSTANT
123
def my_function(param1, param2):
    if param1 > param2:
        return true
    elsif param1 < param2:
        return false
    else:
        return nil
'''

#AGREGAR LOS TOKENS ":" "(" ")" ","

lexer = lex.lex()
 
lexer.input(algoritmoAngel)
# Tokenizador
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
import datetime
import ply.lex as lex

reserved = {
    #Andrés Cornejo
    'nmap': 'NMAP',
    'do': 'DO',
    'break': 'BREAK',
    'puts': 'PUT',
    'redo': 'REDO',
    'BEGIN': 'BEGIN',
    'END': 'END',
    'case': 'CASE',
    'end' : 'END_LOWER',

    #Angel Tomalá
    'def' : 'DEF',
    'return': 'RETURN',
    'class' : 'CLASS',
    'if' : 'IF',
    'elsif' : 'ELSIF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'gets': 'GETS',
    'chomp' : 'CHOMP',
    'to_f': 'TO_F',
    'to_i': 'TO_I',
    'array': 'ARRAY',
    'new' : 'NEW',
    'and' : 'AND_RESERVED',
    'or' : 'OR_RESERVED',
    'to_s' : 'TO_S',

    #Andrés Amador
    'when' : 'WHEN',
    'defined?' : 'DEFINED',
    'in' : 'IN',
    'module' : 'MODULE',
    'self': 'SELF',
    'unless': 'UNLESS',
    'until': 'UNTIL',
    'then': 'THEN',
    'Set' : 'SET',
    'Proc' : 'PROC',
    'call' : 'CALL',
    'to_a' : 'TO_A',
}


tokens = (
    
        #Andrés Cornejo
    "QUOTATION",
    'HASH_ROCKET',
    'AND',
    'OR',
    'NOT',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EXPONENT',
    'MODULO',
    'ASSIGN',
    'PLUS_ASSIGN',
    'MINUS_ASSIGN',
    'MULTIPLY_ASSIGN',
    'DIVIDE_ASSIGN',
    'TRUE',
    'FALSE',

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
    'SYMBOL',
    'COMMA',
    'COLON',
    'LEFT_COR',
    'RIGHT_COR',
    'PERCENTW',
    'SPACE',

    #Andrés Amador
    'MODULO_ASSIGN',
    'EXPONENT_ASSIGN',
    'EQUAL',
    'NOT_EQUAL',
    'GREATER',
    'LESS',
    'GREATER_EQUAL',
    'LESS_EQUAL',
    'COMPARE',
    'CASE_EQUAL',
    'NEWLINE',
    'TAB',
    'BACKSLASH',
    'DOUBLE_QUOTE',
    'LEFTPAR',
    'RIGHTPAR',
    'RANGEIN',
    'RANGEEX',
    'AMPERSAND',
    'PIPE',
    'DOT',
    'CARET',
    'LBRACE',
    'RBRACE',
) + tuple(reserved.values())

#Andrés Cornejo
t_QUOTATION = r'"'
t_HASH_ROCKET = r'=>'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_EXPONENT = r'\*\*'
t_MODULO = r'%'
t_ASSIGN = r'='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_MULTIPLY_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='


#Angel Tomalá
t_INSTANCE_VAR = r'@[a-z_A-Z]\w*'
t_CLASS_VAR = r'@{2}[a-z_A-Z]\w*'
t_GLOBAL_VAR = r'\$[a-z_A-Z]\w*'
t_STRING = r'\'[^\']*\'|"[^"]*"'
t_BOOLEAN = r'\b(true|false)\b'
t_SYMBOL = r':[a-zA-Z_]\w*'
t_COMMA = r','
t_COLON = r':'
t_RIGHT_COR = r'\]'
t_LEFT_COR = r'\['
t_PERCENTW = r'%\w'
t_SPACE = r'\s'

#Andrés Amador
t_MODULO_ASSIGN = r'%='
t_EXPONENT_ASSIGN = r'\*\*='
t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATER_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_COMPARE = r'<=>'
t_CASE_EQUAL = r'==='
t_LEFTPAR = r'\('
t_RIGHTPAR = r'\)'
t_RANGEIN = r'\.\.'
t_RANGEEX = r'\.\.\.'
t_AMPERSAND = r'&'
t_PIPE = r'\|'
t_DOT = r'\.'
t_CARET = r'\^'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

def t_TRUE(t):
    r'\btrue\b'
    return t


def t_FALSE(t):
    r'\bfalse\b'
    return t

def t_LOCAL_VAR(t):
    r'[_a-z]\w*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_CONSTANT(t):
    r'[A-Z]\w*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)    
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

def t_NEWLINE(t):
    r'\\n'
    t.value = '\n'
    return t

def t_TAB(t):
    r'\\t'
    t.value = '\t'
    return t

def t_BACKSLASH(t):
    r'\\\\'
    t.value = '\\'
    return t

def t_DOUBLE_QUOTE(t):
    r'\\"'
    t.value = '"'
    return t

def t_error(t):
    print(f"Token no admitido '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

def t_newLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'  # Ignora espacios y tabulaciones


lexer = lex.lex()
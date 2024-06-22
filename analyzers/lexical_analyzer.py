import datetime
import ply.lex as lex

reserved = {
    #Andrés Cornejo
    'do': 'DO',
    'break': 'BREAK',
    'puts': 'PUT',
    'redo': 'REDO',
    'BEGIN': 'BEGIN',
    'END': 'END',
    'case': 'CASE',

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

    #Andrés Amador
    'when' : 'WHEN',
    'defined?' : 'DEFINED',
    'in' : 'IN',
    'module' : 'MODULE',
    'self': 'SELF',
    'unless': 'UNLESS',
    'until': 'UNTIL'
}


tokens = (
    
        #Andrés Cornejo
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
    'HASH',
    'DOT',
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
    'BIT_AND',
    'BIT_OR',
    'DOT',
) + tuple(reserved.values())

#Andrés Cornejo
t_AND = r'&'
t_OR = r'\|'
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
t_CONSTANT = r'[A-Z]\w*'
t_STRING = r'"[^"]*"'
t_BOOLEAN = r'\b(true|false)\b'
t_SYMBOL = r':[a-zA-Z_]\w*'
t_COMMA = r','
t_HASH = r'\{[^{}]*\}'
t_COLON = r':'
t_DOT = r'\.'
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
t_BIT_AND = r'&'
t_BIT_OR = r'\|'
t_DOT = r'\.'

def t_LOCAL_VAR(t):
    r'[_a-z]\w*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_FLOAT(t):
    r'(\d+\.\d*|\d*\.\d+)'
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

algoritmoAngel = '''
class Animal
  def initialize(name, species)
    @name = name
    @species = species
    _numfloat = 3.21
  end

  def greet
    puts "Hello, I'm #{@name}, a #{@species}."
  end
end

class Zoo
  attr_reader :animals

  def initialize(name)
    @name = name
    @animals = []
  end

  def add_animal(animal)
    @animals << animal
  end

  def show_animals
    puts "Animals in #{@name} Zoo:"
    @animals.each do |animal|
      animal.greet
    end
  end
end

def fibonacci(n)
  return n if n <= 1.4

  fib = [0, 1]
  (2..n).each do |i|
    fib[i] = fib[i - 1] + fib[i - 2]
  end

  fib[n]
end

zoo = Zoo.new("Wildlife")
zoo.add_animal(Animal.new("Buddy", "Dog"))
zoo.add_animal(Animal.new("Charlie", "Cat"))
zoo.add_animal(Animal.new("Ella", "Elephant"))

zoo.show_animals

puts "Fibonacci sequence:"
10.times do |i|
  puts "Fibonacci(#{i}): #{fibonacci(i)}"
end

'''

algoritmoAmador = '''
module Example
  def self.calculate
    a = 10
    b = 20

    unless a == b
      a += 1
      b **= 2
      result = a % b
    end

    if a != b
      puts "a is not equal to b"
    end

    range_inclusive = 1..10
    range_exclusive = 1...10

    if range_inclusive.include?(5)
      puts "5 is in the inclusive range"
    end

    if range_exclusive.include?(10)
      puts "10 is in the exclusive range"
    end

    case result
    when 0
      puts "Result is zero"
    else
      puts "Result is non-zero"
    end

    until result > 1000
      result *= 2
    end

    result %= 3

    puts "Final result: #{result}"
  end

  def self.check_defined
    if defined? (@@class_variable)
      puts "Class variable is defined"
    end
  end
end

Example.calculate
Example.check_defined
'''
algoritmoCornejo= '''
& &
if a < b && b > a
  puts "5"
end
| |
if a > b || c
  puts "This will not be printed"
else
  puts "4"
end

if !c
  puts "a"
end
sum = a + b
difference = a - b
product = a * b
quotient = b / a
exponentiation = a ** 2
modulo = b % a
* *
d = 5
puts "Initial d: #{d}"

d += a
puts "d after += a: #{d}"

d -= b
puts "d after -= b: #{d}"

d *= 2
puts "d after *= 2: #{d}"

d /= 3
puts "d after /= 3: #{d}"

'''
#AGREGAR LOS TOKENS ":" "(" ")" ","

lexer = lex.lex()

tokens_to_log = []

lexer.input(algoritmoAngel)
# Tokenizador
while True:
    tok = lexer.token()
    if not tok:
        break
    tokens_to_log.append(tok)
    #print(tok)

def save_tokens_to_log(github_user, date_hour):
    filename = f"/logs/lexical/lexical-{github_user}-{date_hour.strftime('%d%m%Y-%H%M')}.txt"
    with open(filename, "w") as file:
        for token in tokens_to_log:
            file.write(str(token) + "\n")
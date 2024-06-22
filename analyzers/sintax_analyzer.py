import datetime
import os
import sys
import ply.yacc as yacc
from lexical_analyzer import tokens, reserved


def p_codigo(p):
    ''' codigo : puts 
               | gets
               | estructurasDatos
               | estructurasControl
    '''
    
def p_estructurasDatos(p):
    ''' estructurasDatos : array
                         | var_arreglo
                         | acceder_arreglo
    
    '''

def p_estructurasControl(p):
    ''' estructurasControl : ifStatement
    '''

#-----------------Angel Tomalá-----------------
def p_value(p):
    ''' value : var
             | num
             | STRING
             | NIL
             | SYMBOL
          '''

def p_values_space(p):
    ''' values_space : value SPACE values_space
                     | value
    '''

def p_values(p):
    ''' values : value
               | value COMMA values 
               '''

def p_var(p):
    ''' var : LOCAL_VAR
           | INSTANCE_VAR
           | CLASS_VAR
           | GLOBAL_VAR
           | CONSTANT
           '''

def p_num(p):
    ''' num : FLOAT
           | INTEGER
           '''

def p_gets(p):
    ''' gets : GETS DOT CHOMP DOT TO_F
             | GETS DOT CHOMP DOT TO_I
             | GETS DOT CHOMP
    '''

def p_puts(p):
    ''' puts : PUT values 
    '''

# Estructura de datos (array)
def p_array(p):
    ''' array : array_explicito
              | array_implicito
              | array_creation
              | newArray
    '''

def p_array_explicito(p):
    ''' array_explicito : LEFT_COR values RIGHT_COR
                        | LEFT_COR RIGHT_COR
    '''

def p_array_implicito(p):
    ''' array_implicito : PERCENTW LEFT_COR values_space RIGHT_COR
                        | PERCENTW LEFT_COR RIGHT_COR
    '''

def p_array_creation(p):
    ''' array_creation : ARRAY LEFTPAR array_explicito RIGHTPAR
    '''

def p_newArray(p):
    ''' newArray : ARRAY DOT NEW 
                 | ARRAY DOT NEW LEFTPAR INTEGER RIGHTPAR
                 | ARRAY DOT NEW LEFTPAR INTEGER COMMA values RIGHTPAR
    '''

def p_var_arreglo(p):
    ''' var_arreglo : var
                    | var ASSIGN array
    '''

def p_acceder_arreglo(p):
    ''' acceder_arreglo : var_arreglo LEFT_COR INTEGER RIGHT_COR
    '''

# Estructura de control (if)
def p_ifStatement(p):
    ''' ifStatement : IF condiciones COLON codigo
                     | IF condiciones COLON codigo else_statement
    '''

def p_condiciones(p):
    ''' condiciones : condicion
                    | condiciones conectores condiciones
    '''

def p_conectores(p):
    ''' conectores : AND AND
                   | OR OR
    '''

def p_condicion(p):
    ''' condicion : num operComp num
    '''

def p_operComp(p):
    ''' operComp : GREATER
                 | LESS
                 | GREATER_EQUAL
                 | LESS_EQUAL
                 | EQUAL
                 | NOT_EQUAL
                 | COMPARE
    '''

def p_else_statement(p):
    ''' else_statement : ELSE COLON codigo
    '''

#-----------------Andrés Amador-----------------


#-----------------Andrés Cornejo-----------------



#-----------------------------------------------------------------------

algoritmoAngel = """
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

arrMal = 1212[xdd
"""

def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en linea {p.lineno}, posicion {p.lexpos}: Token inesperado '{p.value}' \n'{p}'"
    else:
        error_msg = "Syntax error: Unexpected end of input"
    print(error_msg)


parser = yacc.yacc()
"""
while True:
    try:
        s = input('ruby > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)

"""

#ASIGNAR AL ALGORITMO
s = algoritmoAngel
log_filename = f"sintactico-AngelT-lancervs-{datetime.datetime.now().strftime('%Y%m%d-%Hh%M')}.txt"
log_directory = "logs/syntax/"

log_filepath = os.path.join(log_directory, log_filename)

with open(log_filepath, "w") as f:
    sys.stdout = f
    result = parser.parse(algoritmoAngel)
    sys.stdout = sys.__stdout__
    print("Análisis completado. Los errores sintácticos se han guardado en el archivo de registro:", log_filename)
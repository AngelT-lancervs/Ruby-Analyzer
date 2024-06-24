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
                         | hash_declaration
                         | hash_access
                         | hash_operations
    
    '''

def p_estructurasControl(p):
    ''' estructurasControl : ifStatement
                           | while_statement
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
    ''' conectores : AND
                   | OR
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

#-----------------Andrés Cornejo-----------------
# Estructuras de datos (hash)
def p_hash_declaration(p):
    ''' hash_declaration : HASH LEFT_COR values RIGHT_COR
                         | HASH LEFT_COR RIGHT_COR
    '''

def p_hash_access(p):
    ''' hash_access : var LEFT_COR value RIGHT_COR
    '''

def p_hash_operations(p):
    ''' hash_operations : hash_access ASSIGN value
    '''

# Reglas sintácticas mínimas
def p_variable_declaration(p):
    ''' variable_declaration : var ASSIGN value
    '''

def p_store_conditional_result(p):
    ''' store_conditional_result : var ASSIGN ifStatement
    '''

def p_declare_data_structures(p):
    ''' declare_data_structures : variable_declaration
                                | array
                                | hash_declaration
    '''

# Estructuras de control (while)
def p_while_statement(p):
    ''' while_statement : WHILE condiciones COLON codigo
    '''

# Reglas sintácticas mínimas
def p_condition_with_connectors(p):
    ''' condition_with_connectors : condiciones conectores condiciones
    '''

# Funciones
def p_method_call(p):
    ''' method_call : var LEFTPAR values RIGHTPAR
                    | var LEFTPAR RIGHTPAR
    '''

def p_print_statement(p):
    ''' print_statement : PUT LEFTPAR values RIGHTPAR
    '''

# Expresiones
def p_boolean_expression(p):
    ''' boolean_expression : expression GREATER expression
                           | expression LESS expression
                           | expression GREATER_EQUAL expression
                           | expression LESS_EQUAL expression
                           | expression EQUAL expression
                           | expression NOT_EQUAL expression
                           | boolean_value '''


def p_boolean_value(p):
    ''' boolean_value : TRUE
                      | FALSE '''


def p_expression(p):
    ''' expression : INTEGER
                   | FLOAT
                   | variable
                   | STRING '''

def p_variable(p):
    ''' variable : LOCAL_VAR
                 | INSTANCE_VAR
                 | CLASS_VAR
                 | GLOBAL_VAR
                 | CONSTANT '''

# Declaraciones
def p_declaraciones(p):
    ''' declaraciones : variable_declaration
                      | store_conditional_result
                      | declare_data_structures
    '''

# Expresiones
def p_expresion(p):
    ''' expresion : puts
                 | gets
                 | print_statement
    '''

#-----------------Andrés Armador-----------------



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

algoritmoAndresCornejo = """
puts "xddd"
puts(hola mundo)
mi_hash = { 'nombre' => 'Juan', 'edad' => 30 }
mi_hash = { 'nombre' => 'Juan', 'edad' => 30, }

while contador < 5
  puts "Contador: #{contador}"
  contador += 1
end

contador = 0
while contador < 5
  puts "Contador: #{contador}"
end

mi_hash = { 'nombre' => 'Juan', 'edad' => 30 }
nombre = mi_hash['nombre']
puts "Nombre: #{nombre}"

mi_hash['edad'] = 31

mi_hash['ciudad'] = 'Bogotá'

mi_hash.delete('edad')

puts "Hash actualizado: #{mi_hash}"

a = 10
b = 20

if a > b
  puts "a es mayor que b"
else
  puts "a no es mayor que b"
end

is_raining = true
umbrella_available = false

if is_raining === umbrella_available
  puts "Tengo paraguas para la lluvia"
else
  puts "No tengo paraguas para la lluvia"
end


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
s = algoritmoAndresCornejo
log_filename = f"sintactico-AndresCornj-andresACF-{datetime.datetime.now().strftime('%Y%m%d-%Hh%M')}.txt"
log_directory = "logs/syntax/"

log_filepath = os.path.join(log_directory, log_filename)

with open(log_filepath, "w") as f:
    sys.stdout = f
    result = parser.parse(algoritmoAndresCornejo)
    sys.stdout = sys.__stdout__
    print("Análisis completado. Los errores sintácticos se han guardado en el archivo de registro:", log_filename)
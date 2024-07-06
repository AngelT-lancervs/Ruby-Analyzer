import datetime
import os
import sys
import ply.yacc as yacc
from lexical_analyzer import tokens, reserved

variablesString = {}
variablesNum = {}
variablesBool = {}
arreglos = {}


def p_codigo(p):
    ''' codigo : puts 
               | gets
               | estructurasDatos
               | estructurasControl
               | method_call
               | block_assignment
               | proc_assignment
               | proc_call
               | declaraciones
               | expression
               | to_string
    '''
def p_estructurasDatos(p):
    ''' estructurasDatos : array
                         | acceder_arreglo
                         | hash_declaration
                         | hash_access
                         | hash_operations
                         | set_expression
                         | set_operations
    '''

def p_estructurasControl(p):
    ''' estructurasControl : ifStatement
                           | while_statement
                           | unless_expression
    '''

#-----------------Angel Tomalá-----------------
def p_value(p):
    ''' value : num
             | var
             | STRING
             | NIL
             | SYMBOL
          '''
    p[0] = p[1]

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
           '''
    p[0] = p[1]

def p_num(p):
    ''' num : FLOAT
           | INTEGER
           '''
    p[0] = p[1] #importante para la regla semantica conversión implicita (Angel Tomalá)

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
    p[0] = [p[1]]

def p_var_arreglo(p):
    ''' var_arreglo : LOCAL_VAR ASSIGN array
    '''
    arreglos[p[1]] = p[3]

def p_array_explicito(p):
    ''' array_explicito : LEFT_COR values RIGHT_COR
                        | LEFT_COR RIGHT_COR
    '''
    p[0] = p[2]

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

def p_acceder_arreglo(p):
    ''' acceder_arreglo : var_arreglo LEFT_COR INTEGER RIGHT_COR
    '''

# Estructura de control (if)
def p_ifStatement(p):
    ''' ifStatement : IF condiciones NEWLINE codigo END_LOWER
                     | IF condiciones NEWLINE codigo NEWLINE else_statement END_LOWER
    '''

def p_condiciones(p):
    ''' condiciones : condicion
                    | condiciones conectores condiciones
    '''

def p_conectores(p):
    ''' conectores : AND
                   | OR
                   | AND_RESERVED
                   | OR_RESERVED
    '''

def p_condicion(p):
    ''' condicion : num operComp num
                  | var operComp num
                  | num operComp var
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
    ''' else_statement : ELSE NEWLINE codigo
    '''

def p_to_string(p):
    ''' to_string : LOCAL_VAR DOT TO_S
    '''
    if p[1] in variablesNum or p[1] in variablesString:
        variablesString[p[1]] = str(p[1])
        if p[1] in variablesNum:
            del variablesNum[p[1]]
            return
    else:
        print(f"Error semántico, Variable '{p[1]}' no existe.")
        return

#REGLA SEMÁNTICA 2 ANGEL TOMALÁ (CONCATENACION DE STRINGS, TRANSFORMAR LOS NUMEROS ANTES DE CONCATENAR)
def p_concatenar_string(p):
    ''' concatenar_string : STRING PLUS STRING
                          | STRING PLUS LOCAL_VAR
                          | LOCAL_VAR PLUS STRING
                          | LOCAL_VAR PLUS LOCAL_VAR
    '''
    for item in p:
        if item != "+":
            if isinstance(item, str):
                if item in variablesNum:
                    print(f"Error semántico, no se puede concatenar {item} sin convertir a string primero.")
                    break
        
                if item not in variablesString and not item.startswith("\""):
                    print(f"Error semántico, la variable '{item}' no existe.")
                    break

def p_declaracion_concatenar_string(p):
    ''' declaracion_concatenar_string : LOCAL_VAR ASSIGN concatenar_string
    '''
    variablesString[p[1]] = str(p[3])

# REGLA SEMÁNTICA 1 ANGEL TOMALÁ (CONVERSIÓN IMPLÍCITA DE ELEMENTOS)
def convert_to_float(value):
    if isinstance(value, int):
        print(f"Convertido implicitamente {value} a float.")
        return float(value)
    elif isinstance(value, list):
        # Asumiendo que value es una lista de subexpresiones, convierte cada una recursivamente
        return [convert_to_float(v) for v in value]
    return value

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
    ''' variable_declaration : LOCAL_VAR ASSIGN value
    '''
    if isinstance(p[3], str):
        variablesString[p[1]] = p[3]
    elif isinstance(p[3], int) or isinstance(p[3], float):
        variablesNum[p[1]] = p[3]

def p_store_conditional_result(p):
    ''' store_conditional_result : LOCAL_VAR ASSIGN condiciones
    '''
    variablesBool[p[1]] = p[3]

def p_declare_data_structures(p):
    ''' declare_data_structures : var_arreglo
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
                      | var_arreglo
                      | LOCAL_VAR ASSIGN arithmetic_production
                      | declaracion_concatenar_string
    '''

# Expresiones
def p_expresion(p):
    ''' expresion : puts
                 | gets
                 | print_statement
    '''

#-----------------Andrés Armador-----------------
def p_set_expression(p):
    """set_expression : SET DOT NEW LEFTPAR LEFT_COR values RIGHT_COR RIGHTPAR
                      | SET LEFT_COR values RIGHT_COR"""
    
def p_set_operations(p):
    """set_operations : set_expression
                      | set_operations set_binary_operators set_expression"""
    
def p_set_declaration(p):
    """declare_data_structures : LOCAL_VAR ASSIGN set_expression"""

    
def p_set_binary_operators(p):
    """set_binary_operators : PLUS
                            | MINUS
                            | AMPERSAND
                            | PIPE
                            | CARET"""
    
def p_unless_expression(p):
    """unless_expression : UNLESS boolean_expression THEN expresion END
                         | UNLESS boolean_expression THEN expresion ELSE expresion END"""

def p_arithmetic_production(p):
    """arithmetic_production : num
                             | LOCAL_VAR
                             | num arithmetic_operators arithmetic_production
                             | LOCAL_VAR arithmetic_operators arithmetic_production"""
    # REGLA SEMÁNTICA 1 ANGEL TOMALÁ (CONVERSIÓN IMPLÍCITA DE ELEMENTOS)
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:

        p[1] = convert_to_float(p[1])
        p[3] = convert_to_float(p[3])

        if isinstance(p[1], str):
            if p[1] not in variablesNum and p[1] not in variablesString:
                print(f"Error semántico, la variable {p[1]} no existe.")
                return
            elif p[1] in variablesString:
                print(f"Error semántico, la variable {p[1]} es una cadena y no puede participar en operaciones aritméticas.")
                return

        if isinstance(p[3], str):
            if p[3] not in variablesNum and p[3] not in variablesString:
                print(f"Error semántico, la variable {p[3]} no existe.")
                return
            elif p[3] in variablesString:
                print(f"Error semántico, la variable {p[3]} es una cadena y no puede participar en operaciones aritméticas.")
                return
        
def p_arithmetic_operators(p):
    """arithmetic_operators : PLUS
                            | MINUS
                            | MULTIPLY
                            | DIVIDE
                            | MODULO
                            | EXPONENT"""
    
def p_block_expression(p):
    """block_expression : LBRACE expresion RBRACE
                         | DO expresion END
                         | LBRACE PIPE LOCAL_VAR PIPE expresion RBRACE
                         | DO PIPE LOCAL_VAR PIPE expresion END"""
    
def p_block_assignment(p):
    """block_assignment : method_call block_expression"""

def p_proc_expression(p):
    """proc_expression : PROC DOT NEW block_expression"""

def p_proc_assignment(p):
    """proc_assignment : LOCAL_VAR ASSIGN proc_expression"""
    variablesString[p[1]] = p[3]

def p_proc_call(p):
    """proc_call : LOCAL_VAR DOT CALL LEFTPAR values RIGHTPAR
                 | LOCAL_VAR DOT LEFTPAR values RIGHTPAR
                 | LOCAL_VAR LEFT_COR values RIGHT_COR"""
    
def p_condition_expr(p):
    """expresion : condition_with_connectors"""


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
    if @name == 3 
        @animals.each do |animal|
      animal.greet
        end
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

algoritmoAmador = """
require 'set'

# Declaración de Sets y operaciones de Sets
set1 = Set.new([1, 2, 3])
set2 = Set.new([3, 4, 5])

union_set = set1 | set2
intersection_set = set1 & set2
difference_set = set1 - set2

puts "Union de sets: #{union_set.to_a}"
puts "Intersección de sets: #{intersection_set.to_a}"
puts "Diferencia de sets: #{difference_set.to_a}"

# Expresión unless
x = 10
y = 5

unless y >= x
  puts "y es menor que x"
end

unless x < y
  puts "x no es menor que y"
end

# Expresión aritmética
a = 10
b = 5

sum = a + b
difference = a - b
product = a * b
quotient = a / b
modulo = a % b

puts "Suma: #{sum}"
puts "Resta: #{difference}"
puts "Producto: #{product}"
puts "Cociente: #{quotient}"
puts "Modulo: #{modulo}"

# Asignación de block
block = proc { |x| x * 2 }
result = block.call(5)

puts "Resultado del bloque: #{result}"

# Asignación y llamada de procs
my_proc = Proc.new { |x, y| x + y }
proc_result = my_proc.call(2, 3)

puts "Resultado del proc: #{proc_result}"

"""

def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en linea {p.lineno}, posicion {p.lexpos}: Token inesperado '{p.value}' \n'{p}'"
    else:
        error_msg = "Syntax error: Unexpected end of input"
    print(error_msg)


parser = yacc.yacc()

while True:
    try:
        s = input('ruby > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)


#ASIGNAR AL ALGORITMO
s = algoritmoAngel
log_filename = f"sintactico-AngelT-lancervs-{datetime.datetime.now().strftime('%Y%m%d-%Hh%M')}.txt"
log_directory = "logs/syntax/"

log_filepath = os.path.join(log_directory, log_filename)

with open(log_filepath, "w") as f:
    sys.stdout = f
    result = parser.parse(s)
    sys.stdout = sys.__stdout__
    print("Análisis completado. Los errores sintácticos se han guardado en el archivo de registro:", log_filename)
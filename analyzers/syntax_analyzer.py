import datetime
import os
import sys
import ply.yacc as yacc
from analyzers.lexical_analyzer import tokens, reserved
import re

variablesString = {}
variablesNum = {}
variablesBool = {}
variablesProc = {}
arreglos = {}
hashes = {}


def p_codigo(p):
    '''codigo : sentencia
              | codigo sentencia'''
    
def p_sentencia(p):
    '''sentencia : puts 
                 | gets
                 | estructurasDatos
                 | estructurasControl
                 | method_call
                 | block_assignment
                 | proc_call
                 | declaraciones
                 | expression
                 | to_string
                 | comparador
                 | range_expression
                 | range_to_a'''

def p_estructurasDatos(p):
    ''' estructurasDatos : array
                         | acceder_arreglo
                         | hash_operations
                         | hash_var
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
               | value COMMA values'''


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
    ''' ifStatement : IF condiciones codigo END_LOWER
                     | IF condiciones codigo else_statement END_LOWER
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
                   | EQUAL
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
    ''' else_statement : ELSE codigo
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
# REGLA SEMÁNTICA 2 ANDRÉS C0RNEJO (CLAVE DUPLICADA EN HASH)
def p_hash_var(p):
    ''' hash_var : LOCAL_VAR ASSIGN LBRACE hash_values RBRACE
                 | LOCAL_VAR ASSIGN LBRACE RBRACE
    '''
    if len(p) == 6:
        # Verificar que p[4] no sea None antes de intentar fusionarlo
        if p[4] is not None:
            p[0] = {**p[4]}
        else:
            p[0] = None
    else:
        p[0] = {}

def p_hash_values(p):
    ''' hash_values : STRING HASH_ROCKET value
                    | STRING HASH_ROCKET value COMMA hash_values
    '''
    if len(p) == 4:
        p[0] = {p[1]: p[3]}
    elif len(p) == 6:
        # Verificar si hay una clave duplicada en p[5]
        if p[1] in p[5]:
            print(f"Error semántico: Clave duplicada '{p[1]}'.")
            p[0] = None
        else:
            p[0] = {p[1]: p[3], **p[5]}

def check_duplicate_keys(new_dict):
    seen_keys = set()
    for key in new_dict:
        if key in seen_keys:
            print(f"Error semántico: Clave duplicada '{key}'.")
        seen_keys.add(key)

        
def p_hash_access(p):
    ''' hash_access : var LBRACE value RBRACE
    '''

def p_hash_operations(p):
    ''' hash_operations : hash_access ASSIGN value
    '''

# Reglas sintácticas mínimas
def p_variable_declaration(p):
    ''' variable_declaration : LOCAL_VAR ASSIGN value
                             | LOCAL_VAR PLUS_ASSIGN value
                             | LOCAL_VAR MULTIPLY_ASSIGN value
                             | LOCAL_VAR MINUS_ASSIGN value
                             | LOCAL_VAR DIVIDE_ASSIGN value
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
                                | hash_var
    '''

# Estructuras de control (while)
def p_while_statement(p):
    ''' while_statement : WHILE condiciones codigo END_LOWER
    '''

# Reglas sintácticas mínimas
def p_condition_with_connectors(p):
    ''' condition_with_connectors : condiciones conectores condiciones
    '''

# Funciones
def p_method_call(p):
    ''' method_call : LOCAL_VAR LEFTPAR values RIGHTPAR
                    | LOCAL_VAR LEFTPAR RIGHTPAR
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
                      | hash_var
                      | LOCAL_VAR ASSIGN arithmetic_production
                      | declaracion_concatenar_string
                      | proc_assignment
                      | range_declare
    '''

# Expresiones
def p_expresion(p):
    ''' expresion : puts
                 | gets
                 | print_statement
    '''



# REGLA SEMÁNTICA 1 ANDRES CORNEJO (REGLAS DE TIPO EN UNA COMPARACIÓN)
def p_comparador(p):
    ''' comparador : value EQUAL value
                   | value COMPARE value
    '''
    left_value = get_variable_value(p[1])
    right_value = get_variable_value(p[3])

    if left_value is None or right_value is None:
        print("Error semántico: Variable no inicializada.")
        p[0] = False
        return
    try:
        result = left_value == right_value
        if result:
            print(f"La comparación '{left_value} == {right_value}' es Verdadera.")
        else:
            print(f"La comparación '{left_value} == {right_value}' es Falsa.")
    except TypeError:
        print(f"No se puede comparar '{left_value}' con '{right_value}'. Tipos de datos incompatibles.")
        result = False

    p[0] = result  # Asignar el resultado al índice cero de p

# Aquí continúan las definiciones y funciones adicionales...
#----------- Presencia de las variables en los diccionarios----Andrés Cornejo ------
def get_variable_value(variable):
    if isinstance(variable, str):
        if variable in variablesNum:
            return variablesNum[variable]
        elif variable in variablesString:
            return variablesString[variable]
        elif variable in variablesBool:
            return variablesBool[variable]
        elif variable in hashes:
            return hashes[variable]
        else:
            print(f"Error semántico: Variable '{variable}' no inicializada.")
            return None
    else:
        return variable 

#-----------------Andrés Armador-----------------
def p_range_declare(p):
    """range_declare : LOCAL_VAR ASSIGN range_expression"""

def p_range_expression(p):
    """range_expression : value RANGEIN value
                        | value RANGEEX value
                        | LEFTPAR value RANGEIN value RIGHTPAR
                        | LEFTPAR value RANGEEX value RIGHTPAR"""
    
    if len(p) == 4:
        if type(p[1]) != type(p[3]):
            print('Error semantico: Valores distintos en rango')
            return
    if len(p) == 6:
        if type(p[2]) != type(p[4]):
            print('Error semantico: Valores distintos en rango')
            return

#Regla semantica 2 (rango a arreglo) Andres Amador
def p_range_to_a(p):
    """range_to_a : LEFTPAR value RANGEIN value RIGHTPAR DOT TO_A
                  | LEFTPAR value RANGEEX value RIGHTPAR DOT TO_A"""
    
    if type(p[2]) != type(p[4]):
        print('Error semántico: Valores distintos en rango')
        return
    
    if isinstance(p[2], float) or isinstance(p[4], float):
        print("Error semántico: No se puede convertir a arreglo un rango de flotantes")
        return




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
                         | DO expresion END_LOWER
                         | LBRACE PIPE LOCAL_VAR PIPE expresion RBRACE
                         | DO PIPE LOCAL_VAR PIPE expresion END
                         | DO PIPE LOCAL_VAR PIPE expresion END_LOWER"""
    
def p_block_assignment(p):
    """block_assignment : method_call block_expression"""

def p_proc_expression(p):
    """proc_expression : PROC DOT NEW block_expression"""

#REGLA SEMANTICA ANDRÉS AMADOR (LLAMADA DE PROCS)
def p_proc_assignment(p):
    """proc_assignment : LOCAL_VAR ASSIGN proc_expression"""
    variablesProc[p[1]] = p[3]

def p_proc_call(p):
    """proc_call : LOCAL_VAR DOT CALL LEFTPAR values RIGHTPAR
                 | LOCAL_VAR DOT LEFTPAR values RIGHTPAR
                 | LOCAL_VAR DOT CALL LEFTPAR RIGHTPAR
                 | LOCAL_VAR DOT LEFTPAR RIGHTPAR"""
    
    if p[1] in variablesProc:
        pass
    else:
        print(f"Error semántico: La variable \"{p[1]}\" no existe o no es un proc")

def p_proc_call_cor(p):
    """proc_call : LOCAL_VAR LEFT_COR values RIGHT_COR
                 | LOCAL_VAR LEFT_COR RIGHT_COR"""
    
    if p[1] in variablesProc or p[1] in arreglos:
        pass
    else:
        print(f"Error semántico: La variable \"{p[1]}\" no existe o no es un proc")
    
def p_condition_expr(p):
    """expresion : condition_with_connectors"""


#-----------------------------------------------------------------------

def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en linea {p.lineno}, posicion {p.lexpos}: Token inesperado '{p.value}' \n'{p}'"
    else:
        error_msg = "Syntax error: Unexpected end of input"
    print(error_msg)


parser = yacc.yacc()

def capture_semantic_errors(input_code):
    log_directory = "logs/semantic/"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_filename = f"semantic-amadoran-{datetime.datetime.now().strftime('%Y%m%d-%Hh%M')}.txt"
    log_filepath = os.path.join(log_directory, log_filename)

    with open(log_filepath, "w") as f:
        sys.stdout = f
        lines = input_code.strip().split('\n')
        for line_num, line in enumerate(lines, start=1):
            try:
                parser.parse(line)
            except Exception as e:
                print(f"Error en línea {line_num}: {e}")
        sys.stdout = sys.__stdout__
    
    print("Análisis completado. Los errores semánticos se han guardado en el archivo de registro:", log_filename)

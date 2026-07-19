T_INT   = "INT" # entero
T_BOOL  = "BOOL" # booleano
T_OP    = "OP" # operador
T_ID    = "IDENTIFIER" # identificador
T_EOF   = "EOF" # fin de archivo

T_LPAREN = "LPAREN" # (
T_RPAREN = "RPAREN" # )
T_LBRACE = "LBRACE" # {
T_RBRACE = "RBRACE" # }
T_COMMA  = "COMMA" # ,

T_SI       = "SI" # si
T_SINO     = "SINO" # sino
T_MIENTRAS = "MIENTRAS" # mientras
T_TAREA    = "TAREA" # tarea
T_HAZ      = "HAZ" # haz
T_HACER    = "HACER" # hacer
T_VER      = "VER" # ver
T_TOMAR    = "TOMAR" # tomar

# TODO: Añadir los tokens para el tipo string
# T_STRING = "STRING" # cadena de texto

KEYWORDS = {
    "si":         T_SI, # Condicional if
    "sino":       T_SINO, # Condicional if-else
    "mientras":   T_MIENTRAS, # Ciclo while
    "tarea":      T_TAREA, # función
    "haz":        T_HAZ, # retornar
    "hacer":      T_HACER, # Ciclo for
    "ver":        T_VER, # imprimir o mostrar
    "tomar":      T_TOMAR, # tomar un valor
    
    # TODO: AÑADIR LAS PALABRAS RESERVADAS PARA TRUE Y FALSE
    # "verdadero":  T_BOOL,   # o T_TRUE
    # "falso":      T_BOOL,   # o T_FALSE
}

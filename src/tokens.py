T_INT   = "INT" # entero
T_BOOL  = "BOOL" # booleano
T_OP    = "OP" # operador
T_ID    = "IDENTIFIER" # identificador
T_EOF   = "EOF" # fin de archivo

T_SI       = "SI"
T_SINO     = "SINO"
T_MIENTRAS = "MIENTRAS"
T_TAREA    = "TAREA"
T_HAZ      = "HAZ"
T_HACER    = "HACER"
T_VER      = "VER"
T_TOMAR    = "TOMAR"

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

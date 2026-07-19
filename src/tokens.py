T_INT   = "INT"
T_BOOL  = "BOOL"
T_OP    = "OP"
T_ID    = "IDENTIFIER"
T_EOF   = "EOF"

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
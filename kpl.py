import sys

from src.lexer import Lexer
from src.interpreter import Interpreter
from src.tokens import T_EOF


def main():
    # Validamos que pases el archivo por consola
    if len(sys.argv) < 2:
        print("Uso: python kpl.py <archivo.kpl>")
        return

    filename = sys.argv[1]

    # Leemos tu código personalizado
    with open(filename, encoding="utf-8") as file:
        code = file.read()

    # 1. Pasar el texto por el Lexer para obtener los tokens
    lexer = Lexer(code)
    tokens = []
    token = lexer.get_next_token()
    tokens.append(token)

    while token[0] != T_EOF:
        token = lexer.get_next_token()
        tokens.append(token)

    # 2. El intérprete ejecuta esos tokens directamente
    interpreter = Interpreter(tokens)
    interpreter.run()


if __name__ == "__main__":
    main()

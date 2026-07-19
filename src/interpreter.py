from src.tokens import (
    T_INT,
    T_OP,
    T_ID,
    T_EOF,
    T_LPAREN,
    T_RPAREN,
    T_LBRACE,
    T_RBRACE,
    T_COMMA,
    T_SI,
    T_SINO,
    T_MIENTRAS,
    T_TAREA,
    T_HAZ,
    T_HACER,
    T_VER,
    T_TOMAR,
) # Tokens para el intérprete

# Clase para manejar el retorno de valores
class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

# Clase para manejar el intérprete
class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else (T_EOF, None)
        self.scopes = [{}]
        self.const_scopes = [set()]
        self.functions = {}

    # Método para avanzar en los tokens
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = (T_EOF, None)

    # Método para ver el siguiente token
    def peek_token(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return (T_EOF, None)

    # Método para esperar un token específico
    def expect(self, token_type, value=None):
        token = self.current_token
        if token[0] != token_type or (value is not None and token[1] != value):
            expected = value if value is not None else token_type
            raise Exception(
                f"Se esperaba '{expected}', se encontró '{token[1]}' ({token[0]})"
            )
        self.advance()
        return token

    # Método para esperar un operador específico
    def expect_op(self, op):
        return self.expect(T_OP, op)

    # Método para verificar si un nombre es una constante
    @staticmethod
    def _is_const_name(name):
        return bool(name) and all(c.isupper() or c == "_" for c in name) and any(
            c.isupper() for c in name
        )

    # Método para verificar si un nombre es una variable
    @staticmethod
    def _is_var_name(name):
        return bool(name) and all(
            c.islower() or c.isdigit() or c == "_" for c in name
        ) and not name[0].isdigit()

    # Método para buscar una variable en los scopes
    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Variable no definida: '{name}'")

    # Método para asignar un valor a una variable
    def assign(self, name, value):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name in self.scopes[i]:
                if name in self.const_scopes[i]:
                    raise Exception(f"No se puede reasignar la constante '{name}'")
                self.scopes[i][name] = value
                return

        if self._is_const_name(name):
            self.const_scopes[-1].add(name)
        elif not self._is_var_name(name):
            raise Exception(
                f"Nombre inválido '{name}': usa minúsculas para variables "
                "o MAYÚSCULAS para constantes"
            )
        self.scopes[-1][name] = value

    # Método para ejecutar el intérprete
    def run(self):
        while self.current_token[0] != T_EOF:
            self.statement()

    # Método para ejecutar un bloque de tokens
    def run_tokens(self, tokens):
        saved_tokens = self.tokens
        saved_pos = self.pos
        saved_current = self.current_token

        self.tokens = list(tokens) + [(T_EOF, None)]
        self.pos = 0
        self.current_token = self.tokens[0]
        try:
            while self.current_token[0] != T_EOF:
                self.statement()
        finally:
            self.tokens = saved_tokens
            self.pos = saved_pos
            self.current_token = saved_current

    # Método para evaluar un bloque de tokens
    def eval_tokens(self, tokens):
        saved_tokens = self.tokens
        saved_pos = self.pos
        saved_current = self.current_token

        self.tokens = list(tokens) + [(T_EOF, None)]
        self.pos = 0
        self.current_token = self.tokens[0]
        try:
            return self.parse_expression()
        finally:
            self.tokens = saved_tokens
            self.pos = saved_pos
            self.current_token = saved_current

    # Método para recoger tokens hasta encontrar un tipo específico
    def collect_until(self, stop_types):
        tokens = []
        depth_paren = 0
        depth_brace = 0

        while self.current_token[0] != T_EOF:
            token_type = self.current_token[0]
            if depth_paren == 0 and depth_brace == 0 and token_type in stop_types:
                break

            if token_type == T_LPAREN:
                depth_paren += 1
            elif token_type == T_RPAREN:
                depth_paren -= 1
            elif token_type == T_LBRACE:
                depth_brace += 1
            elif token_type == T_RBRACE:
                depth_brace -= 1

            tokens.append(self.current_token)
            self.advance()

        return tokens

    # Método para recoger un bloque de tokens
    def collect_block(self):
        self.expect(T_LBRACE)
        tokens = []
        depth = 1

        while self.current_token[0] != T_EOF and depth > 0:
            token_type = self.current_token[0]
            if token_type == T_LBRACE:
                depth += 1
            elif token_type == T_RBRACE:
                depth -= 1
                if depth == 0:
                    self.advance()
                    break
            tokens.append(self.current_token)
            self.advance()

        if depth != 0:
            raise Exception("Bloque sin cerrar: falta '}'")
        return tokens

    # Método para ejecutar una sentencia
    def statement(self):
        token_type = self.current_token[0]

        if token_type == T_VER:
            self.statement_ver()
        elif token_type == T_SI:
            self.statement_si()
        elif token_type == T_MIENTRAS:
            self.statement_mientras()
        elif token_type == T_HACER:
            self.statement_hacer()
        elif token_type == T_TAREA:
            self.statement_tarea()
        elif token_type == T_HAZ:
            self.statement_haz()
        elif token_type == T_ID:
            self.statement_id()
        elif token_type == T_LBRACE:
            self.run_tokens(self.collect_block())
        else:
            raise Exception(
                f"Sentencia inesperada: '{self.current_token[1]}' ({token_type})"
            )

    # Método para ejecutar una sentencia de ver
    def statement_ver(self):
        self.expect(T_VER)
        value = self.parse_expression()
        print(value)

    # Método para ejecutar una sentencia de identificador
    def statement_id(self):
        next_token = self.peek_token()

        if next_token[0] == T_OP and next_token[1] == "=":
            name = self.current_token[1]
            self.advance()
            self.expect_op("=")
            value = self.parse_rhs()
            self.assign(name, value)
        elif next_token[0] == T_LPAREN:
            self.parse_expression()
        else:
            raise Exception(
                f"Sentencia inválida cerca de '{self.current_token[1]}'"
            )

    # Método para parsear el derecho de una asignación
    def parse_rhs(self):
        if self.current_token[0] == T_TOMAR:
            self.advance()
            return int(input())
        return self.parse_expression()

    # Método para ejecutar una sentencia de si
    def statement_si(self):
        self.expect(T_SI)
        condition = self.parse_expression()
        then_body = self.collect_block()
        else_body = None

        if self.current_token[0] == T_SINO:
            self.advance()
            else_body = self.collect_block()

        if condition:
            self.run_tokens(then_body)
        elif else_body is not None:
            self.run_tokens(else_body)

    # Método para ejecutar una sentencia de mientras
    def statement_mientras(self):
        self.expect(T_MIENTRAS)
        condition_tokens = self.collect_until({T_LBRACE})
        body = self.collect_block()

        while self.eval_tokens(condition_tokens):
            self.run_tokens(body)

    # Método para ejecutar una sentencia de hacer
    def statement_hacer(self):
        self.expect(T_HACER)
        init_tokens = self.collect_until({T_COMMA})
        self.expect(T_COMMA)
        condition_tokens = self.collect_until({T_COMMA})
        self.expect(T_COMMA)
        step_tokens = self.collect_until({T_LBRACE})
        body = self.collect_block()

        self.run_tokens(init_tokens)
        while self.eval_tokens(condition_tokens):
            self.run_tokens(body)
            self.run_tokens(step_tokens)

    # Método para ejecutar una sentencia de tarea
    def statement_tarea(self):
        self.expect(T_TAREA)
        name = self.expect(T_ID)[1]
        self.expect(T_LPAREN)

        params = []
        if self.current_token[0] != T_RPAREN:
            params.append(self.expect(T_ID)[1])
            while self.current_token[0] == T_COMMA:
                self.advance()
                params.append(self.expect(T_ID)[1])

        self.expect(T_RPAREN)
        body = self.collect_block()
        self.functions[name] = (params, body)

    # Método para ejecutar una sentencia de haz
    def statement_haz(self):
        self.expect(T_HAZ)
        value = self.parse_expression()
        raise ReturnSignal(value)

    # Método para llamar a una función
    def call_function(self, name, args):
        if name not in self.functions:
            raise Exception(f"Función no definida: '{name}'")

        params, body = self.functions[name]
        if len(params) != len(args):
            raise Exception(
                f"'{name}' espera {len(params)} argumento(s), recibió {len(args)}"
            )

        self.scopes.append(dict(zip(params, args)))
        self.const_scopes.append(set())
        try:
            self.run_tokens(body)
            return 0
        except ReturnSignal as signal:
            return signal.value
        finally:
            self.scopes.pop()
            self.const_scopes.pop()

    # Método para parsear la lista de argumentos de una función
    def parse_arg_list(self):
        self.expect(T_LPAREN)
        args = []
        if self.current_token[0] != T_RPAREN:
            args.append(self.parse_expression())
            while self.current_token[0] == T_COMMA:
                self.advance()
                args.append(self.parse_expression())
        self.expect(T_RPAREN)
        return args

    # Método para parsear una expresión
    def parse_expression(self):
        return self.parse_comparison()

    # Método para parsear una comparación
    def parse_comparison(self):
        left = self.parse_additive()

        while self.current_token[0] == T_OP and self.current_token[1] in {
            "==",
            "!=",
            "<",
            ">",
        }:
            op = self.current_token[1]
            self.advance()
            right = self.parse_additive()
            if op == "==":
                left = 1 if left == right else 0
            elif op == "!=":
                left = 1 if left != right else 0
            elif op == "<":
                left = 1 if left < right else 0
            elif op == ">":
                left = 1 if left > right else 0

        return left

    # Método para parsear una suma o resta
    def parse_additive(self):
        left = self.parse_term()

        while self.current_token[0] == T_OP and self.current_token[1] in {"+", "-"}:
            op = self.current_token[1]
            self.advance()
            right = self.parse_term()
            if op == "+":
                left = left + right
            else:
                left = left - right

        return left

    # Método para parsear un término
    def parse_term(self):
        left = self.parse_factor()

        while self.current_token[0] == T_OP and self.current_token[1] in {"*", "/"}:
            op = self.current_token[1]
            self.advance()
            right = self.parse_factor()
            if op == "*":
                left = left * right
            else:
                if right == 0:
                    raise Exception("División entre cero")
                left = left // right

        return left

    # Método para parsear un factor
    def parse_factor(self):
        token = self.current_token

        if token[0] == T_OP and token[1] == "-":
            self.advance()
            return -self.parse_factor()

        if token[0] == T_INT:
            self.advance()
            return token[1]

        if token[0] == T_ID:
            name = token[1]
            self.advance()
            if self.current_token[0] == T_LPAREN:
                args = self.parse_arg_list()
                return self.call_function(name, args)
            return self.lookup(name)

        if token[0] == T_LPAREN:
            self.advance()
            value = self.parse_expression()
            self.expect(T_RPAREN)
            return value

        raise Exception(
            f"Expresión inválida cerca de '{token[1]}' ({token[0]})"
        )

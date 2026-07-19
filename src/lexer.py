from src.tokens import T_INT, T_OP, T_ID, T_EOF, KEYWORDS


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return (T_INT, int(result))

    def get_identifier(self):
        result = ""
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()

        if result in KEYWORDS:
            return (KEYWORDS[result], result)
        return (T_ID, result)

    def get_operator(self):
        char = self.current_char
        next_char = self.peek()

        if char == "=" and next_char == "=":
            self.advance()
            self.advance()
            return (T_OP, "==")

        if char == "!" and next_char == "=":
            self.advance()
            self.advance()
            return (T_OP, "!=")

        if char in {"+", "-", "*", "/", "=", "<", ">"}:
            self.advance()
            return (T_OP, char)

        raise Exception(f"Carácter ilegal detectado: '{self.current_char}'")

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.get_number()

            if self.current_char.isalpha() or self.current_char == "_":
                return self.get_identifier()

            if self.current_char in {"+", "-", "*", "/", "=", "<", ">", "!"}:
                return self.get_operator()

            raise Exception(f"Carácter ilegal detectado: '{self.current_char}'")

        return (T_EOF, None)

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token[0] == T_EOF:
                break
        return tokens

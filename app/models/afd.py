# =============================================================================
# MODEL — Autómatas Finitos Deterministas (AFD)
# Cada autómata está definido por su quíntupla M = (Q, Σ, δ, q0, F)
# =============================================================================

from enum import Enum, auto


class TokenType(Enum):
    PALABRA_RESERVADA = "PALABRA_RESERVADA"
    IDENTIFICADOR     = "IDENTIFICADOR"
    NUMERO            = "NUMERO"
    OPERADOR_LOGICO   = "OPERADOR_LOGICO"
    OPERADOR_RELACIONAL = "OPERADOR_RELACIONAL"
    OPERADOR_ARITMETICO = "OPERADOR_ARITMETICO"
    SIMBOLO           = "SIMBOLO"
    INVALIDO          = "INVALIDO"


class Token:
    """Representa un token reconocido por el analizador léxico."""

    def __init__(self, tipo: TokenType, lexema: str, linea: int, columna: int):
        self.tipo    = tipo
        self.lexema  = lexema
        self.linea   = linea
        self.columna = columna

    def to_dict(self) -> dict:
        return {
            "tipo":    self.tipo.value,
            "lexema":  self.lexema,
            "linea":   self.linea,
            "columna": self.columna,
        }

    def __repr__(self):
        return f"Token({self.tipo.value}, '{self.lexema}', L{self.linea}:C{self.columna})"


# =============================================================================
# AFD 1 — IDENTIFICADORES
# Q  = {q0, q1, q_err}
# Σ  = letras, dígitos, _
# F  = {q1}
# q0 = q0
# δ:
#   q0 + (letra|_) → q1
#   q0 + dígito    → q_err
#   q1 + (letra|_|dígito) → q1
# =============================================================================

class AFD_Identificador:
    ESTADOS = {"q0", "q1", "q_err"}
    ESTADO_INICIAL = "q0"
    ESTADOS_ACEPTACION = {"q1"}

    @staticmethod
    def _clasificar(c: str) -> str:
        if c.isalpha() or c == "_":
            return "letra_"
        if c.isdigit():
            return "digito"
        return "otro"

    def transicion(self, estado: str, simbolo: str) -> str:
        cat = self._clasificar(simbolo)
        delta = {
            "q0": {"letra_": "q1",  "digito": "q_err", "otro": "q_err"},
            "q1": {"letra_": "q1",  "digito": "q1",    "otro": "q_err"},
            "q_err": {"letra_": "q_err", "digito": "q_err", "otro": "q_err"},
        }
        return delta[estado][cat]

    def acepta(self, cadena: str) -> bool:
        estado = self.ESTADO_INICIAL
        for c in cadena:
            estado = self.transicion(estado, c)
        return estado in self.ESTADOS_ACEPTACION


# =============================================================================
# AFD 2 — NÚMEROS  (enteros y decimales)
# Q  = {q0, q1, q2, q3, q_err}
# Σ  = dígitos, punto
# F  = {q1, q3}
# δ:
#   q0 + dígito → q1
#   q1 + dígito → q1
#   q1 + punto  → q2
#   q2 + dígito → q3
#   q3 + dígito → q3
# =============================================================================

class AFD_Numero:
    ESTADOS = {"q0", "q1", "q2", "q3", "q_err"}
    ESTADO_INICIAL = "q0"
    ESTADOS_ACEPTACION = {"q1", "q3"}

    @staticmethod
    def _clasificar(c: str) -> str:
        if c.isdigit():
            return "digito"
        if c == ".":
            return "punto"
        return "otro"

    def transicion(self, estado: str, simbolo: str) -> str:
        cat = self._clasificar(simbolo)
        delta = {
            "q0": {"digito": "q1",    "punto": "q_err", "otro": "q_err"},
            "q1": {"digito": "q1",    "punto": "q2",    "otro": "q_err"},
            "q2": {"digito": "q3",    "punto": "q_err", "otro": "q_err"},
            "q3": {"digito": "q3",    "punto": "q_err", "otro": "q_err"},
            "q_err": {"digito": "q_err", "punto": "q_err", "otro": "q_err"},
        }
        return delta[estado][cat]

    def acepta(self, cadena: str) -> bool:
        estado = self.ESTADO_INICIAL
        for c in cadena:
            estado = self.transicion(estado, c)
        return estado in self.ESTADOS_ACEPTACION


# =============================================================================
# AFD 3 — OPERADORES LÓGICOS: &&  ||  !
# Q  = {q0, q1_amp, q2_and, q3_pipe, q4_or, q5_not, q_err}
# F  = {q2_and, q4_or, q5_not}
# =============================================================================

class AFD_OperadorLogico:
    ESTADOS = {"q0", "q1_amp", "q2_and", "q3_pipe", "q4_or", "q5_not", "q_err"}
    ESTADO_INICIAL = "q0"
    ESTADOS_ACEPTACION = {"q2_and", "q4_or", "q5_not"}

    @staticmethod
    def _clasificar(c: str) -> str:
        if c == "&":  return "amp"
        if c == "|":  return "pipe"
        if c == "!":  return "excl"
        return "otro"

    def transicion(self, estado: str, simbolo: str) -> str:
        cat = self._clasificar(simbolo)
        delta = {
            "q0":     {"amp": "q1_amp", "pipe": "q3_pipe", "excl": "q5_not", "otro": "q_err"},
            "q1_amp": {"amp": "q2_and", "pipe": "q_err",   "excl": "q_err",  "otro": "q_err"},
            "q2_and": {"amp": "q_err",  "pipe": "q_err",   "excl": "q_err",  "otro": "q_err"},
            "q3_pipe":{"amp": "q_err",  "pipe": "q4_or",   "excl": "q_err",  "otro": "q_err"},
            "q4_or":  {"amp": "q_err",  "pipe": "q_err",   "excl": "q_err",  "otro": "q_err"},
            "q5_not": {"amp": "q_err",  "pipe": "q_err",   "excl": "q_err",  "otro": "q_err"},
            "q_err":  {"amp": "q_err",  "pipe": "q_err",   "excl": "q_err",  "otro": "q_err"},
        }
        return delta[estado][cat]

    def acepta(self, cadena: str) -> bool:
        estado = self.ESTADO_INICIAL
        for c in cadena:
            estado = self.transicion(estado, c)
        return estado in self.ESTADOS_ACEPTACION


# =============================================================================
# AFD 4 — OPERADORES RELACIONALES: == != < > <= >=
# Q  = {q0, q1_lt, q1_gt, q1_eq, q1_bang, q2_leq, q2_geq, q2_eqeq, q2_neq, q_err}
# F  = {q1_lt, q1_gt, q2_leq, q2_geq, q2_eqeq, q2_neq}
# =============================================================================

class AFD_OperadorRelacional:
    ESTADO_INICIAL = "q0"
    ESTADOS_ACEPTACION = {"q1_lt", "q1_gt", "q2_leq", "q2_geq", "q2_eqeq", "q2_neq"}

    @staticmethod
    def _clasificar(c: str) -> str:
        if c == "<":  return "lt"
        if c == ">":  return "gt"
        if c == "=":  return "eq"
        if c == "!":  return "bang"
        return "otro"

    def transicion(self, estado: str, simbolo: str) -> str:
        cat = self._clasificar(simbolo)
        delta = {
            "q0":     {"lt": "q1_lt",  "gt": "q1_gt",  "eq": "q1_eq",   "bang": "q1_bang", "otro": "q_err"},
            "q1_lt":  {"lt": "q_err",  "gt": "q_err",  "eq": "q2_leq",  "bang": "q_err",   "otro": "q_err"},
            "q1_gt":  {"lt": "q_err",  "gt": "q_err",  "eq": "q2_geq",  "bang": "q_err",   "otro": "q_err"},
            "q1_eq":  {"lt": "q_err",  "gt": "q_err",  "eq": "q2_eqeq", "bang": "q_err",   "otro": "q_err"},
            "q1_bang":{"lt": "q_err",  "gt": "q_err",  "eq": "q2_neq",  "bang": "q_err",   "otro": "q_err"},
            "q2_leq": {"lt": "q_err",  "gt": "q_err",  "eq": "q_err",   "bang": "q_err",   "otro": "q_err"},
            "q2_geq": {"lt": "q_err",  "gt": "q_err",  "eq": "q_err",   "bang": "q_err",   "otro": "q_err"},
            "q2_eqeq":{"lt": "q_err",  "gt": "q_err",  "eq": "q_err",   "bang": "q_err",   "otro": "q_err"},
            "q2_neq": {"lt": "q_err",  "gt": "q_err",  "eq": "q_err",   "bang": "q_err",   "otro": "q_err"},
            "q_err":  {"lt": "q_err",  "gt": "q_err",  "eq": "q_err",   "bang": "q_err",   "otro": "q_err"},
        }
        return delta.get(estado, {}).get(cat, "q_err")

    def acepta(self, cadena: str) -> bool:
        estado = self.ESTADO_INICIAL
        for c in cadena:
            estado = self.transicion(estado, c)
        return estado in self.ESTADOS_ACEPTACION


# =============================================================================
# AFD 5 — OPERADORES ARITMÉTICOS: + - * / %
# Q  = {q0, q1, q_err}
# F  = {q1}
# =============================================================================

class AFD_OperadorAritmetico:
    ESTADO_INICIAL = "q0"
    ESTADOS_ACEPTACION = {"q1"}
    OPERADORES = set("+-*/%")

    def transicion(self, estado: str, simbolo: str) -> str:
        delta = {
            "q0":    {True: "q1",    False: "q_err"},
            "q1":    {True: "q_err", False: "q_err"},
            "q_err": {True: "q_err", False: "q_err"},
        }
        return delta[estado][simbolo in self.OPERADORES]

    def acepta(self, cadena: str) -> bool:
        estado = self.ESTADO_INICIAL
        for c in cadena:
            estado = self.transicion(estado, c)
        return estado in self.ESTADOS_ACEPTACION


# =============================================================================
# Palabras reservadas del lenguaje ficticio
# =============================================================================

PALABRAS_RESERVADAS = {
    "si", "sino", "mientras", "retornar", "fin",
    "entero", "decimal", "texto", "booleano", "verdadero", "falso"
}

SIMBOLOS = set("(){}=;,")

COLORES_TOKEN = {
    TokenType.PALABRA_RESERVADA.value:    "#3B82F6",   # azul
    TokenType.IDENTIFICADOR.value:        "#10B981",   # verde
    TokenType.NUMERO.value:               "#F59E0B",   # amarillo
    TokenType.OPERADOR_LOGICO.value:      "#8B5CF6",   # violeta
    TokenType.OPERADOR_RELACIONAL.value:  "#EC4899",   # rosa
    TokenType.OPERADOR_ARITMETICO.value:  "#FB923C",   # naranja
    TokenType.SIMBOLO.value:              "#6B7280",   # gris
    TokenType.INVALIDO.value:             "#DC2626",   # rojo oscuro
}
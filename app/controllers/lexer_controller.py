# =============================================================================
# CONTROLLER — Lógica de negocio del analizador léxico + rutas Flask
# Responsabilidad: coordinar Modelos → procesar entrada → llamar Vista
# =============================================================================

from flask import Blueprint, request, jsonify, render_template
from app.models import (
    AFD_Identificador, AFD_Numero, AFD_OperadorLogico,
    AFD_OperadorRelacional, AFD_OperadorAritmetico,
    Token, TokenType, PALABRAS_RESERVADAS, SIMBOLOS,
)
from app.views import LexerView

lexer_bp = Blueprint("lexer", __name__)

# ---------------------------------------------------------------------------
# Servicio interno: motor del analizador léxico
# ---------------------------------------------------------------------------

class LexerService:
    """
    Implementa el análisis léxico usando los AFD del modelo.
    Aplica el principio Maximal Munch: consume el lexema más largo posible.
    """

    def __init__(self):
        self._afd_id   = AFD_Identificador()
        self._afd_num  = AFD_Numero()
        self._afd_log  = AFD_OperadorLogico()
        self._afd_rel  = AFD_OperadorRelacional()
        self._afd_arit = AFD_OperadorAritmetico()

    # ------------------------------------------------------------------
    # Clasificación de un lexema ya extraído
    # ------------------------------------------------------------------

    def _clasificar_lexema(self, lexema: str) -> TokenType:
        if self._afd_id.acepta(lexema):
            if lexema in PALABRAS_RESERVADAS:
                return TokenType.PALABRA_RESERVADA
            return TokenType.IDENTIFICADOR
        if self._afd_num.acepta(lexema):
            return TokenType.NUMERO
        if self._afd_log.acepta(lexema):
            return TokenType.OPERADOR_LOGICO
        if self._afd_rel.acepta(lexema):
            return TokenType.OPERADOR_RELACIONAL
        if self._afd_arit.acepta(lexema):
            return TokenType.OPERADOR_ARITMETICO
        if len(lexema) == 1 and lexema in SIMBOLOS:
            return TokenType.SIMBOLO
        return TokenType.INVALIDO

    # ------------------------------------------------------------------
    # Maximal Munch: extrae el lexema más largo posible desde pos
    # ------------------------------------------------------------------

    def _siguiente_token(self, codigo: str, pos: int, linea: int, col: int) -> tuple:
        """
        Retorna (Token, nueva_pos, nueva_linea, nueva_col) usando Maximal Munch.
        """
        c = codigo[pos]

        # Espacios y saltos de línea (ignorar)
        if c == "\n":
            return None, pos + 1, linea + 1, 1
        if c in " \t\r":
            return None, pos + 1, linea, col + 1

        # ---- Intento 1: Identificadores / palabras reservadas --------
        # Estado inicial q0 del AFD_Identificador acepta letra o _
        if c.isalpha() or c == "_":
            fin = pos
            estado = self._afd_id.ESTADO_INICIAL
            while fin < len(codigo):
                sig = self._afd_id.transicion(estado, codigo[fin])
                if sig == "q_err":
                    break
                estado = sig
                fin += 1
            lexema = codigo[pos:fin]
            tipo = TokenType.PALABRA_RESERVADA if lexema in PALABRAS_RESERVADAS else TokenType.IDENTIFICADOR
            return Token(tipo, lexema, linea, col), fin, linea, col + (fin - pos)

        # ---- Intento 2: Números -------------------------------------
        if c.isdigit():
            fin = pos
            estado = self._afd_num.ESTADO_INICIAL
            ultimo_aceptado = -1
            while fin < len(codigo):
                sig = self._afd_num.transicion(estado, codigo[fin])
                if sig == "q_err":
                    break
                estado = sig
                fin += 1
                if estado in self._afd_num.ESTADOS_ACEPTACION:
                    ultimo_aceptado = fin
            if ultimo_aceptado > pos:
                lexema = codigo[pos:ultimo_aceptado]
                return Token(TokenType.NUMERO, lexema, linea, col), ultimo_aceptado, linea, col + (ultimo_aceptado - pos)
            # Si no se aceptó nada, marcar como inválido
            return Token(TokenType.INVALIDO, c, linea, col), pos + 1, linea, col + 1

        # ---- Intento 3: Operadores relacionales (dos caracteres) ----
        if c in "<>!=":
            dos = codigo[pos:pos+2]
            if self._afd_rel.acepta(dos):
                return Token(TokenType.OPERADOR_RELACIONAL, dos, linea, col), pos + 2, linea, col + 2
            uno = codigo[pos:pos+1]
            if self._afd_rel.acepta(uno):
                return Token(TokenType.OPERADOR_RELACIONAL, uno, linea, col), pos + 1, linea, col + 1
            # '!' solo sin '=' también puede ser operador lógico
            if c == "!" and not (pos + 1 < len(codigo) and codigo[pos+1] == "="):
                return Token(TokenType.OPERADOR_LOGICO, "!", linea, col), pos + 1, linea, col + 1
            return Token(TokenType.INVALIDO, c, linea, col), pos + 1, linea, col + 1

        # ---- Intento 4: Operadores lógicos (&& ||) ------------------
        if c in "&|":
            dos = codigo[pos:pos+2]
            if self._afd_log.acepta(dos):
                return Token(TokenType.OPERADOR_LOGICO, dos, linea, col), pos + 2, linea, col + 2
            return Token(TokenType.INVALIDO, c, linea, col), pos + 1, linea, col + 1

        # ---- Intento 5: Operadores aritméticos ----------------------
        if c in "+-*/%":
            return Token(TokenType.OPERADOR_ARITMETICO, c, linea, col), pos + 1, linea, col + 1

        # ---- Intento 6: Símbolos ------------------------------------
        if c in SIMBOLOS:
            return Token(TokenType.SIMBOLO, c, linea, col), pos + 1, linea, col + 1

        # ---- Desconocido --------------------------------------------
        return Token(TokenType.INVALIDO, c, linea, col), pos + 1, linea, col + 1

    # ------------------------------------------------------------------
    # Punto de entrada principal
    # ------------------------------------------------------------------

    def analizar(self, codigo: str) -> list[Token]:
        """
        Recorre el codigo fuente y retorna la lista de tokens encontrados.
        """
        tokens = []
        pos    = 0
        linea  = 1
        col    = 1
        n      = len(codigo)

        while pos < n:
            token, pos, linea, col = self._siguiente_token(codigo, pos, linea, col)
            if token is not None:
                tokens.append(token)

        return tokens


# ---------------------------------------------------------------------------
# Instancias compartidas (inyección de dependencias manual)
# ---------------------------------------------------------------------------
_servicio = LexerService()
_vista     = LexerView()


# ---------------------------------------------------------------------------
# Rutas Flask
# ---------------------------------------------------------------------------

@lexer_bp.route("/", methods=["GET"])
def index():
    """Página principal con el editor de código."""
    return render_template("index.html")


@lexer_bp.route("/analizar", methods=["POST"])
def analizar():
    """
    Endpoint principal.
    Acepta JSON { "codigo": "..." } o multipart/form-data con campo 'codigo'.
    Retorna JSON con tokens, HTML coloreado, tabla y estadísticas.
    """
    # Obtener el código fuente
    if request.is_json:
        data   = request.get_json(silent=True) or {}
        codigo = data.get("codigo", "")
    else:
        codigo = request.form.get("codigo", "")

    if not codigo.strip():
        return jsonify({"error": "El campo 'codigo' está vacío."}), 400

    # ---- Controller: delega al servicio (modelo) ----
    tokens = _servicio.analizar(codigo)

    # ---- View: genera las representaciones ----
    html_coloreado = _vista.render_tokens_html(tokens)
    tabla_html     = _vista.render_tabla_tokens(tokens)
    estadisticas   = _vista.render_estadisticas(tokens)

    return jsonify({
        "tokens":         [t.to_dict() for t in tokens],
        "html_coloreado": html_coloreado,
        "tabla_html":     tabla_html,
        "estadisticas":   estadisticas,
    })


@lexer_bp.route("/analizar/archivo", methods=["POST"])
def analizar_archivo():
    """
    Endpoint para subir un archivo .txt con código fuente.
    """
    if "archivo" not in request.files:
        return jsonify({"error": "No se encontró el campo 'archivo'."}), 400

    archivo = request.files["archivo"]

    if archivo.filename == "":
        return jsonify({"error": "No se seleccionó ningún archivo."}), 400

    if not archivo.filename.endswith(".txt"):
        return jsonify({"error": "Solo se aceptan archivos .txt"}), 400

    try:
        codigo = archivo.read().decode("utf-8")
    except UnicodeDecodeError:
        return jsonify({"error": "El archivo no tiene codificación UTF-8."}), 400

    tokens         = _servicio.analizar(codigo)
    html_coloreado = _vista.render_tokens_html(tokens)
    tabla_html     = _vista.render_tabla_tokens(tokens)
    estadisticas   = _vista.render_estadisticas(tokens)

    return jsonify({
        "archivo":        archivo.filename,
        "tokens":         [t.to_dict() for t in tokens],
        "html_coloreado": html_coloreado,
        "tabla_html":     tabla_html,
        "estadisticas":   estadisticas,
    })
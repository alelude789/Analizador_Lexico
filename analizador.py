import re
import html

# ============================
# ANALIZADOR LEXICO SIMPLE
# Lenguaje ficticio
# ============================

PALABRAS_RESERVADAS = {
    "si", "sino", "mientras", "retornar", "entero", "decimal", "texto", "booleano", "verdadero", "falso"
}

OPERADORES_LOGICOS = {"&&", "||", "!"}
OPERADORES_ARITMETICOS = {"+", "-", "*", "/", "%"}
OPERADORES_RELACIONALES = {"==", "!=", "<", ">", "<=", ">="}
SIMBOLOS = {"(", ")", "{", "}", ";", ",", "="}


def es_identificador(token):
    """
    Reconoce identificadores:
    - Debe iniciar con letra o _
    - Luego puede tener letras, numeros o _
    Ejemplos validos: x, suma1, _valor
    """
    if not token:
        return False

    if not (token[0].isalpha() or token[0] == "_"):
        return False

    for c in token[1:]:
        if not (c.isalnum() or c == "_"):
            return False

    return True


def es_numero_decimal(token):
    """
    Reconoce numeros enteros y decimales:
    - 10
    - 25.5
    - 0.75
    """
    return re.fullmatch(r"\d+(\.\d+)?", token) is not None


def clasificar_token(token):
    if token in PALABRAS_RESERVADAS:
        return "PALABRA_RESERVADA"

    if es_numero_decimal(token):
        return "NUMERO"

    if token in OPERADORES_LOGICOS:
        return "OPERADOR_LOGICO"

    if token in OPERADORES_ARITMETICOS:
        return "OPERADOR_ARITMETICO"

    if token in OPERADORES_RELACIONALES:
        return "OPERADOR_RELACIONAL"

    if token in SIMBOLOS:
        return "SIMBOLO"

    if es_identificador(token):
        return "IDENTIFICADOR"

    return "INVALIDO"


def dividir_tokens(texto):
    """
    Separa el codigo fuente en tokens.
    Primero reconoce operadores de dos caracteres como &&, ||, ==, !=, <=, >=.
    Luego reconoce palabras, numeros decimales y simbolos individuales.
    """
    patron = r"&&|\|\||==|!=|<=|>=|\d+\.\d+|\d+|[A-Za-z_][A-Za-z0-9_]*|[+\-*/%(){};,=<>!]|\S"
    return re.findall(patron, texto)


def analizar_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    tokens = dividir_tokens(texto)
    resultado = []

    for token in tokens:
        tipo = clasificar_token(token)
        resultado.append((token, tipo))

    return resultado, texto


def generar_html(resultado, salida="salida.html"):
    colores = {
        "PALABRA_RESERVADA": "#6f42c1",
        "IDENTIFICADOR": "#0d6efd",
        "NUMERO": "#198754",
        "OPERADOR_LOGICO": "#fd7e14",
        "OPERADOR_ARITMETICO": "#20c997",
        "OPERADOR_RELACIONAL": "#d63384",
        "SIMBOLO": "#6c757d",
        "INVALIDO": "#dc3545"
    }

    html_tokens = ""

    for token, tipo in resultado:
        color = colores.get(tipo, "#000")
        clase = "token invalido" if tipo == "INVALIDO" else "token"
        html_tokens += f'<span class="{clase}" style="background:{color};">{html.escape(token)}</span> '

    contenido = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultado del Analizador Lexico</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            padding: 30px;
        }}

        h1 {{
            color: #222;
        }}

        .contenedor {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 8px rgba(0,0,0,0.15);
            line-height: 2.3;
        }}

        .token {{
            color: white;
            padding: 6px 10px;
            border-radius: 6px;
            font-weight: bold;
            display: inline-block;
        }}

        .invalido {{
            border: 2px solid black;
        }}

        .leyenda {{
            margin-top: 25px;
            background: white;
            padding: 15px;
            border-radius: 10px;
        }}

        .item {{
            margin: 6px 0;
        }}

        .cuadro {{
            display: inline-block;
            width: 18px;
            height: 18px;
            margin-right: 8px;
            vertical-align: middle;
        }}
    </style>
</head>
<body>
    <h1>Resultado del Analizador Lexico</h1>

    <div class="contenedor">
        {html_tokens}
    </div>

    <div class="leyenda">
        <h2>Leyenda</h2>
        {''.join(f'<div class="item"><span class="cuadro" style="background:{color};"></span>{tipo}</div>' for tipo, color in colores.items())}
    </div>
</body>
</html>"""

    with open(salida, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)


def mostrar_en_consola(resultado):
    colores_terminal = {
        "PALABRA_RESERVADA": "\033[95m",
        "IDENTIFICADOR": "\033[94m",
        "NUMERO": "\033[92m",
        "OPERADOR_LOGICO": "\033[93m",
        "OPERADOR_ARITMETICO": "\033[96m",
        "OPERADOR_RELACIONAL": "\033[91m",
        "SIMBOLO": "\033[90m",
        "INVALIDO": "\033[41m"
    }

    reset = "\033[0m"

    for token, tipo in resultado:
        color = colores_terminal.get(tipo, "")
        print(f"{color}{token}{reset}", end=" ")

    print("\n")


if __name__ == "__main__":
    archivo_entrada = "codigo.txt"

    resultado, texto_original = analizar_archivo(archivo_entrada)

    print("\nCODIGO ANALIZADO:\n")
    print(texto_original)

    print("\nTOKENS COLOREADOS EN CONSOLA:\n")
    mostrar_en_consola(resultado)

    print("TABLA DE TOKENS:\n")
    for token, tipo in resultado:
        print(f"{token:15} -> {tipo}")

    generar_html(resultado, "salida.html")
    print("\nArchivo salida.html generado correctamente.")

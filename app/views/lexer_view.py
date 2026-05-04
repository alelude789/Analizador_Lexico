# =============================================================================
# VIEW — Generación de HTML coloreado por tipo de token
# Responsabilidad: transformar la lista de Token en representación visual
# =============================================================================

from app.models import Token, TokenType, COLORES_TOKEN


class LexerView:
    """
    Genera la salida HTML con tokens coloreados por categoría.
    Esta clase solo se encarga de la presentación, no de la lógica de negocio.
    """

    # Etiquetas badge para cada tipo de token
    BADGE_CLASSES = {
        TokenType.PALABRA_RESERVADA.value:    "badge-reservada",
        TokenType.IDENTIFICADOR.value:        "badge-identificador",
        TokenType.NUMERO.value:               "badge-numero",
        TokenType.OPERADOR_LOGICO.value:      "badge-logico",
        TokenType.OPERADOR_RELACIONAL.value:  "badge-relacional",
        TokenType.OPERADOR_ARITMETICO.value:  "badge-aritmetico",
        TokenType.SIMBOLO.value:              "badge-simbolo",
        TokenType.INVALIDO.value:             "badge-invalido",
    }

    def render_tokens_html(self, tokens: list[Token]) -> str:
        """
        Genera fragmento HTML con cada token envuelto en un <span> coloreado.
        """
        if not tokens:
            return "<p class='text-gray-400 italic'>No se encontraron tokens.</p>"

        partes = []
        linea_actual = 1

        for token in tokens:
            # Salto de línea si cambia la línea
            while linea_actual < token.linea:
                partes.append("<br>")
                linea_actual += 1

            clase = self.BADGE_CLASSES.get(token.tipo.value, "badge-invalido")
            lexema_escaped = (
                token.lexema
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            partes.append(
                f'<span class="token {clase}" '
                f'title="{token.tipo.value} | L{token.linea}:C{token.columna}">'
                f'{lexema_escaped}</span>'
            )

        return " ".join(partes)

    def render_tabla_tokens(self, tokens: list[Token]) -> str:
        """
        Genera una tabla HTML con el detalle de todos los tokens.
        """
        if not tokens:
            return ""

        filas = []
        for i, t in enumerate(tokens, start=1):
            clase = self.BADGE_CLASSES.get(t.tipo.value, "badge-invalido")
            lexema_escaped = t.lexema.replace("<", "&lt;").replace(">", "&gt;")
            filas.append(
                f"<tr>"
                f"<td class='td-num'>{i}</td>"
                f"<td><span class='token {clase}'>{lexema_escaped}</span></td>"
                f"<td class='td-tipo'>{t.tipo.value}</td>"
                f"<td class='td-pos'>L{t.linea}:C{t.columna}</td>"
                f"</tr>"
            )

        filas_html = "\n".join(filas)
        return f"""
        <table class="token-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Lexema</th>
              <th>Tipo</th>
              <th>Posición</th>
            </tr>
          </thead>
          <tbody>
            {filas_html}
          </tbody>
        </table>
        """

    def render_estadisticas(self, tokens: list[Token]) -> dict:
        """
        Calcula estadísticas del análisis para mostrar en la vista.
        """
        from collections import Counter
        conteo = Counter(t.tipo.value for t in tokens)
        invalidos = conteo.get(TokenType.INVALIDO.value, 0)
        return {
            "total": len(tokens),
            "invalidos": invalidos,
            "validos": len(tokens) - invalidos,
            "por_tipo": dict(conteo),
            "colores": COLORES_TOKEN,
        }
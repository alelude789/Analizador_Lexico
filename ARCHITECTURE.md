# Documentación Técnica - Arquitectura del Proyecto

## 📐 Estructura del Análisis Léxico

```
CÓDIGO FUENTE
    ↓
SCANNER (main.js via AJAX)
    ↓
LexerService._siguiente_token()
    ├─ Saltar espacios/saltos de línea
    ├─ Maximal Munch → AFD_Identificador
    ├─ Maximal Munch → AFD_Numero
    ├─ Maximal Munch → AFD_OperadorLogico
    ├─ Maximal Munch → AFD_OperadorRelacional
    ├─ Maximal Munch → AFD_OperadorAritmetico
    ├─ Clasificar símbolo
    └─ Crear Token
    ↓
LISTA DE TOKENS
    ↓
LexerView.render_tokens_html()
    ├─ HTML coloreado
    ├─ Tabla de tokens
    └─ Estadísticas
    ↓
JSON Response → Frontend
    ↓
RESULTADO VISUAL
```

## 🔄 Flujo de Petición HTTP

```
1. Cliente (JavaScript)
   └─ Envía JSON con código → POST /analizar

2. Servidor Flask
   ├─ LexerService.analizar()
   │  └─ Genera lista de tokens
   ├─ LexerView.render_tokens_html()
   │  └─ Genera HTML coloreado
   ├─ LexerView.render_tabla_tokens()
   │  └─ Genera tabla HTML
   └─ LexerView.render_estadisticas()
      └─ Calcula estadísticas

3. Servidor Retorna JSON
   ├─ tokens: []
   ├─ html_coloreado: "<span>...</span>"
   ├─ tabla_html: "<table>...</table>"
   └─ estadisticas: {...}

4. Cliente (JavaScript)
   ├─ Actualiza DOM con HTML coloreado
   ├─ Inserta tabla
   ├─ Muestra estadísticas
   └─ Actualiza interfaz visual
```

## 🤖 Máquina de Estados - AFD Identificador

```
        letra, _
    ─────────────→
    │             │
    q0 ← ✓ ✗ q1 ← letra, _, dígito
    │             │
    └─────────────┘
      (otro)

Ejemplo de análisis: "variable123"

v → q0 --(v es letra)--> q1
a → q1 --(a es letra)--> q1
r → q1 --(r es letra)--> q1
i → q1 --(i es letra)--> q1
a → q1 --(a es letra)--> q1
b → q1 --(b es letra)--> q1
l → q1 --(l es letra)--> q1
e → q1 --(e es letra)--> q1
1 → q1 --(1 es dígito)--> q1
2 → q1 --(2 es dígito)--> q1
3 → q1 --(3 es dígito)--> q1

✓ Estado final en q1 (aceptado)
```

## 🔀 Máquina de Estados - AFD Número

```
     dígito            dígito
   ─────────→ q1 ─────────→ q3
   │         /│\    .      /│\
   │        / │ \   dígito  │
   q0 ← ✓  /  │  ────────── 
         dígito

Ejemplos:
- "42" → q0 -2-> q1 -2-> q1 ✓
- "3.14" → q0 -3-> q1 -.- q2 -1-> q3 -4-> q3 ✓
- "5." → q0 -5-> q1 -.- q2 (sin dígito) ✗
```

## 📊 Estructura de Datos - Token

```python
class Token:
    tipo: TokenType      # Enum del tipo de token
    lexema: str         # Texto del token (ej: "variable", "42")
    linea: int          # Número de línea
    columna: int        # Número de columna

Ejemplo:
Token(
    tipo=TokenType.IDENTIFICADOR,
    lexema="x",
    linea=1,
    columna=5
)
```

## 🎨 Mapa de Colores

```python
COLORES_TOKEN = {
    "PALABRA_RESERVADA":    "#3B82F6",   # Azul (RGB: 59, 130, 246)
    "IDENTIFICADOR":        "#10B981",   # Verde (RGB: 16, 185, 129)
    "NUMERO":               "#F59E0B",   # Amarillo (RGB: 245, 158, 11)
    "OPERADOR_LOGICO":      "#8B5CF6",   # Violeta (RGB: 139, 92, 246)
    "OPERADOR_RELACIONAL":  "#EC4899",   # Rosa (RGB: 236, 72, 153)
    "OPERADOR_ARITMETICO":  "#FB923C",   # Naranja (RGB: 251, 146, 60)
    "SIMBOLO":              "#6B7280",   # Gris (RGB: 107, 114, 128)
    "INVALIDO":             "#DC2626",   # Rojo (RGB: 220, 38, 38)
}
```

## 🧮 Algoritmo Maximal Munch - Pseudocódigo

```
Función SiguienteToken(código, posición):
    
    // Intentar cada tipo de token en orden
    
    // 1. Identificadores
    si (código[pos] es letra o _):
        estado ← q0
        fin ← pos
        
        mientras (fin < longitud(código)):
            siguiente_estado ← transición(estado, código[fin])
            si (siguiente_estado es error):
                romper
            fin ← fin + 1
            si (siguiente_estado es aceptación):
                último_válido ← fin
        
        lexema ← código[pos:último_válido]
        retornar Token(IDENTIFICADOR, lexema, línea, col)
    
    // 2. Números (similar a identificadores)
    // 3. Operadores
    // 4. Símbolos
    // ...
    
    // Si nada coincide: token inválido
    retornar Token(INVALIDO, código[pos], línea, col)
```

## 📡 API REST Endpoints

### GET `/`
- **Descripción:** Obtiene página HTML principal
- **Respuesta:** HTML (text/html)
- **Estado:** 200 OK

### POST `/analizar`
- **Descripción:** Analiza código JSON
- **Request Body:**
  ```json
  {
    "codigo": "string"
  }
  ```
- **Respuesta:** JSON
  ```json
  {
    "tokens": [{"tipo": "string", "lexema": "string", "linea": 0, "columna": 0}],
    "html_coloreado": "string",
    "tabla_html": "string",
    "estadisticas": {
      "total": 0,
      "validos": 0,
      "invalidos": 0,
      "por_tipo": {},
      "colores": {}
    }
  }
  ```
- **Estado:** 200 OK o 400 Bad Request
- **Errors:**
  - 400: Código vacío

### POST `/analizar/archivo`
- **Descripción:** Analiza archivo .txt
- **Request:** multipart/form-data
  - `archivo`: File (text/plain)
- **Respuesta:** JSON (igual a `/analizar` + campo `archivo`)
- **Estado:** 200 OK o 400 Bad Request
- **Errors:**
  - 400: No existe campo archivo
  - 400: Archivo vacío
  - 400: No es .txt
  - 400: No es UTF-8

## 🔧 Extensibilidad

### Agregar Nuevo Tipo de Token

1. **Modelo** (`app/models/afd.py`):
```python
class AFD_MiTipo:
    ESTADO_INICIAL = "q0"
    ESTADOS_ACEPTACION = {"q1"}
    
    def transicion(self, estado, simbolo):
        # Implementar tabla de transición
        pass
    
    def acepta(self, cadena):
        # Validar si cadena es aceptada
        pass
```

2. **Enum** (`app/models/afd.py`):
```python
class TokenType(Enum):
    MI_TIPO = "MI_TIPO"
```

3. **Controller** (`app/controllers/lexer_controller.py`):
```python
if c.matches_mi_tipo():
    dos = codigo[pos:pos+2]
    if self._afd_mitipo.acepta(dos):
        return Token(TokenType.MI_TIPO, dos, linea, col), pos + 2, ...
```

4. **Color** (`app/models/afd.py`):
```python
COLORES_TOKEN = {
    ...
    TokenType.MI_TIPO.value: "#XXXXXX",
}
```

5. **CSS** (`app/static/css/style.css`):
```css
.badge-mitipo { background: #XXXXXX; color: var(--c-mitipo); border: 1px solid var(--c-mitipo); }
```

## 🧪 Testing

### Unit Test - AFD Identificador

```python
import unittest
from app.models import AFD_Identificador, TokenType

class TestAFDIdentificador(unittest.TestCase):
    def setUp(self):
        self.afd = AFD_Identificador()
    
    def test_identificador_simple(self):
        self.assertTrue(self.afd.acepta("variable"))
    
    def test_identificador_con_underscore(self):
        self.assertTrue(self.afd.acepta("_nombre"))
    
    def test_identificador_con_numeros(self):
        self.assertTrue(self.afd.acepta("var123"))
    
    def test_identificador_incorrecto_comienza_con_numero(self):
        self.assertFalse(self.afd.acepta("123var"))
    
    def test_identificador_vacio(self):
        self.assertFalse(self.afd.acepta(""))
```

### Integration Test - Análisis Completo

```python
def test_analisis_completo():
    from app import create_app
    
    app = create_app()
    client = app.test_client()
    
    response = client.post('/analizar', json={
        'codigo': 'entero x = 10;'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tokens']) == 5
    assert data['estadisticas']['validos'] == 5
    assert data['estadisticas']['invalidos'] == 0
```

## 📈 Rendimiento

### Complejidad Temporal

- **Análisis léxico:** O(n) donde n = longitud del código
- **Cada transición AFD:** O(1)
- **Generación HTML:** O(m) donde m = número de tokens

**Rendimiento típico:**
- 1000 líneas de código: < 100ms
- 10000 líneas de código: < 1s

## 🔐 Seguridad

### Consideraciones

1. **Validación de entrada:**
   - Máximo 1MB de código
   - Validación de UTF-8
   - Escapado de caracteres especiales

2. **Protección contra ataques:**
   - XSS: Escapado de HTML
   - CSRF: Tokens CSRF (configurar en producción)
   - Timeout: Límite de tiempo de análisis

3. **En Producción:**
   - HTTPS obligatorio
   - Headers de seguridad
   - Rate limiting
   - Logging de errores

## 📚 Referencias

- [Hopcroft, Motwani, Ullman] Autómatas Finitos
- [Aho, Lam, Sethi, Ullman] Compiladores: Principios, Técnicas y Herramientas
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)

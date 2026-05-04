# 🔬 Analizador Léxico con Arquitectura MVC

Un analizador léxico profesional basado en **Autómatas Finitos Deterministas (AFD)** implementado con arquitectura **MVC** usando **Flask**. Reconoce y clasifica tokens de un lenguaje ficticio con interfaz web moderna.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Autómatas Implementados](#autómatas-implementados)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Autores](#autores)

## ✨ Características

- ✅ **Análisis léxico en tiempo real** usando AJAX
- ✅ **5 Autómatas Finitos Deterministas** para diferentes tipos de tokens
- ✅ **Algoritmo Maximal Munch** para extracción de lexemas más largos
- ✅ **Interfaz web moderna** con estilos tipo consola oscura
- ✅ **Tokens coloreados** por categoría (palabras reservadas, números, operadores, etc.)
- ✅ **Tabla de tokens** con filtro de búsqueda
- ✅ **Estadísticas detalladas** por tipo de token
- ✅ **Upload de archivos `.txt`** para análisis
- ✅ **Ejemplo de código precargado** para pruebas rápidas
- ✅ **Responsive design** - adaptable a dispositivos móviles

## 🏗️ Arquitectura

El proyecto sigue el patrón **Model-View-Controller (MVC)**:

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/CSS/JS)              │
│              Interfaz de usuario - main.js             │
└──────────────────────────┬──────────────────────────────┘
                           │ AJAX
                           ▼
┌─────────────────────────────────────────────────────────┐
│              CONTROLLER (Flask Routes)                  │
│          lexer_controller.py - /analizar               │
│              Coordina Modelo ↔ Vista                    │
└──────────────────────────┬──────────────────────────────┘
                    ┌──────┴──────┐
                    ▼             ▼
        ┌──────────────────┐  ┌──────────────────┐
        │ MODEL            │  │ VIEW             │
        │ afd.py           │  │ lexer_view.py    │
        │ • 5 AFDs         │  │ • HTML Generator │
        │ • Token Class    │  │ • Estadísticas   │
        │ • Lógica léxica  │  │ • Tabla HTML     │
        └──────────────────┘  └──────────────────┘
```

### Componentes:

- **Model** (`app/models/afd.py`)
  - Implementación de 5 Autómatas Finitos Deterministas
  - Clase `Token` para representar tokens
  - Diccionarios de palabras reservadas y símbolos
  
- **Controller** (`app/controllers/lexer_controller.py`)
  - Clase `LexerService` con lógica del análisis léxico
  - Rutas Flask: `/` (GET), `/analizar` (POST), `/analizar/archivo` (POST)
  - Orquestación entre Modelo y Vista

- **View** (`app/views/lexer_view.py`)
  - Generación de HTML con tokens coloreados
  - Renderización de tabla de tokens
  - Cálculo de estadísticas

## 🤖 Autómatas Implementados

### 1. **AFD Identificadores**
```
Estados: {q0, q1, q_err}
Inicial: q0
Aceptación: {q1}

Reglas:
- q0 + (letra|_) → q1
- q1 + (letra|_|dígito) → q1

Ejemplos: variable, _nombre, contador123
```

### 2. **AFD Números**
```
Estados: {q0, q1, q2, q3, q_err}
Inicial: q0
Aceptación: {q1, q3}

Reglas:
- q0 + dígito → q1
- q1 + dígito → q1
- q1 + punto → q2
- q2 + dígito → q3
- q3 + dígito → q3

Ejemplos: 42, 3.14, 0, 100.5
```

### 3. **AFD Operadores Lógicos**
```
Estados: {q0, q1_amp, q2_and, q3_pipe, q4_or, q5_not, q_err}
Inicial: q0
Aceptación: {q2_and, q4_or, q5_not}

Soporta: &&, ||, !

Ejemplos: && || !
```

### 4. **AFD Operadores Relacionales**
```
Estados: {q0, q1_lt, q1_gt, q1_eq, q1_bang, q2_leq, q2_geq, q2_eqeq, q2_neq, q_err}
Inicial: q0
Aceptación: {q1_lt, q1_gt, q2_leq, q2_geq, q2_eqeq, q2_neq}

Soporta: ==, !=, <, >, <=, >=

Ejemplos: == != < > <= >=
```

### 5. **AFD Operadores Aritméticos**
```
Estados: {q0, q1, q_err}
Inicial: q0
Aceptación: {q1}

Soporta: +, -, *, /, %

Ejemplos: + - * / %
```

## 📦 Requisitos

- **Python 3.7+**
- **Flask 3.0.0**
- **Werkzeug 3.0.1**
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/lexer_mvc.git
cd lexer_mvc
```

### 2. Crear entorno virtual (Recomendado)

```bash
python -m venv venv
```

Activar el entorno:

**En Linux/macOS:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene:
```
Flask==3.0.0
Werkzeug==3.0.1
```

## ▶️ Ejecución

### Opción 1: Ejecución Normal

```bash
python main.py
```

### Opción 2: Con Variable de Entorno

```bash
FLASK_APP=main.py FLASK_ENV=development python -m flask run
```

### Resultado esperado:

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server...
 * Running on http://127.0.0.1:5000
 * Running on http://10.20.136.46:5000
Press CTRL+C to quit
```

Luego accede a:
```
http://localhost:5000
```

## 📖 Uso

### 1. **Interfaz Web**

Abre `http://localhost:5000` en tu navegador.

### 2. **Cargar Ejemplo**

Haz clic en el botón **"Ejemplo"** para cargar código de prueba predefinido.

### 3. **Escribir Código**

Escribe o pega código en el editor izquierdo. Ejemplo:

```
entero num = 10;
si (num > 5 && num < 20) {
  retornar verdadero;
}
```

### 4. **Analizar**

Haz clic en **"▶ Analizar"** para ejecutar el análisis léxico.

### 5. **Resultado**

Verás:
- ✅ **Tokens coloreados** en la sección derecha
- ✅ **Estadísticas** con conteo de tokens por tipo
- ✅ **Tabla de tokens** con detalles (lexema, tipo, línea, columna)

### 6. **Filtrar Tokens**

Usa el cuadro de búsqueda en la tabla para filtrar por lexema o tipo.

### 7. **Subir Archivo**

Haz clic en **"📂 Subir .txt"** para analizar un archivo de texto.

## 📁 Estructura del Proyecto

```
lexer_mvc/
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias
├── README.md                        # Este archivo
│
├── app/
│   ├── __init__.py                  # Factory Flask (create_app)
│   │
│   ├── models/
│   │   ├── __init__.py              # Exports de modelos
│   │   └── afd.py                   # AFDs y Token class
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── lexer_controller.py      # LexerService + rutas Flask
│   │
│   ├── views/
│   │   ├── __init__.py              # Exports de vistas
│   │   └── lexer_view.py            # LexerView - renderización HTML
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css            # Estilos - interfaz moderna
│   │   └── js/
│   │       └── main.js              # JavaScript - AJAX y eventos
│   │
│   └── templates/
│       └── index.html               # Plantilla HTML
│
└── tests/                           # Tests (opcional)
```

## 🎨 Clasificación de Tokens

Cada token se clasifica con un color distintivo:

| Token | Color | Ejemplo |
|-------|-------|---------|
| Palabra Reservada | 🔵 Azul | `si`, `retornar`, `entero` |
| Identificador | 🟢 Verde | `variable`, `contador` |
| Número | 🟡 Amarillo | `42`, `3.14` |
| Operador Lógico | 🟣 Violeta | `&&`, `\|\|`, `!` |
| Operador Relacional | 🩷 Rosa | `==`, `!=`, `<`, `>` |
| Operador Aritmético | 🟠 Naranja | `+`, `-`, `*`, `/`, `%` |
| Símbolo | ⚪ Gris | `(`, `)`, `{`, `}`, `;` |
| Inválido | 🔴 Rojo | Caracteres no reconocidos |

## 🔍 Ejemplo de Análisis

**Entrada:**
```
decimal x = 5.5;
si (x >= 10) {
  x = x * 2;
}
```

**Salida (Análisis):**
```
Token #1:  decimal       PALABRA_RESERVADA    L1:C1
Token #2:  x             IDENTIFICADOR        L1:C9
Token #3:  =             SIMBOLO              L1:C11
Token #4:  5.5           NUMERO               L1:C13
Token #5:  ;             SIMBOLO              L1:C17
Token #6:  si            PALABRA_RESERVADA    L2:C1
Token #7:  (             SIMBOLO              L2:C4
Token #8:  x             IDENTIFICADOR        L2:C5
Token #9:  >=            OPERADOR_RELACIONAL  L2:C7
Token #10: 10            NUMERO               L2:C10
Token #11: )             SIMBOLO              L2:C12
Token #12: {             SIMBOLO              L3:C1
Token #13: x             IDENTIFICADOR        L3:C3
Token #14: =             SIMBOLO              L3:C5
Token #15: x             IDENTIFICADOR        L3:C7
Token #16: *             OPERADOR_ARITMETICO  L3:C9
Token #17: 2             NUMERO               L3:C11
Token #18: ;             SIMBOLO              L3:C12
Token #19: }             SIMBOLO              L4:C1

Total: 19 tokens (19 válidos, 0 inválidos)
```

## 🌐 Endpoints API

### GET `/`
Retorna la página HTML principal.

**Respuesta:** HTML con interfaz

---

### POST `/analizar`
Analiza código fuente enviado por JSON.

**Request:**
```json
{
  "codigo": "entero x = 10;"
}
```

**Response:**
```json
{
  "tokens": [
    {
      "tipo": "PALABRA_RESERVADA",
      "lexema": "entero",
      "linea": 1,
      "columna": 1
    },
    {
      "tipo": "IDENTIFICADOR",
      "lexema": "x",
      "linea": 1,
      "columna": 9
    },
    ...
  ],
  "html_coloreado": "<span class='token badge-reservada' ...>entero</span>...",
  "tabla_html": "<table class='token-table'>...</table>",
  "estadisticas": {
    "total": 5,
    "validos": 5,
    "invalidos": 0,
    "por_tipo": {
      "PALABRA_RESERVADA": 1,
      "IDENTIFICADOR": 1,
      "NUMERO": 1,
      "SIMBOLO": 2
    },
    "colores": {...}
  }
}
```

---

### POST `/analizar/archivo`
Analiza un archivo `.txt` enviado como multipart/form-data.

**Request:** Multipart form con campo `archivo`

**Response:** JSON igual a `/analizar` + campo `archivo`

## 🛠️ Desarrollo

### Modificar Palabras Reservadas

En `app/models/afd.py`:
```python
PALABRAS_RESERVADAS = {
    "si", "sino", "mientras", "retornar", "fin",
    "entero", "decimal", "texto", "booleano", "verdadero", "falso"
}
```

### Agregar Nuevos Símbolos

En `app/models/afd.py`:
```python
SIMBOLOS = set("(){}=;,")
```

### Cambiar Colores

En `app/models/afd.py` y `app/static/css/style.css`:
```python
COLORES_TOKEN = {
    TokenType.PALABRA_RESERVADA.value: "#3B82F6",  # azul
    ...
}
```

## 📋 Algoritmo: Maximal Munch

El analizador implementa el principio **Maximal Munch** para extraer el lexema más largo posible:

```python
def _siguiente_token(self, codigo, pos, linea, col):
    """
    Intenta avanzar tanto como sea posible desde la posición actual
    siguiendo las transiciones del AFD correspondiente.
    """
    c = codigo[pos]
    
    # Ejemplo: números
    if c.isdigit():
        fin = pos
        estado = AFD_Numero.ESTADO_INICIAL
        ultimo_aceptado = -1
        
        while fin < len(codigo):
            sig = AFD_Numero.transicion(estado, codigo[fin])
            if sig == "q_err":
                break
            estado = sig
            fin += 1
            if estado in AFD_Numero.ESTADOS_ACEPTACION:
                ultimo_aceptado = fin  # Guarda posición válida
        
        # Retorna el lexema más largo válido
        return Token(TokenType.NUMERO, codigo[pos:ultimo_aceptado], ...)
```

Ventajas:
- ✅ Reconoce `3.14` como un número, no como `3`, `.`, `1`, `4`
- ✅ Identifica correctamente operadores como `==` vs `=`
- ✅ Maneja números decimales correctamente

## 🧪 Testing

Para agregar tests, crea archivos en la carpeta `tests/`:

```python
# tests/test_afd.py
from app.models import AFD_Identificador, AFD_Numero

def test_identificador():
    afd = AFD_Identificador()
    assert afd.acepta("variable") == True
    assert afd.acepta("_nombre") == True
    assert afd.acepta("123abc") == False

def test_numero():
    afd = AFD_Numero()
    assert afd.acepta("42") == True
    assert afd.acepta("3.14") == True
    assert afd.acepta("3.14.15") == False
```

Ejecutar con pytest:
```bash
pip install pytest
pytest tests/
```

## 🔒 Seguridad

⚠️ **Nota para Producción:**

El servidor Flask en modo debug no es seguro para producción. Para desplegar:

1. Usar un servidor WSGI como **Gunicorn**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

2. Configurar **HTTPS** con Let's Encrypt

3. Desactivar debug:
```python
app.run(debug=False)
```

## 📝 Lenguaje Ficticio - Especificación

### Palabras Reservadas
```
si, sino, mientras, retornar, fin
entero, decimal, texto, booleano
verdadero, falso
```

### Tipos de Datos
- `entero`: Números sin decimales
- `decimal`: Números con punto decimal
- `texto`: Cadenas de caracteres (futuro)
- `booleano`: `verdadero` o `falso`

### Operadores

**Aritméticos:** `+`, `-`, `*`, `/`, `%`

**Relacionales:** `==`, `!=`, `<`, `>`, `<=`, `>=`

**Lógicos:** `&&`, `||`, `!`

### Símbolos
```
( ) { } = ; ,
```

## 🚨 Limitaciones Actuales

- No reconoce comentarios (`//`, `/* */`)
- No soporta cadenas de texto entrecomilladas
- No valida sintaxis (solo análisis léxico)
- No genera código intermedio

Estas pueden ser mejoras futuras.

## 📚 Referencias

- **Teoría de Autómatas:** Sipser, M. (2012). *Introduction to the Theory of Computation*
- **Análisis Léxico:** Aho, A. V., et al. (2006). *Compilers: Principles, Techniques, and Tools*
- **Flask:** https://flask.palletsprojects.com/

## 📄 Licencia

Este proyecto está bajo licencia **MIT**. Ver archivo `LICENSE` para más detalles.

## 👥 Autores

- **Sebastian Narvaez**
- **Dilan Chamba**
- **Alexander Ludeña**
- **Boris Rengel**
- **Jose Encalada**

**Asignatura:** Teoría de la Computación  
**Institución:** [Tu Universidad]  
**Año:** 2026

## 📧 Contacto

Para preguntas o sugerencias, abre un **Issue** en el repositorio o contacta a los autores.

---

**Última actualización:** Mayos 2026  
**Versión:** 1.0.0

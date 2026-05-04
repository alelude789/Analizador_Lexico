# Analizador Lexico para Lenguaje Ficticio

## Objetivo

Este proyecto simula un analizador lexico. Lee un archivo de texto con codigo fuente y clasifica cada parte como token valido o invalido.

## Tokens reconocidos

1. Palabras reservadas:
   - si
   - sino
   - mientras
   - retornar
   - entero
   - decimal
   - texto
   - booleano
   - verdadero
   - falso

2. Identificadores:
   - Deben iniciar con letra o guion bajo
   - Luego pueden tener letras, numeros o guion bajo
   - Ejemplos: edad, promedio, variable1, _dato

3. Numeros:
   - Enteros: 10, 25, 100
   - Decimales: 9.5, 7.0, 10.25

4. Operadores logicos:
   - &&
   - ||
   - !

5. Operadores relacionales:
   - ==
   - !=
   - <
   - >
   - <=
   - >=

6. Operadores aritmeticos:
   - +
   - -
   - *
   - /
   - %

7. Simbolos:
   - (
   - )
   - {
   - }
   - ;
   - ,
   - =

## Como ejecutar

En la terminal:

```bash
python3 analizador.py
```

El programa lee el archivo:

```bash
codigo.txt
```

Luego genera:

```bash
salida.html
```

Abre salida.html en el navegador para ver los tokens pintados de colores.

## Relacion con JFLAP

Para la entrega en JFLAP se deben crear AFN separados:

1. AFN para identificadores
2. AFN para numeros enteros y decimales
3. AFN para palabras reservadas
4. AFN para operadores logicos
5. AFN para operadores relacionales
6. AFN para operadores aritmeticos
7. AFN para simbolos

Despues en JFLAP:

1. Crear el AFN
2. Ir a Convert
3. Convertir a DFA
4. Minimizar el DFA
5. Probar cadenas validas e invalidas

## Ejemplos de prueba

Valido:

```txt
entero edad = 20;
si (edad >= 18 && edad < 25) {
    retornar verdadero;
}
```

Invalido:

```txt
@error
```

El simbolo @ sera marcado como INVALIDO.

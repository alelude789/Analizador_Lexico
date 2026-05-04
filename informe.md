# Informe corto del proyecto

## Tema

Analizadores lexicos para un lenguaje propio usando automatas finitos.

## Problema

Se necesita reconocer los tokens principales de un lenguaje de programacion ficticio. Para esto se disenaron automatas finitos no deterministas, luego se convirtieron a automatas finitos deterministas y finalmente se implemento una simulacion en Python.

## Tokens definidos

El lenguaje reconoce palabras reservadas, identificadores, numeros enteros, numeros decimales, operadores logicos, operadores relacionales, operadores aritmeticos y simbolos especiales.

## Diseno de automatas

### Identificadores

Un identificador inicia con una letra o guion bajo. Luego puede tener letras, numeros o guion bajo.

Expresion regular:

```txt
(letra | _) (letra | digito | _)*
```

### Numeros

Un numero puede ser entero o decimal.

Expresion regular:

```txt
digito+ (. digito+)?
```

### Operadores logicos

Se reconocen:

```txt
&&
||
!
```

### Operadores relacionales

Se reconocen:

```txt
==
!=
<
>
<=
>=
```

## Implementacion en Python

El programa lee el archivo codigo.txt, separa el texto en tokens, clasifica cada token y genera una pagina HTML llamada salida.html donde los tokens validos se muestran con colores y los tokens invalidos aparecen en rojo.

## Conclusion

El proyecto demuestra como los automatas finitos pueden utilizarse para construir la primera etapa de un compilador: el analisis lexico.

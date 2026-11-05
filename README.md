# Mapa de Linaje de Datos

> Generador automático de mapas interactivos de linaje de datos a partir de scripts SQL.

**[Ver demo interactiva](https://lunajesusalfonso-gif.github.io/Portafolio/)** · construida con scripts SQL de ejemplo ficticios ([sql_ejemplo/](sql_ejemplo)).

## Descripción

Herramienta en Python que lee una carpeta de scripts SQL, identifica de qué tablas se alimenta cada uno y los conecta con el macro proceso al que pertenecen y los reportes (libros de trabajo) donde terminan. El resultado es un grafo interactivo en HTML que se regenera cada vez que se ejecuta el script.

## Problema

En equipos de BI es común que nadie sepa con certeza qué reportes se rompen si cambia una tabla, o de dónde sale realmente el dato de un tablero. Documentar ese linaje a mano es lento y se desactualiza rápido.

## Objetivos

- Hacer visible la cadena de dependencias **tabla → script → macro proceso → reporte**.
- Reducir el tiempo de análisis de impacto ante cambios en tablas fuente.
- Eliminar la documentación manual: el mapa se genera solo a partir del código.
- Permitir que perfiles no técnicos entiendan el flujo de los datos con una vista visual.

## Arquitectura de 4 niveles

| Nivel | Nodo | Forma | Cómo se obtiene |
|---|---|---|---|
| 1 | Tabla fuente | base de datos (morado) | Expresión regular sobre `FROM` / `JOIN` del SQL |
| 2 | Script SQL | círculo (cian) | Cada archivo `.sql` de la carpeta |
| 3 | Macro proceso | estrella (verde) | Reglas por palabra clave en el nombre del script |
| 4 | Libro de trabajo | cuadrado (naranja) | Diccionario macro proceso → reportes, o script → reportes |

## Características

- Extracción de tablas con `re`, normalizando esquemas, comillas y rutas.
- Grafo dirigido e interactivo con [pyvis](https://pyvis.readthedocs.io/) (zoom, arrastre, tooltips).
- Interfaz personalizada inyectada en el HTML: encabezado, contadores por nivel, leyenda y botones de control.
- HTML autocontenido, sin dependencias externas de JavaScript.
- Reglas de negocio configurables sin tocar la lógica (diccionarios al inicio de la función).

## Estructura del repositorio

```
├── mapa_linaje.py       # Script principal
├── sql_ejemplo/         # Scripts SQL ficticios para la demo
├── index.html           # Mapa generado (publicado con GitHub Pages)
├── requirements.txt     # Dependencias
└── README.md
```

## Uso

```bash
pip install -r requirements.txt
python mapa_linaje.py                      # usa la carpeta sql_ejemplo
python mapa_linaje.py ruta/a/mis_sql -o mapa.html
```

Abre el HTML resultante en cualquier navegador. Las reglas de negocio (`reglas_negocio`, `libros_de_trabajo`, `scripts_a_reportes`) se editan al inicio de `generar_mapa_multinivel`.

## Aprendizajes

- Parseo de SQL con expresiones regulares y sus límites (subconsultas, CTE, alias).
- Modelado de dependencias como un grafo dirigido por niveles.
- Generación y personalización de visualizaciones HTML desde Python.

## Mejoras futuras

- Parser SQL real (por ejemplo `sqlglot`) para detectar columnas y CTE.
- Leer reglas de negocio desde un archivo YAML/JSON en lugar de diccionarios en el código.
- Resaltar el impacto aguas abajo al seleccionar una tabla.

## Tecnologías

Python · pyvis / vis-network · expresiones regulares · HTML + CSS

## Autor

Jesús Alfonso Luna

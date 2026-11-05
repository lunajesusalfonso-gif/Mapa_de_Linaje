# Mapa de Linaje de Datos

Herramienta en Python que **lee scripts SQL y genera automáticamente un mapa interactivo de linaje de datos**: de qué tablas se alimenta cada script, a qué macro proceso pertenece y en qué libros de trabajo (reportes) termina.

![Tipos de nodo](Mapa%20de%20Linaje/Dataset.png)

## Qué problema resuelve

En equipos de BI es común que nadie sepa con certeza qué reportes se rompen si cambia una tabla. Este proyecto vuelve visible esa cadena de dependencias sin documentarla a mano: el mapa se regenera cada vez que se corre el script.

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
- Reglas de negocio configurables sin tocar la lógica (diccionarios al inicio de la función).

## Uso

```bash
pip install -r requirements.txt
python mapa_linaje.py
```

Edita la ruta de la carpeta con tus `.sql` al final de `mapa_linaje.py` (variable `mi_ruta`). El resultado se guarda como `mapa_multinivel.html`; ábrelo en cualquier navegador.

## Tecnologías

Python · pyvis / vis-network · expresiones regulares · HTML + CSS

## Autor

Jesús Alfonso Luna

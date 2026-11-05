import os
import re
from pyvis.network import Network

# =================================================================
# 1. EXTRACCIÓN Y LIMPIEZA DE NOMBRES
# =================================================================
def extraer_tablas_limpio(contenido_sql):
    tablas = set()
    patron = re.compile(r'\b(?:FROM|JOIN)\s+([\"a-zA-Z0-9_\.\-\/]+)', re.IGNORECASE)
    coincidencias = patron.findall(contenido_sql)
    for item in coincidencias:
        nombre = item.replace('"', '')
        if '/' in nombre:
            nombre = nombre.split('/')[-1]
        elif '.' in nombre:
            nombre = nombre.split('.')[-1]
        nombre_final = nombre.upper().strip()
        if nombre_final and not nombre_final.startswith('(') and len(nombre_final) > 2:
            tablas.add(nombre_final)
    return tablas

# =================================================================
# 2. GENERADOR DE MAPA
# =================================================================
def generar_mapa_multinivel(ruta_carpetas):
    print(f"--- CONSTRUYENDO ARQUITECTURA DE 4 NIVELES ---")

    # NIVEL 3 → NIVEL 4: Macro proceso a Lista de libros 
    
    libros_de_trabajo = {
        "SELL OUT":    ["Reporte Comercial", "Seguimiento Diario"],
        "Venta Total":[
  "Venta Total (Dirección General)",
  "Venta Total (LATAM)",
  "Radiografía de SKUs",
  "Marketplace Resell",
  "Reporte de Junta de Consejo",
  "Avance de Meta Mensual",
  "Venta Total (B2B)",
  "Ejecutivos Frankenstein",
  "Benchmark de Venta Total",
  "Venta Total (B2B Especializado)",
  "Venta Tuya Cloud",
  "Venta Total (Producto Empacado)",
  "Venta Total (Desarrollo de Producto)",
  "Radiografía de SKUs Reingenieria",
  "Radiografía de SKUs nueva fuente"
],
       
    }

    # Opcion 2 : Script SQL a Lista de libros
   # Usar el nombre exacto del archivo .sql
    scripts_a_reportes = {
        "mi_script_especial.sql": ["Seguimiento Diario", "Reporte Financiero"],
         "Concurso Retail.sql": ["Concurso Retail"],
       
    }

    # ── NIVEL 2 → NIVEL 3: Script → Macro proceso ───────────────────
    reglas_negocio = {
        "bipos":       "SELL OUT",
        "ventatotal":  "Venta Total",
        "venta total": "Venta Total",
    }

    net = Network(height="100vh", width="100%", bgcolor="#0f172a", font_color="white", directed=True)

    if not os.path.exists(ruta_carpetas):
        print(f"ERROR: No existe la ruta {ruta_carpetas}")
        return

    archivos_sql = [f for f in os.listdir(ruta_carpetas) if f.endswith('.sql')]

    # Helper para agregar un libro y su arista sin duplicados
    def conectar_a_libro(origen, libro):
        if libro not in [n['id'] for n in net.nodes]:
            net.add_node(
                libro,
                label=libro,
                color="#b9f3ef",
                shape="square",
                size=40,
                font={'size': 22, 'face': 'Arial', 'bold': True}
            )
        net.add_edge(origen, libro, color="#86b3e6", width=4)

    for archivo in archivos_sql:
        ruta_archivo = os.path.join(ruta_carpetas, archivo)

        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.read()
            tablas = extraer_tablas_limpio(contenido)

            # NIVEL 2: Nodo del Script 
            net.add_node(archivo, label=archivo, color="#00d4ff", shape="dot", size=25, font={'size': 14})

            # NIVEL 1: Nodos de Tabla 
            for tabla in tablas:
                net.add_node(tabla, label=tabla, color="#7115fa", shape="database", size=20, font={'size': 12})
                net.add_edge(tabla, archivo, color="#475569", width=1.5)

            # NIVEL 3: Macro Procesos 
            archivo_minusculas = archivo.lower()
            for palabra_clave, macro_proceso in reglas_negocio.items():
                if palabra_clave.lower() in archivo_minusculas:
                    if macro_proceso not in [n['id'] for n in net.nodes]:
                        net.add_node(
                            macro_proceso,
                            label=macro_proceso,
                            color="#066f0d",
                            shape="star",
                            size=45,
                            font={'size': 20, 'face': 'Arial', 'bold': True}
                        )
                    net.add_edge(archivo, macro_proceso, color="#a855f7", width=3)

                    # NIVEL 4: libros del macro proceso
                    for libro in libros_de_trabajo.get(macro_proceso, []):
                        conectar_a_libro(macro_proceso, libro)

            # opcion 2 script a lista de libros
            for libro in scripts_a_reportes.get(archivo, []):
                conectar_a_libro(archivo, libro)

    net.repulsion(node_distance=300, spring_length=250, spring_strength=0.05, damping=0.9)

    output_file = os.path.join(ruta_carpetas, "mapa_multinivel.html")
    net.save_graph(output_file)

    # =================================================================
    #Interfaz de Usuario
    # =================================================================
    CSS_PREMIUM = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap" rel="stylesheet">\n'
        '<style>\n'
        ':root{'
        '--bg-void:#04060d;--bg-glass:rgba(8,14,30,0.82);--border:rgba(255,255,255,0.07);'
        '--border-hi:rgba(168,135,255,0.3);--gold:#c9a96e;--cyan:#38bdf8;--violet:#a78bfa;'
        '--orange:#f97316;--text:#f1f5f9;--muted:#64748b;--dim:#1e293b;}\n'
        '*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}\n'
        'html,body{width:100%;height:100%;overflow:hidden;background:var(--bg-void);font-family:\'DM Sans\',sans-serif;color:var(--text)}\n'
        'body::before{content:\'\';position:fixed;inset:0;z-index:0;pointer-events:none;'
        'background:radial-gradient(ellipse 60% 50% at 15% 20%,rgba(99,58,210,.09) 0%,transparent 70%),'
        'radial-gradient(ellipse 50% 40% at 85% 75%,rgba(56,189,248,.06) 0%,transparent 70%)}\n'
        '#mynetwork{position:fixed!important;inset:0!important;width:100%!important;height:100%!important;z-index:1;border:none!important;background:transparent!important}\n'
        '#ui-header{position:fixed;top:28px;left:32px;z-index:100;animation:fadeDown .9s cubic-bezier(.16,1,.3,1) both}\n'
        '#ui-header .eyebrow{font-family:\'DM Mono\',monospace;font-size:10px;letter-spacing:.25em;color:var(--gold);text-transform:uppercase;opacity:.85}\n'
        '#ui-header h1{font-family:\'Bebas Neue\',sans-serif;font-size:36px;letter-spacing:.06em;line-height:1;color:var(--text)}\n'
        '#ui-header .goldline{width:36px;height:2px;background:linear-gradient(90deg,var(--gold),transparent);margin:6px 0;border-radius:2px}\n'
        '#ui-header .sub{font-size:11.5px;color:var(--muted);font-weight:300;letter-spacing:.03em}\n'
        '#ui-stats{position:fixed;top:28px;right:32px;z-index:100;display:flex;flex-direction:column;gap:10px;align-items:flex-end;animation:fadeDown .9s cubic-bezier(.16,1,.3,1) .1s both}\n'
        '.chip{background:var(--bg-glass);border:1px solid var(--border);border-radius:8px;padding:10px 18px;backdrop-filter:blur(20px);display:flex;flex-direction:column;align-items:flex-end;gap:2px;min-width:115px;box-shadow:0 8px 32px rgba(0,0,0,.5);transition:border-color .2s}\n'
        '.chip:hover{border-color:var(--border-hi)}\n'
        '.chip .val{font-family:\'Bebas Neue\',sans-serif;font-size:30px;letter-spacing:.04em;line-height:1}\n'
        '.chip .lbl{font-family:\'DM Mono\',monospace;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}\n'
        '.chip.violet .val{color:var(--violet)}.chip.cyan .val{color:var(--cyan)}.chip.gold .val{color:var(--gold)}.chip.orange .val{color:var(--orange)}\n'
        '#ui-legend{position:fixed;bottom:32px;left:32px;z-index:100;background:var(--bg-glass);border:1px solid var(--border);border-radius:10px;padding:18px 22px;backdrop-filter:blur(20px);box-shadow:0 24px 80px rgba(0,0,0,.8);animation:fadeUp 1s cubic-bezier(.16,1,.3,1) .2s both}\n'
        '#ui-legend .ltitle{font-family:\'DM Mono\',monospace;font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin-bottom:14px}\n'
        '.lrow{display:flex;align-items:center;gap:10px;margin-bottom:10px;font-size:12.5px;font-weight:300}\n'
        '.lrow:last-child{margin-bottom:0}\n'
        '.ldot{width:10px;height:10px;border-radius:50%;flex-shrink:0}\n'
        '.ldb{width:10px;height:12px;border-radius:2px;flex-shrink:0}\n'
        '.lstar{width:12px;height:12px;flex-shrink:0;clip-path:polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)}\n'
        '.lsq{width:11px;height:11px;flex-shrink:0}\n'
        '#ui-controls{position:fixed;bottom:32px;right:32px;z-index:100;display:flex;gap:8px;animation:fadeUp 1s cubic-bezier(.16,1,.3,1) .3s both}\n'
        '.btn{background:var(--bg-glass);border:1px solid var(--border);border-radius:8px;padding:9px 16px;backdrop-filter:blur(20px);color:var(--muted);font-family:\'DM Mono\',monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;transition:all .18s;box-shadow:0 4px 16px rgba(0,0,0,.4)}\n'
        '.btn:hover{border-color:var(--border-hi);color:var(--text);background:rgba(167,139,250,.1)}\n'
        '#ui-wm{position:fixed;bottom:36px;left:50%;transform:translateX(-50%);z-index:100;font-family:\'DM Mono\',monospace;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--dim);pointer-events:none;animation:fadeUp 1.2s cubic-bezier(.16,1,.3,1) .4s both}\n'
        '.vis-tooltip{background:var(--bg-glass)!important;border:1px solid var(--border-hi)!important;border-radius:8px!important;color:var(--text)!important;font-family:\'DM Sans\',sans-serif!important;font-size:12px!important;padding:8px 14px!important;backdrop-filter:blur(20px)!important;box-shadow:0 12px 40px rgba(0,0,0,.6)!important}\n'
        '@keyframes fadeDown{from{opacity:0;transform:translateY(-14px)}to{opacity:1;transform:translateY(0)}}\n'
        '@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}\n'
        '</style>\n'
    )

    UI_HTML = (
        '<div id="ui-header">'
        '<span class="eyebrow">Business Intelligence &middot; Data Architecture</span>'
        '<h1>Mapa de Linaje</h1>'
        '<div class="goldline"></div>'
        '<span class="sub">Visualizaci&oacute;n de dependencias y flujo de datos</span>'
        '</div>\n'
        '<div id="ui-stats">'
        '<div class="chip violet"><span class="val" id="s-scripts">-</span><span class="lbl">Scripts SQL</span></div>'
        '<div class="chip cyan"><span class="val" id="s-tables">-</span><span class="lbl">Tablas Fuente</span></div>'
        '<div class="chip gold"><span class="val" id="s-macros">-</span><span class="lbl">Macro Procesos</span></div>'
        '<div class="chip orange"><span class="val" id="s-books">-</span><span class="lbl">Libros de Trabajo</span></div>'
        '</div>\n'
        '<div id="ui-legend">'
        '<div class="ltitle">Tipos de nodo</div>'
        '<div class="lrow"><div class="ldb" style="background:#7115fa"></div> Tabla fuente</div>'
        '<div class="lrow"><div class="ldot" style="background:#00d4ff"></div> Script SQL</div>'
        '<div class="lrow"><div class="lstar" style="background:#066f0d"></div> Macro proceso</div>'
        '<div class="lrow"><div class="lsq" style="background:#f97316"></div> Libro de trabajo</div>'
        '</div>\n'
        '<div id="ui-controls">'
        '<button class="btn" onclick="network.fit()">Ajustar</button>'
        '<button class="btn" onclick="network.stabilize()">Estabilizar</button>'
        '</div>\n'
        '<div id="ui-wm">Data Lineage Map &middot; Generado autom&aacute;ticamente</div>\n'
        '<script>\n'
        '(function poll(){\n'
        '  var t=setInterval(function(){\n'
        '    if(typeof network==="undefined") return;\n'
        '    clearInterval(t);\n'
        '    var n=network.body.data.nodes.get();\n'
        '    document.getElementById("s-scripts").textContent=n.filter(function(x){return x.shape==="dot";}).length;\n'
        '    document.getElementById("s-tables").textContent=n.filter(function(x){return x.shape==="database";}).length;\n'
        '    document.getElementById("s-macros").textContent=n.filter(function(x){return x.shape==="star";}).length;\n'
        '    document.getElementById("s-books").textContent=n.filter(function(x){return x.shape==="square";}).length;\n'
        '  },200);\n'
        '})();\n'
        '</script>\n'
    )

    with open(output_file, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("</head>", CSS_PREMIUM + "</head>")
    html = html.replace("<body>",  "<body>\n" + UI_HTML)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n--- ÉXITO ---")
    print(f"Mapa premium generado en: {output_file}")

# =================================================================
# 3. Archivo Guardado
# =================================================================
mi_ruta = r"C:\Users\jluna\Desktop\env_bi\Mapa de Linaje"
generar_mapa_multinivel(mi_ruta)
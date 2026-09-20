import json
import os
import random

import flet as ft

# ----------------------------------------------------------------------------
# Configuración y colores
# ----------------------------------------------------------------------------
BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE, "assets")
SAVE_FILE = os.path.join(BASE, "guardado.json")

VERDE_OSCURO = "#146B3A"
VERDE = "#2E9E5B"
VERDE_MEDIO = "#5DBE7B"
VERDE_CLARO = "#DDF5E3"
AMARILLO = "#FFC83D"
BLANCO = "#FFFFFF"
GRIS = "#B8C4BC"
ROJO_SUAVE = "#FDE3E3"
ROJO = "#D64545"

SOMBRA = ft.BoxShadow(
    blur_radius=10,
    color=ft.Colors.with_opacity(0.16, ft.Colors.BLACK),
    offset=ft.Offset(0, 4),
)

TEMAS = {
    "clasico": {"arriba": "#E6F8EA", "abajo": "#6CCB85", "ola1": "#4FB870", "ola2": "#2E9E5B"},
    "caribe": {"arriba": "#E0F7FA", "abajo": "#4FC3E0", "ola1": "#2BA7C9", "ola2": "#1B86A8"},
}

# ----------------------------------------------------------------------------
# Datos del juego (puedes moverlos a un JSON si prefieres)
# Cada país: 3 preguntas de acentos y 3 de modismos.
# opciones = (texto, subtítulo)   correcta = índice de la opción correcta
# Las frases de acentos son de ejemplo: cámbialas por tus audios reales.
# ----------------------------------------------------------------------------
PAISES = [
    {"nombre": "México", "codigo": "MX", "colores": ["#006847", "#FFFFFF", "#CE1126"]},
    {"nombre": "Colombia", "codigo": "CO", "colores": ["#FCD116", "#003893", "#CE1126"]},
    {"nombre": "Perú", "codigo": "PE", "colores": ["#D91023", "#FFFFFF", "#D91023"]},
    {"nombre": "Uruguay", "codigo": "UY", "colores": ["#FFFFFF", "#0038A8", "#FFFFFF"]},
    {"nombre": "Argentina", "codigo": "AR", "colores": ["#74ACDF", "#FFFFFF", "#74ACDF"]},
]

PREGUNTAS = {
    "México": {
        "acentos": [
            {"frase": "Órale, cuate, ¿qué onda? Está bien padre.", "audio": "mx_chilango.mp3",
             "opciones": [("Chilango", "Ciudad de México"), ("Norteño", "Monterrey"), ("Yucateco", "Mérida")], "correcta": 0},
            {"frase": "¿Qué onda, compa? Vámonos a echar unos tacos al carbón.", "audio": "mx_norteno.mp3",
             "opciones": [("Yucateco", "Mérida"), ("Norteño", "Monterrey"), ("Chilango", "Ciudad de México")], "correcta": 1},
            {"frase": "¿Bix a bel? Vamos por unos panuchos.", "audio": "mx_yucateco.mp3",
             "opciones": [("Norteño", "Monterrey"), ("Chilango", "Ciudad de México"), ("Yucateco", "Mérida")], "correcta": 2},
        ],
        "modismos": [
            {"frase": "No manches", "opciones": [("Expresar sorpresa", "¡No puede ser!"), ("Pedir silencio", "Callarse"), ("Lavar la ropa", "Limpiar")], "correcta": 0},
            {"frase": "Echar la hueva", "opciones": [("Cocinar huevos", "En la cocina"), ("Holgazanear", "No hacer nada"), ("Hacer deporte", "Ejercitarse")], "correcta": 1},
            {"frase": "Estar crudo", "opciones": [("Tener hambre", "Ganas de comer"), ("Estar enojado", "Sentir rabia"), ("Tener resaca", "Malestar al día siguiente")], "correcta": 2},
        ],
    },
    "Colombia": {
        "acentos": [
            {"frase": "¿Qué más, parce? Todo bien por acá.", "audio": "co_paisa.mp3",
             "opciones": [("Paisa", "Antioquia"), ("Costeño", "Región Caribe"), ("Rolo", "Bogotá")], "correcta": 0},
            {"frase": "Ajá, mi amor, ¿y tú qué? Eso está bien barato.", "audio": "co_costeno.mp3",
             "opciones": [("Rolo", "Bogotá"), ("Paisa", "Antioquia"), ("Costeño", "Región Caribe")], "correcta": 2},
            {"frase": "¿Cómo le va, sumercé? Qué gusto verlo.", "audio": "co_rolo.mp3",
             "opciones": [("Costeño", "Región Caribe"), ("Rolo", "Bogotá"), ("Paisa", "Antioquia")], "correcta": 1},
        ],
        "modismos": [
            {"frase": "Estar en la luna", "opciones": [("Estar distraído", "No prestar atención"), ("Estar enojado", "Sentir rabia"), ("Estar cansado", "Tener sueño")], "correcta": 0},
            {"frase": "Dar papaya", "opciones": [("Regalar fruta", "Ser generoso"), ("Exponerse", "Facilitar que se aprovechen"), ("Cocinar", "Preparar comida")], "correcta": 1},
            {"frase": "Ser un gomelo", "opciones": [("Ser muy rápido", "Correr mucho"), ("Ser tímido", "No hablar"), ("Ser presumido", "Joven de clase alta")], "correcta": 2},
        ],
    },
    "Perú": {
        "acentos": [
            {"frase": "Pucha, causa, qué chévere está esto.", "audio": "pe_limeno.mp3",
             "opciones": [("Limeño", "Lima"), ("Arequipeño", "Arequipa"), ("Cusqueño", "Cusco")], "correcta": 0},
            {"frase": "Oye, ¿vamos por un rocoto relleno, ya?", "audio": "pe_arequipeno.mp3",
             "opciones": [("Cusqueño", "Cusco"), ("Arequipeño", "Arequipa"), ("Limeño", "Lima")], "correcta": 1},
            {"frase": "Ay, papay, qué frío hace hoy, ¿no?", "audio": "pe_cusqueno.mp3",
             "opciones": [("Limeño", "Lima"), ("Arequipeño", "Arequipa"), ("Cusqueño", "Cusco")], "correcta": 2},
        ],
        "modismos": [
            {"frase": "Pisar el palito", "opciones": [("Caer en una trampa", "Ser engañado"), ("Bailar", "Moverse al ritmo"), ("Hacer deporte", "Correr")], "correcta": 0},
            {"frase": "Chamba", "opciones": [("Fiesta", "Celebración"), ("Trabajo", "Empleo"), ("Comida", "Almuerzo")], "correcta": 1},
            {"frase": "Estar misio", "opciones": [("Estar feliz", "Sentir alegría"), ("Estar perdido", "No saber dónde"), ("No tener plata", "Estar sin dinero")], "correcta": 2},
        ],
    },
    "Uruguay": {
        "acentos": [
            {"frase": "Bo, ¿qué hacés? Vamos a tomar unos mates a la rambla.", "audio": "uy_montevideano.mp3",
             "opciones": [("Montevideano", "Montevideo"), ("Fronterizo", "Rivera"), ("Porteño", "Buenos Aires")], "correcta": 0},
            {"frase": "Ta, ta, dale que llegamos temprano.", "audio": "uy_ta.mp3",
             "opciones": [("Porteño", "Buenos Aires"), ("Montevideano", "Montevideo"), ("Cordobés", "Córdoba")], "correcta": 1},
            {"frase": "Bo, ¿viste el partido? Estuvo bárbaro.", "audio": "uy_bo.mp3",
             "opciones": [("Paisa", "Antioquia"), ("Limeño", "Lima"), ("Montevideano", "Montevideo")], "correcta": 2},
        ],
        "modismos": [
            {"frase": "Botija", "opciones": [("Niño", "Chico o chica"), ("Botella", "Recipiente"), ("Jefe", "Líder")], "correcta": 0},
            {"frase": "Ta", "opciones": [("Tarde", "Llegar después"), ("De acuerdo", "Está bien, ok"), ("Tal vez", "No estar seguro")], "correcta": 1},
            {"frase": "Ni ahí", "opciones": [("Estar cerca", "A pocos metros"), ("Estar de acuerdo", "Decir que sí"), ("De ninguna manera", "Rechazar algo")], "correcta": 2},
        ],
    },
    "Argentina": {
        "acentos": [
            {"frase": "Che, boludo, ¿viste el partido? Una masa.", "audio": "ar_porteno.mp3",
             "opciones": [("Porteño", "Buenos Aires"), ("Cordobés", "Córdoba"), ("Salteño", "Salta")], "correcta": 0},
            {"frase": "Mirá vos, qué lindo che, vamos al cuarteto.", "audio": "ar_cordobes.mp3",
             "opciones": [("Salteño", "Salta"), ("Cordobés", "Córdoba"), ("Porteño", "Buenos Aires")], "correcta": 1},
            {"frase": "Vamos a la peña a comer unas empanadas salteñas.", "audio": "ar_salteno.mp3",
             "opciones": [("Porteño", "Buenos Aires"), ("Cordobés", "Córdoba"), ("Salteño", "Salta")], "correcta": 2},
        ],
        "modismos": [
            {"frase": "Estar al horno", "opciones": [("Estar en problemas", "Situación difícil"), ("Tener calor", "Sentir temperatura"), ("Cocinar", "Preparar comida")], "correcta": 0},
            {"frase": "Un mango", "opciones": [("Una fruta", "Fruta tropical"), ("Un peso", "Dinero"), ("Un rato", "Poco tiempo")], "correcta": 1},
            {"frase": "Laburar", "opciones": [("Descansar", "Dormir"), ("Pasear", "Salir a caminar"), ("Trabajar", "Tener un empleo")], "correcta": 2},
        ],
    },
}

TIENDA = [
    {"id": "sombrero", "nombre": "Sombrero vueltiao", "desc": "Accesorio de Mapi", "precio": 80,
     "tab": "Objetos", "tipo": "equipo", "emoji": "👒", "color": "#FFF3D6"},
    {"id": "gorra", "nombre": "Gorra latina", "desc": "Accesorio de Mapi", "precio": 60,
     "tab": "Objetos", "tipo": "equipo", "emoji": "🧢", "color": "#D9F0DF"},
    {"id": "pista", "nombre": "Pista extra", "desc": "Úsala en cualquier nivel", "precio": 40,
     "tab": "Ayudas", "tipo": "ayuda", "emoji": "💡", "color": "#FFF0DD"},
    {"id": "caribe", "nombre": "Tema Caribe", "desc": "Fondo especial del mapa", "precio": 120,
     "tab": "Temas", "tipo": "tema", "emoji": "🌊", "color": "#DDF2F7"},
]

XP_POR_ACIERTO = 20
PUNTOS_POR_ACIERTO = 10


# ----------------------------------------------------------------------------
# Estado guardado (puntos, nivel, compras, progreso)
# ----------------------------------------------------------------------------
class Estado:
    def __init__(self):
        self.reiniciar()
        self.cargar()

    def reiniciar(self):
        self.puntos = 245
        self.xp = 0
        self.nivel = 1
        self.max_pais = 0          # índice del último país desbloqueado
        self.pistas = 2
        self.comprados = []        # ids de objetos/temas comprados
        self.equipado = None       # id del accesorio puesto en Mapi
        self.tema = "clasico"

    def cargar(self):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                datos = json.load(f)
            for k, v in datos.items():
                if hasattr(self, k):
                    setattr(self, k, v)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def guardar(self):
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.__dict__, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    @property
    def xp_necesaria(self):
        return self.nivel * 100

    def sumar_xp(self, cantidad):
        self.xp += cantidad
        while self.xp >= self.xp_necesaria:
            self.xp -= self.xp_necesaria
            self.nivel += 1


# ----------------------------------------------------------------------------
# App
# ----------------------------------------------------------------------------
class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.estado = Estado()
        self.q = None          # partida en curso
        self.tab_tienda = "Objetos"
        self.audio = None

        page.title = "Mapiando"
        page.padding = 0
        page.spacing = 0
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.width = 400
        page.window.height = 820
        page.bgcolor = "#E6F8EA"

        self.vista_inicio()

    # ------------------------------------------------------------------ util
    def mostrar(self, control):
        self.page.clean()
        self.page.add(control)
        self.page.update()

    def aviso(self, texto):
        self.page.open(ft.SnackBar(ft.Text(texto), duration=2200))

    def tema(self):
        return TEMAS.get(self.estado.tema, TEMAS["clasico"])

    def fondo(self, contenido, olas=False):
        t = self.tema()
        capas = [
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[t["arriba"], t["abajo"]],
                ),
            )
        ]
        if olas:
            capas.append(
                ft.Container(
                    height=130, left=-60, right=-60, bottom=-20,
                    bgcolor=t["ola1"], border_radius=ft.border_radius.only(top_left=260, top_right=260),
                )
            )
            capas.append(
                ft.Container(
                    height=90, left=-30, right=-60, bottom=-20,
                    bgcolor=t["ola2"], border_radius=ft.border_radius.only(top_left=200, top_right=300),
                )
            )
        capas.append(ft.Container(content=contenido, expand=True))
        return ft.Stack(capas, expand=True)

    def boton(self, texto, icono, on_click, principal=False, ancho=270, alto=54):
        color_txt = BLANCO if principal else VERDE_OSCURO
        fila = []
        if icono:
            fila.append(ft.Icon(icono, color=color_txt, size=22))
        fila.append(ft.Text(texto, weight=ft.FontWeight.W_800, size=16, color=color_txt))
        return ft.Container(
            content=ft.Row(fila, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            width=ancho, height=alto, border_radius=16,
            bgcolor=VERDE if principal else BLANCO,
            border=ft.border.all(2, VERDE_OSCURO) if principal else None,
            shadow=SOMBRA, on_click=on_click, ink=True,
            alignment=ft.alignment.center,
        )

    def boton_redondo(self, icono, on_click, bg=BLANCO, color=VERDE_OSCURO, size=40):
        return ft.Container(
            content=ft.Icon(icono, color=color, size=size * 0.5),
            width=size, height=size, border_radius=size / 2, bgcolor=bg,
            alignment=ft.alignment.center, shadow=SOMBRA, on_click=on_click, ink=True,
        )

    def tarjeta(self, contenido, padding=16, ancho=None):
        return ft.Container(
            content=contenido, padding=padding, bgcolor=BLANCO, width=ancho,
            border_radius=22, shadow=SOMBRA,
        )

    def mapi(self, size=56):
        """Mascota. Si existe assets/mapi.png la usa; si no, dibuja una carita."""
        if os.path.exists(os.path.join(ASSETS_DIR, "mapi.png")):
            cara = ft.Image(src="mapi.png", width=size, height=size)
        else:
            cara = ft.Container(
                width=size, height=size, border_radius=size / 2, bgcolor=VERDE,
                border=ft.border.all(2, VERDE_OSCURO), alignment=ft.alignment.center,
                content=ft.Icon(ft.Icons.SENTIMENT_SATISFIED_ALT, color=BLANCO, size=size * 0.62),
            )
        extra = next((i["emoji"] for i in TIENDA if i["id"] == self.estado.equipado), "")
        if not extra:
            return cara
        return ft.Stack(
            [cara, ft.Container(ft.Text(extra, size=size * 0.45), left=size * 0.22, top=-size * 0.28)],
            width=size, height=size, clip_behavior=ft.ClipBehavior.NONE,
        )

    def barra_progreso(self, valor, alto=10, color=VERDE):
        return ft.ProgressBar(
            value=valor, bar_height=alto, color=color,
            bgcolor=ft.Colors.with_opacity(0.25, VERDE_OSCURO), border_radius=alto,
        )

    def chip_pais(self, pais):
        franja = ft.Row(
            [ft.Container(width=8, height=12, bgcolor=c) for c in pais["colores"]],
            spacing=0,
        )
        return ft.Container(
            content=ft.Row(
                [ft.Container(franja, border_radius=3, clip_behavior=ft.ClipBehavior.HARD_EDGE),
                 ft.Text(pais["nombre"].upper(), size=10, weight=ft.FontWeight.W_800, color=VERDE_OSCURO)],
                spacing=6, tight=True,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=4),
            bgcolor=BLANCO, border_radius=20, shadow=SOMBRA,
        )

    # ---------------------------------------------------------- 1. INICIO
    def vista_inicio(self, e=None):
        contenido = ft.Column(
            [
                ft.Container(expand=2),
                ft.Icon(ft.Icons.LOCATION_ON, size=58, color=VERDE_OSCURO),
                ft.Text("Mapiando", size=46, weight=ft.FontWeight.W_900, color=VERDE_OSCURO),
                ft.Text("Descubre Latinoamérica jugando", size=13, color=VERDE_OSCURO),
                ft.Container(height=36),
                self.boton("JUGAR", ft.Icons.PLAY_CIRCLE_FILL, self.vista_mapa, principal=True),
                self.boton("OPCIONES", ft.Icons.SETTINGS, self.abrir_opciones),
                self.boton("SALIR", ft.Icons.LOGOUT, lambda e: self.page.window.close()),
                ft.Container(expand=3),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
        )
        self.mostrar(self.fondo(contenido, olas=True))

    def abrir_opciones(self, e=None):
        def reiniciar(_):
            self.estado.reiniciar()
            self.estado.guardar()
            self.page.close(dlg)
            self.aviso("Progreso reiniciado")

        dlg = ft.AlertDialog(
            title=ft.Text("Opciones"),
            content=ft.Text("¿Quieres borrar tu progreso, puntos y compras y empezar de cero?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.page.close(dlg)),
                ft.TextButton("Reiniciar progreso", on_click=reiniciar),
            ],
        )
        self.page.open(dlg)

    # ---------------------------------------------------------- 2. MAPA
    def vista_mapa(self, e=None):
        est = self.estado
        cabecera = ft.Row(
            [
                self.tarjeta(
                    ft.Column(
                        [
                            ft.Text(f"Nivel {est.nivel}", size=13, weight=ft.FontWeight.W_800, color=VERDE_OSCURO),
                            self.barra_progreso(est.xp / est.xp_necesaria, alto=6),
                            ft.Text(f"{est.xp} / {est.xp_necesaria} XP", size=9, color=VERDE_OSCURO),
                            ft.Text(f"● {est.puntos} pts", size=10, weight=ft.FontWeight.W_700, color="#E09A00"),
                        ],
                        spacing=3, tight=True,
                    ),
                    padding=10, ancho=125,
                ),
                ft.Text("Mapiando", size=22, weight=ft.FontWeight.W_900, color=BLANCO),
                ft.Row(
                    [
                        self.boton_redondo(ft.Icons.STOREFRONT, self.vista_tienda, size=38),
                        self.boton_redondo(ft.Icons.ARROW_BACK_IOS_NEW, self.vista_inicio, size=38),
                    ],
                    spacing=6,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        # --- mapa: imagen de fondo + nodos por coordenadas (ajústalas a tu mapa.png)
        ancho, alto = 340, 470
        posiciones = [(70, 40), (185, 105), (80, 185), (200, 260), (95, 340)]
        capas = []
        if os.path.exists(os.path.join(ASSETS_DIR, "mapa.png")):
            capas.append(ft.Image(src="mapa.png", width=ancho, height=alto, fit=ft.ImageFit.CONTAIN))
        else:
            capas.append(ft.Container(
                left=45, top=10, width=250, height=440, bgcolor="#3FA867",
                border=ft.border.all(3, VERDE_OSCURO),
                border_radius=ft.border_radius.only(top_left=120, top_right=60, bottom_left=40, bottom_right=140),
                content=ft.Text("Pon tu mapa en\nassets/mapa.png", size=11, color=BLANCO,
                                text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.bottom_center, padding=12,
            ))

        # línea punteada entre niveles
        for i in range(len(posiciones) - 1):
            x1, y1 = posiciones[i]
            x2, y2 = posiciones[i + 1]
            for k in range(1, 7):
                t = k / 7
                capas.append(ft.Container(
                    left=x1 + 23 + (x2 - x1) * t - 3, top=y1 + 23 + (y2 - y1) * t - 3,
                    width=6, height=6, border_radius=3, bgcolor=BLANCO,
                ))

        for i, pais in enumerate(PAISES):
            libre = i <= est.max_pais
            x, y = posiciones[i]
            nodo = ft.Container(
                width=46, height=46, border_radius=23,
                bgcolor=AMARILLO if libre else "#D9DEE2",
                border=ft.border.all(3, BLANCO), shadow=SOMBRA,
                alignment=ft.alignment.center,
                content=ft.Text(str(i + 1), size=18, weight=ft.FontWeight.W_900, color=VERDE_OSCURO)
                if libre else ft.Icon(ft.Icons.LOCK, size=20, color="#8A959D"),
                on_click=lambda e, idx=i: self.elegir_modo(idx),
            )
            etiqueta = ft.Container(
                ft.Text(pais["nombre"], size=10, weight=ft.FontWeight.W_800, color=VERDE_OSCURO),
                padding=ft.padding.symmetric(horizontal=6, vertical=1),
                bgcolor=ft.Colors.with_opacity(0.85, BLANCO), border_radius=8,
            )
            capas.append(ft.Column([nodo, etiqueta], left=x, top=y, spacing=2,
                                   horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=46))

        marco_mapa = ft.Container(
            content=ft.Stack(capas, width=ancho, height=alto),
            bgcolor=ft.Colors.with_opacity(0.18, BLANCO),
            border_radius=24, border=ft.border.all(1, ft.Colors.with_opacity(0.5, BLANCO)),
            alignment=ft.alignment.center, expand=True,
        )

        ayuda = self.tarjeta(
            ft.Row(
                [
                    self.mapi(44),
                    ft.Column(
                        [ft.Text("¿Cómo jugar?", size=14, weight=ft.FontWeight.W_800, color=VERDE_OSCURO),
                         ft.Text("Mapi te explica", size=11, color=VERDE_OSCURO)],
                        spacing=0, expand=True,
                    ),
                    self.boton_redondo(ft.Icons.HELP_OUTLINE, self.como_jugar, bg=AMARILLO, size=40),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=12,
        )

        contenido = ft.Column([cabecera, marco_mapa, ayuda], spacing=12)
        # fondo azul (mapa) como en el Figma
        self.mostrar(ft.Container(
            content=ft.Container(contenido, padding=ft.padding.only(left=14, right=14, top=16, bottom=14)),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center, end=ft.alignment.bottom_center,
                colors=["#59B8F0", "#1F86D6"],
            ),
            expand=True,
        ))

    def como_jugar(self, e=None):
        dlg = ft.AlertDialog(
            title=ft.Text("¿Cómo jugar?"),
            content=ft.Text(
                "1. Toca un nivel del mapa y elige Acentos o Modismos.\n"
                "2. Responde las preguntas: cada acierto suma puntos y XP.\n"
                "3. Con 2 aciertos o más desbloqueas el siguiente país.\n"
                "4. Usa las pistas si te atascas y gasta tus puntos en la tienda."
            ),
            actions=[ft.TextButton("¡Entendido!", on_click=lambda _: self.page.close(dlg))],
        )
        self.page.open(dlg)

    def elegir_modo(self, idx):
        if idx > self.estado.max_pais:
            self.aviso("Completa el nivel anterior para desbloquear este país.")
            return
        pais = PAISES[idx]

        def jugar(tipo):
            self.page.close(dlg)
            self.iniciar_quiz(idx, tipo)

        dlg = ft.AlertDialog(
            title=ft.Text(f"{pais['nombre']}"),
            content=ft.Text("¿Qué quieres practicar?"),
            actions=[
                ft.TextButton("Acentos", on_click=lambda _: jugar("acentos")),
                ft.TextButton("Modismos", on_click=lambda _: jugar("modismos")),
            ],
        )
        self.page.open(dlg)

    # ------------------------------------------------- 3 y 4. QUIZ
    def iniciar_quiz(self, idx, tipo):
        pais = PAISES[idx]
        preguntas = []
        for p in random.sample(PREGUNTAS[pais["nombre"]][tipo], k=len(PREGUNTAS[pais["nombre"]][tipo])):
            orden = list(range(len(p["opciones"])))
            random.shuffle(orden)
            preguntas.append({
                **p,
                "opciones": [p["opciones"][i] for i in orden],
                "correcta": orden.index(p["correcta"]),
            })
        self.q = {"idx": idx, "tipo": tipo, "preguntas": preguntas, "i": 0, "aciertos": 0,
                  "respuesta": None, "ocultas": [], "pista_usada": False}
        self.vista_quiz()

    def vista_quiz(self):
        q, est = self.q, self.estado
        pais = PAISES[q["idx"]]
        total = len(q["preguntas"])
        preg = q["preguntas"][q["i"]]
        es_acento = q["tipo"] == "acentos"
        respondida = q["respuesta"] is not None

        titulo = f"{'Acentos' if es_acento else 'Modismos'} de {pais['nombre']}"
        cabecera = ft.Column(
            [
                ft.Row(
                    [
                        self.boton_redondo(ft.Icons.ARROW_BACK_IOS_NEW, self.vista_mapa, size=38),
                        ft.Text(titulo, size=18, weight=ft.FontWeight.W_900, color=VERDE_OSCURO),
                        self.boton_redondo(ft.Icons.HELP_OUTLINE, self.como_jugar, bg=AMARILLO, size=38),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row([self.chip_pais(pais)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [
                        ft.Container(self.barra_progreso(q["i"] / total, alto=10), expand=True),
                        ft.Text(f"{q['i'] + 1} / {total}", size=12, weight=ft.FontWeight.W_700, color=VERDE_OSCURO),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )

        if es_acento:
            cuerpo = ft.Column(
                [
                    ft.Text("ESCUCHA Y DESCUBRE", size=10, weight=ft.FontWeight.W_800, color=VERDE),
                    ft.Text("¿De qué región es este acento?", size=21, weight=ft.FontWeight.W_900,
                            color=VERDE_OSCURO, text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        content=ft.Icon(ft.Icons.MUSIC_NOTE, color=BLANCO, size=38),
                        width=76, height=76, border_radius=38, bgcolor=VERDE,
                        border=ft.border.all(4, VERDE_MEDIO), alignment=ft.alignment.center,
                        shadow=SOMBRA, ink=True, on_click=lambda e: self.reproducir(preg.get("audio")),
                    ),
                    ft.Text("Toca para escuchar y repetir", size=10, color=VERDE_OSCURO),
                    ft.Text(f"“{preg['frase']}”", size=12, italic=True, color="#5C6B62",
                            text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8,
            )
            subtitulo = "Selecciona una respuesta"
        else:
            cuerpo = ft.Column(
                [
                    ft.Text("DESCUBRE EL SIGNIFICADO", size=10, weight=ft.FontWeight.W_800, color=VERDE),
                    ft.Text("¿Qué significa esta expresión?", size=21, weight=ft.FontWeight.W_900,
                            color=VERDE_OSCURO, text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        ft.Text(f"“{preg['frase']}”", size=19, weight=ft.FontWeight.W_800, color=VERDE_OSCURO,
                                text_align=ft.TextAlign.CENTER),
                        padding=ft.padding.symmetric(horizontal=20, vertical=16), bgcolor=VERDE_CLARO,
                        border_radius=16, border=ft.border.all(2, VERDE_MEDIO), alignment=ft.alignment.center,
                    ),
                    ft.Text("Elige la opción que mejor la explica", size=10, color=VERDE_OSCURO),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10,
            )
            subtitulo = "Elige el significado correcto"

        tarjeta_pregunta = ft.Container(
            self.tarjeta(cuerpo, padding=18), alignment=ft.alignment.center,
        )

        # --- opciones A / B / C
        opciones = []
        for n, (texto, sub) in enumerate(preg["opciones"]):
            if n in q["ocultas"]:
                continue
            bg, borde, letra_bg = BLANCO, None, VERDE
            icono = ft.Icons.CHEVRON_RIGHT
            if respondida:
                if n == preg["correcta"]:
                    bg, borde, letra_bg, icono = "#DFF7E5", ft.border.all(2, VERDE), VERDE, ft.Icons.CHECK_CIRCLE
                elif n == q["respuesta"]:
                    bg, borde, letra_bg, icono = ROJO_SUAVE, ft.border.all(2, ROJO), ROJO, ft.Icons.CANCEL
            opciones.append(ft.Container(
                content=ft.Row(
                    [
                        ft.Container(ft.Text("ABC"[n], size=13, weight=ft.FontWeight.W_900, color=BLANCO),
                                     width=28, height=28, border_radius=14, bgcolor=letra_bg,
                                     alignment=ft.alignment.center),
                        ft.Column(
                            [ft.Text(texto, size=14, weight=ft.FontWeight.W_800, color=VERDE_OSCURO),
                             ft.Text(sub, size=10, color="#5C6B62")],
                            spacing=0, expand=True,
                        ),
                        ft.Icon(icono, color=letra_bg if respondida and borde else VERDE_OSCURO, size=20),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=14, vertical=11),
                bgcolor=bg, border=borde, border_radius=16, shadow=SOMBRA, ink=True,
                on_click=None if respondida else (lambda e, k=n: self.responder(k)),
            ))

        # --- botones inferiores
        if respondida:
            ultimo = q["i"] == total - 1
            derecha = self.boton("Ver resultado" if ultimo else "Siguiente", ft.Icons.ARROW_FORWARD,
                                 self.siguiente, principal=True, ancho=170, alto=48)
        else:
            derecha = self.boton(f"Pista ({est.pistas})", ft.Icons.LIGHTBULB, self.usar_pista,
                                 ancho=170, alto=48)
        inferior = ft.Row(
            [self.boton("Volver al mapa", None, self.vista_mapa, ancho=170, alto=48), derecha],
            alignment=ft.MainAxisAlignment.CENTER, spacing=12,
        )

        contenido = ft.Column(
            [
                ft.Container(cabecera, padding=ft.padding.only(left=16, right=16, top=16)),
                ft.Container(tarjeta_pregunta, padding=ft.padding.symmetric(horizontal=16)),
                ft.Container(
                    ft.Text(subtitulo, size=12, weight=ft.FontWeight.W_800, color=VERDE_OSCURO),
                    padding=ft.padding.only(left=20, top=4),
                ),
                ft.Container(ft.Column(opciones, spacing=9), padding=ft.padding.symmetric(horizontal=16)),
                ft.Container(expand=True),
                ft.Container(inferior, padding=ft.padding.only(bottom=22)),
            ],
            spacing=10, scroll=ft.ScrollMode.AUTO, expand=True,
        )
        self.mostrar(self.fondo(contenido, olas=True))

    def reproducir(self, archivo):
        if not archivo:
            return
        ruta = os.path.join(ASSETS_DIR, "audio", archivo)
        if not os.path.exists(ruta):
            self.aviso(f"Falta el audio: assets/audio/{archivo}")
            return
        try:
            if self.audio in self.page.overlay:
                self.page.overlay.remove(self.audio)
            self.audio = ft.Audio(src=f"/audio/{archivo}", autoplay=True)
            self.page.overlay.append(self.audio)
            self.page.update()
        except Exception as ex:  # el audio no debe romper el juego
            self.aviso(f"No se pudo reproducir el audio: {ex}")

    def responder(self, n):
        q, est = self.q, self.estado
        preg = q["preguntas"][q["i"]]
        q["respuesta"] = n
        if n == preg["correcta"]:
            q["aciertos"] += 1
            est.puntos += PUNTOS_POR_ACIERTO
            est.sumar_xp(XP_POR_ACIERTO)
            est.guardar()
        self.vista_quiz()

    def usar_pista(self, e=None):
        q, est = self.q, self.estado
        if q["pista_usada"]:
            self.aviso("Ya usaste la pista en esta pregunta.")
            return
        if est.pistas <= 0:
            self.aviso("No tienes pistas. Compra más en la tienda.")
            return
        preg = q["preguntas"][q["i"]]
        malas = [n for n in range(len(preg["opciones"])) if n != preg["correcta"] and n not in q["ocultas"]]
        if malas:
            q["ocultas"].append(random.choice(malas))
            q["pista_usada"] = True
            est.pistas -= 1
            est.guardar()
        self.vista_quiz()

    def siguiente(self, e=None):
        q = self.q
        if q["i"] + 1 >= len(q["preguntas"]):
            self.vista_resultado()
            return
        q["i"] += 1
        q["respuesta"] = None
        q["ocultas"] = []
        q["pista_usada"] = False
        self.vista_quiz()

    def vista_resultado(self):
        q, est = self.q, self.estado
        total = len(q["preguntas"])
        aprobado = q["aciertos"] >= 2
        nuevo_pais = None
        if aprobado and q["idx"] == est.max_pais and est.max_pais < len(PAISES) - 1:
            est.max_pais += 1
            nuevo_pais = PAISES[est.max_pais]["nombre"]
            est.guardar()

        mensaje = "¡Excelente!" if aprobado else "¡Sigue practicando!"
        detalle = [
            ft.Text(mensaje, size=26, weight=ft.FontWeight.W_900, color=VERDE_OSCURO),
            ft.Text(f"Acertaste {q['aciertos']} de {total}", size=16, color=VERDE_OSCURO),
            ft.Text(f"+{q['aciertos'] * PUNTOS_POR_ACIERTO} pts   +{q['aciertos'] * XP_POR_ACIERTO} XP",
                    size=14, weight=ft.FontWeight.W_800, color="#E09A00"),
        ]
        if nuevo_pais:
            detalle.append(ft.Text(f"¡Desbloqueaste {nuevo_pais}!", size=14, weight=ft.FontWeight.W_800, color=VERDE))

        contenido = ft.Column(
            [
                ft.Container(expand=1),
                self.mapi(90),
                ft.Container(height=10),
                self.tarjeta(ft.Column(detalle, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
                             padding=22, ancho=320),
                ft.Container(height=14),
                self.boton("Repetir", ft.Icons.REFRESH, lambda e: self.iniciar_quiz(q["idx"], q["tipo"]), principal=True),
                self.boton("Volver al mapa", ft.Icons.MAP, self.vista_mapa),
                ft.Container(expand=2),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10,
        )
        self.mostrar(self.fondo(contenido, olas=True))

    # ---------------------------------------------------------- 5. TIENDA
    def vista_tienda(self, e=None):
        est = self.estado

        cabecera = ft.Row(
            [
                self.boton_redondo(ft.Icons.ARROW_BACK_IOS_NEW, self.vista_mapa, size=38),
                ft.Text("Tienda", size=22, weight=ft.FontWeight.W_900, color=VERDE_OSCURO),
                ft.Container(
                    ft.Row([ft.Icon(ft.Icons.STAR, color=AMARILLO, size=16),
                            ft.Text(f"{est.puntos} pts", size=12, weight=ft.FontWeight.W_800, color=VERDE_OSCURO)],
                           spacing=4, tight=True),
                    padding=ft.padding.symmetric(horizontal=12, vertical=7), bgcolor=BLANCO,
                    border_radius=20, shadow=SOMBRA,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        bienvenida = self.tarjeta(
            ft.Row(
                [
                    ft.Container(self.mapi(46), padding=ft.padding.only(top=12)),
                    ft.Column(
                        [ft.Text("¡Bienvenido a la tienda!", size=14, weight=ft.FontWeight.W_800, color=VERDE_OSCURO),
                         ft.Text("Compra accesorios, ayudas y temas con tus puntos.", size=10, color="#5C6B62")],
                        spacing=2, expand=True,
                    ),
                ],
                spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(left=14, right=14, top=6, bottom=12),
        )

        def cambiar_tab(nombre):
            self.tab_tienda = nombre
            self.vista_tienda()

        tabs = ft.Container(
            ft.Row(
                [
                    ft.Container(
                        ft.Text(n, size=12, weight=ft.FontWeight.W_800,
                                color=BLANCO if n == self.tab_tienda else VERDE_OSCURO),
                        expand=True, height=34, alignment=ft.alignment.center, border_radius=14,
                        bgcolor=VERDE if n == self.tab_tienda else None, ink=True,
                        on_click=lambda e, n=n: cambiar_tab(n),
                    )
                    for n in ("Objetos", "Ayudas", "Temas")
                ],
                spacing=4,
            ),
            padding=4, bgcolor=BLANCO, border_radius=18, shadow=SOMBRA,
        )

        filas = []
        for it in [i for i in TIENDA if i["tab"] == self.tab_tienda]:
            filas.append(self.tarjeta(
                ft.Row(
                    [
                        ft.Container(ft.Text(it["emoji"], size=26), width=54, height=54, border_radius=14,
                                     bgcolor=it["color"], alignment=ft.alignment.center),
                        ft.Column(
                            [ft.Text(it["nombre"], size=14, weight=ft.FontWeight.W_800, color=VERDE_OSCURO),
                             ft.Text(it["desc"], size=10, color="#5C6B62")],
                            spacing=1, expand=True,
                        ),
                        self.boton_item(it),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=12,
            ))
        if self.tab_tienda == "Ayudas":
            filas.append(ft.Text(f"Tienes {est.pistas} pistas", size=12, color=VERDE_OSCURO,
                                 text_align=ft.TextAlign.CENTER, width=360))

        contenido = ft.Column(
            [
                ft.Container(
                    ft.Column(
                        [
                            cabecera,
                            ft.Text("Usa tus puntos para personalizar a Mapi", size=11, color=VERDE_OSCURO,
                                    text_align=ft.TextAlign.CENTER, width=360),
                            bienvenida,
                            tabs,
                            ft.Text(f"{self.tab_tienda} destacados", size=13, weight=ft.FontWeight.W_800,
                                    color=VERDE_OSCURO),
                            ft.Column(filas, spacing=10),
                        ],
                        spacing=12,
                    ),
                    padding=ft.padding.only(left=16, right=16, top=16, bottom=110),
                ),
            ],
            scroll=ft.ScrollMode.AUTO, expand=True,
        )
        self.mostrar(self.fondo(contenido, olas=True))

    def boton_item(self, it):
        est = self.estado
        comprado = it["id"] in est.comprados
        tipo = it["tipo"]
        if tipo == "equipo" and comprado:
            puesto = est.equipado == it["id"]
            texto, bg, accion = ("Puesto", GRIS, lambda e: self.equipar(it, False)) if puesto \
                else ("Poner", VERDE_MEDIO, lambda e: self.equipar(it, True))
        elif tipo == "tema" and comprado:
            puesto = est.tema == it["id"]
            texto, bg, accion = ("En uso", GRIS, lambda e: self.equipar(it, False)) if puesto \
                else ("Usar", VERDE_MEDIO, lambda e: self.equipar(it, True))
        else:
            texto, bg, accion = f"{it['precio']} pts", VERDE, lambda e: self.comprar(it)
        return ft.Container(
            ft.Text(texto, size=12, weight=ft.FontWeight.W_800, color=BLANCO),
            width=76, height=34, border_radius=12, bgcolor=bg, alignment=ft.alignment.center,
            ink=True, on_click=accion,
        )

    def comprar(self, it):
        est = self.estado
        if est.puntos < it["precio"]:
            self.aviso(f"Te faltan {it['precio'] - est.puntos} pts para comprar {it['nombre']}.")
            return
        est.puntos -= it["precio"]
        if it["tipo"] == "ayuda":
            est.pistas += 1
        else:
            est.comprados.append(it["id"])
            self.equipar(it, True, refrescar=False)
        est.guardar()
        self.vista_tienda()
        self.aviso(f"¡Compraste {it['nombre']}!")

    def equipar(self, it, poner, refrescar=True):
        est = self.estado
        if it["tipo"] == "equipo":
            est.equipado = it["id"] if poner else None
        elif it["tipo"] == "tema":
            est.tema = it["id"] if poner else "clasico"
        est.guardar()
        if refrescar:
            self.vista_tienda()


def main(page: ft.Page):
    App(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir=ASSETS_DIR)
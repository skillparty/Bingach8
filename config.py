"""
Archivo de configuración para el juego Bingacho
"""

# Configuración de la pantalla
WIDTH = 3456
HEIGHT = 2234
FULLSCREEN = True
TITLE = "Bingacho"

# Colores - Nueva paleta moderna
WHITE = (255, 255, 255)  # Blanco puro para fondo
BLACK = (0, 0, 0)        # Negro para algunos textos

# Nueva paleta de colores elegante y moderna
COLORS = {
    'BACKGROUND': (15, 23, 42),       # Slate 900 #0F172A
    'PRIMARY': (99, 102, 241),        # Indigo 500 #6366F1
    'SECONDARY': (236, 72, 153),      # Pink 500 #EC4899
    'ACCENT': (34, 197, 94),          # Green 500 #22C55E
    'HIGHLIGHT': (251, 191, 36),      # Amber 400 #FBBF24
    'WHITE': (248, 250, 252),         # Slate 50 #F8FAFC
    'BLACK': (15, 23, 42),            # Slate 900 #0F172A
    'GRAY': (100, 116, 139),          # Slate 500 #64748B
    'LIGHT_GRAY': (203, 213, 225),    # Slate 300 #CBD5E1
    'DARK_GRAY': (51, 65, 85)         # Slate 700 #334155
}

# Mapeo de colores para compatibilidad
BACKGROUND_COLOR = COLORS['BACKGROUND']
PRIMARY_COLOR = COLORS['PRIMARY']
SECONDARY_COLOR = COLORS['SECONDARY']
ACCENT_COLOR = COLORS['ACCENT']
HIGHLIGHT_COLOR = COLORS['HIGHLIGHT']
WHITE = COLORS['WHITE']
BLACK = COLORS['BLACK']
GRAY = COLORS['GRAY']
LIGHT_GRAY = COLORS['LIGHT_GRAY']
DARK_GRAY = COLORS['DARK_GRAY']

# Colores específicos para elementos del juego
BUTTON_COLOR = PRIMARY_COLOR
BUTTON_HOVER_COLOR = SECONDARY_COLOR
TEXT_COLOR = WHITE
SUBTITLE_COLOR = HIGHLIGHT_COLOR
BORDER_COLOR = ACCENT_COLOR
GLOW_COLOR = PRIMARY_COLOR
ALT_GLOW_COLOR = COLORS['ACCENT']
FRAME_COLOR = COLORS['PRIMARY']

# Sistema de colores para el juego
PRIMARY = PRIMARY_COLOR           # Indigo como color principal
PRIMARY_LIGHT = (130, 134, 251)  # Indigo más claro
PRIMARY_DARK = (70, 74, 171)     # Indigo más oscuro

SECONDARY = SECONDARY_COLOR       # Rosa como secundario
SECONDARY_LIGHT = (244, 114, 182) # Rosa más claro
SECONDARY_DARK = (190, 24, 93)    # Rosa más oscuro

# Acentos vibrantes para destacar elementos
ACCENT = ACCENT_COLOR        # Verde como acento
ACCENT_LIGHT = (100, 255, 100) # Verde más claro
ACCENT_DARK = (0, 200, 0)      # Verde más oscuro

# Fondos
BACKGROUND = BACKGROUND_COLOR    # Fondo azul oscuro
BACKGROUND_DARK = (10, 10, 15)  # Azul muy oscuro para contraste

# Colores para los rangos del tablero y el historial
PRIMARY_LIGHT = (130, 134, 251)  # Definición explícita del color Indigo claro
RANGE_1_30 = PRIMARY_LIGHT        # Indigo claro para números 1-30
RANGE_31_60 = HIGHLIGHT_COLOR    # Ámbar para números 31-60
RANGE_61_90 = SECONDARY_COLOR    # Rosa para números 61-90

# Colores para estados de UI
DISABLED = (156, 163, 175)   # Gris para botones deshabilitados
HOVER = (255, 235, 205)      # Tono claro anaranjado para hover
SELECTED = HIGHLIGHT_COLOR   # Ámbar para selecciones

# Colores tradicionales (mantener compatibilidad)
RED = (239, 68, 68)
GREEN = (34, 197, 94)
BLUE = (59, 130, 246)
YELLOW = (250, 204, 21)
PURPLE = (147, 51, 234)
ORANGE = (249, 115, 22)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
BACKGROUND_COLOR = (30, 30, 80)  # Fondo azul oscuro

# Carpetas del juego
AUDIO_FOLDER = "audios_wav"  # Carpeta con los archivos de audio WAV
AUDIO_FILE_FORMAT = "wav"    # Formato de los archivos de audio

# Configuración de las pelotas
BALL_RADIUS = 40
MAX_BOUNCES = 3
BOUNCE_DAMPING = 0.75      # Aumentado de 0.6 a 0.75 para rebotes más rápidos
GRAVITY = 1.0             # Aumentado significativamente para caída mucho más rápida
INITIAL_VELOCITY = 8.0    # Aumentado significativamente para velocidad inicial mucho mayor

# Configuración del tablero
BOARD_ROWS = 9
BOARD_COLS = 10
TOTAL_NUMBERS = 90
BOARD_TOP_MARGIN = 30  # Espacio desde arriba
BOARD_CELL_PADDING = 2  # Espacio entre celdas

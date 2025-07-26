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

# Paleta de colores profesional y moderna - Inspirada en diseño de software moderno
COLORS = {
    # Fondos y superficies
    'BACKGROUND': (13, 17, 23),       # GitHub Dark #0D1117
    'SURFACE': (22, 27, 34),          # GitHub Dark Surface #161B22
    'SURFACE_ELEVATED': (33, 38, 45), # Superficie elevada #21262D
    
    # Colores primarios - Azul profesional
    'PRIMARY': (88, 166, 255),        # Azul GitHub #58A6FF
    'PRIMARY_HOVER': (116, 184, 255), # Azul hover #74B8FF
    'PRIMARY_DARK': (56, 139, 253),   # Azul oscuro #388BFD
    
    # Colores secundarios - Verde éxito
    'SUCCESS': (63, 185, 80),         # Verde GitHub #3FB950
    'SUCCESS_HOVER': (82, 196, 94),   # Verde hover #52C45E
    'SUCCESS_MUTED': (46, 160, 67),   # Verde apagado #2EA043
    
    # Colores de acento - Naranja/Ámbar
    'ACCENT': (255, 184, 0),          # Ámbar profesional #FFB800
    'ACCENT_HOVER': (255, 196, 37),   # Ámbar hover #FFC425
    'WARNING': (255, 149, 0),         # Naranja advertencia #FF9500
    
    # Colores de error/peligro
    'DANGER': (248, 81, 73),          # Rojo GitHub #F85149
    'DANGER_HOVER': (255, 108, 96),   # Rojo hover #FF6C60
    
    # Textos
    'TEXT_PRIMARY': (248, 248, 242),  # Texto principal #F8F8F2
    'TEXT_SECONDARY': (139, 148, 158), # Texto secundario #8B949E
    'TEXT_MUTED': (110, 118, 129),    # Texto apagado #6E7681
    'TEXT_INVERSE': (13, 17, 23),     # Texto inverso #0D1117
    
    # Bordes y separadores
    'BORDER': (48, 54, 61),           # Borde sutil #30363D
    'BORDER_MUTED': (33, 38, 45),     # Borde muy sutil #21262D
    
    # Estados especiales
    'HIGHLIGHT': (255, 235, 59),      # Amarillo resaltado #FFEB3B
    'GLOW': (88, 166, 255, 128),      # Brillo azul con alpha
    'SHADOW': (0, 0, 0, 64),          # Sombra sutil
}

# Mapeo de colores para compatibilidad con código existente
BACKGROUND_COLOR = COLORS['BACKGROUND']
PRIMARY_COLOR = COLORS['PRIMARY']
SECONDARY_COLOR = COLORS['SUCCESS']
ACCENT_COLOR = COLORS['ACCENT']
HIGHLIGHT_COLOR = COLORS['ACCENT']
WHITE = COLORS['TEXT_PRIMARY']
BLACK = COLORS['TEXT_INVERSE']
GRAY = COLORS['TEXT_SECONDARY']
LIGHT_GRAY = COLORS['TEXT_MUTED']
DARK_GRAY = COLORS['SURFACE_ELEVATED']

# Colores específicos para elementos del juego - Renovados
BUTTON_COLOR = COLORS['PRIMARY']
BUTTON_HOVER_COLOR = COLORS['PRIMARY_HOVER']
TEXT_COLOR = COLORS['TEXT_PRIMARY']
SUBTITLE_COLOR = COLORS['TEXT_SECONDARY']
BORDER_COLOR = COLORS['BORDER']
GLOW_COLOR = COLORS['PRIMARY']
ALT_GLOW_COLOR = COLORS['ACCENT']
FRAME_COLOR = COLORS['SURFACE']

# Nuevos colores específicos para UI mejorada
UI_COLORS = {
    'CARD_BACKGROUND': COLORS['SURFACE'],
    'CARD_BORDER': COLORS['BORDER'],
    'CARD_HOVER': COLORS['SURFACE_ELEVATED'],
    'BUTTON_SUCCESS': COLORS['SUCCESS'],
    'BUTTON_SUCCESS_HOVER': COLORS['SUCCESS_HOVER'],
    'BUTTON_WARNING': COLORS['WARNING'],
    'BUTTON_DANGER': COLORS['DANGER'],
    'NUMBER_1_30': COLORS['SUCCESS'],      # Verde para 1-30
    'NUMBER_31_60': COLORS['ACCENT'],      # Ámbar para 31-60  
    'NUMBER_61_90': COLORS['PRIMARY'],     # Azul para 61-90
    'CURRENT_NUMBER': COLORS['HIGHLIGHT'], # Amarillo para número actual
}

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

# Colores para los rangos del tablero y el historial - Actualizados
RANGE_1_30 = UI_COLORS['NUMBER_1_30']    # Verde para números 1-30
RANGE_31_60 = UI_COLORS['NUMBER_31_60']  # Ámbar para números 31-60
RANGE_61_90 = UI_COLORS['NUMBER_61_90']  # Azul para números 61-90

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

# Configuración de tipografía
FONTS = {
    'PRIMARY': 'JetBrains Mono',      # Fuente principal
    'FALLBACK': ['Monaco', 'Consolas', 'Courier New', 'monospace'],  # Fuentes de respaldo
    'SIZES': {
        'TITLE': 120,        # Títulos principales
        'SUBTITLE': 48,      # Subtítulos
        'HEADING': 36,       # Encabezados
        'BODY': 24,          # Texto normal
        'SMALL': 18,         # Texto pequeño
        'TINY': 14,          # Texto muy pequeño
        'NUMBER_LARGE': 72,  # Números grandes (número actual)
        'NUMBER_MEDIUM': 32, # Números medianos (tablero)
        'NUMBER_SMALL': 20,  # Números pequeños (historial)
    }
}

# Carpetas del juego
AUDIO_FOLDER = "audios_wav"  # Carpeta con los archivos de audio WAV
AUDIO_FILE_FORMAT = "wav"    # Formato de los archivos de audio

# Función para cargar fuentes con fallbacks
def get_font(size, bold=False):
    """
    Carga JetBrains Mono con fallbacks automáticos
    """
    import pygame
    
    # Lista de fuentes a probar en orden de preferencia
    font_names = [FONTS['PRIMARY']] + FONTS['FALLBACK']
    
    for font_name in font_names:
        try:
            if font_name == 'JetBrains Mono':
                # Intentar cargar JetBrains Mono desde el sistema
                font = pygame.font.SysFont(font_name, size, bold=bold)
                if font.get_ascent() > 0:  # Verificar que la fuente se cargó correctamente
                    return font
            else:
                # Cargar fuentes de fallback
                font = pygame.font.SysFont(font_name, size, bold=bold)
                if font.get_ascent() > 0:
                    return font
        except:
            continue
    
    # Si ninguna fuente funciona, usar la fuente por defecto de pygame
    return pygame.font.Font(None, size)

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

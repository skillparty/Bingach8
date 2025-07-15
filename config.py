"""
Archivo de configuración para el juego Bingacho
"""

# Configuración de la pantalla
WIDTH = 1024
HEIGHT = 768
TITLE = "Bingacho"

# Colores (esquema retro Vegas con paleta moderna)
WHITE = (255, 255, 255)  # Blanco puro para fondo
BLACK = (0, 0, 0)        # Negro para algunos textos

# Colores principales - paleta sugerida
VEGAS_RED = (40, 0, 0)    # Rojo oscuro profundo
VEGAS_GOLD = (255, 215, 0)  # Dorado brillante
VEGAS_YELLOW = (255, 255, 0)  # Amarillo
VEGAS_SILVER = (192, 192, 192)  # Plateado
VEGAS_WHITE = (255, 255, 255)  # Blanco
VEGAS_ORANGE = (255, 165, 0)  # Naranja

# Referencias directas para el código
BUTTON_COLOR = (180, 0, 0)  # Rojo brillante para botones
BUTTON_HOVER_COLOR = (220, 60, 0)  # Naranja rojizo para hover de botones
GLOW_COLOR = VEGAS_GOLD     # Dorado para brillos
ALT_GLOW_COLOR = VEGAS_YELLOW  # Amarillo para brillos alternativos
BORDER_COLOR = VEGAS_ORANGE  # Naranja para bordes
FRAME_COLOR = VEGAS_SILVER  # Plateado para marcos
TEXT_COLOR = WHITE          # Blanco para texto

# Sistema de colores para el juego
PRIMARY = VEGAS_RED           # Color principal
PRIMARY_LIGHT = (180, 0, 0) # Rojo más claro
PRIMARY_DARK = (20, 0, 0)   # Rojo más oscuro

SECONDARY = VEGAS_WHITE   # Color secundario
SECONDARY_LIGHT = (249, 250, 251) # Casi blanco
SECONDARY_DARK = (209, 213, 219) # Gris un poco más oscuro

# Acentos vibrantes para destacar elementos
ACCENT = VEGAS_GOLD          # Dorado para acentos importantes
ACCENT_LIGHT = (253, 230, 138) # Dorado más claro
ACCENT_DARK = (217, 119, 6)   # Dorado más oscuro

# Fondos
BACKGROUND = WHITE           # Fondo blanco limpio
BACKGROUND_DARK = (15, 23, 42) # Azul muy oscuro para contraste

# Colores por rangos de números - nueva paleta Vegas
RANGE_1_30 = PRIMARY_LIGHT     # Rojo para números 1-30
RANGE_31_60 = VEGAS_GOLD      # Dorado para números 31-60
RANGE_61_90 = VEGAS_ORANGE    # Naranja para números 61-90

# Colores para estados de UI
DISABLED = VEGAS_SILVER      # Plateado para botones deshabilitados
HOVER = (255, 235, 205)      # Tono claro anaranjado para hover
SELECTED = VEGAS_GOLD         # Dorado para selecciones

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
BOUNCE_DAMPING = 0.6
GRAVITY = 0.2
INITIAL_VELOCITY = 2

# Configuración del tablero
BOARD_ROWS = 9
BOARD_COLS = 10
TOTAL_NUMBERS = 90
BOARD_TOP_MARGIN = 30  # Espacio desde arriba
BOARD_CELL_PADDING = 2  # Espacio entre celdas

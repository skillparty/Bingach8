#Escrito y dirigido por Alejandro Rollano
#Fecha de creación: 01/07/2025
#Fecha de última modificación: 14/07/2025

import os
import sys
import random
import pygame
from pygame.locals import *
import math
import threading
import base64

# Importar configuración
import config as cfg

# Importar pantalla de título
from title_screen import TitleScreen

# Importar módulos multijugador
from mode_selection import ModeSelection
from multiplayer_manager import get_multiplayer_manager, reset_multiplayer_manager
from bingo_card_renderer import BingoCardRenderer

# Variables para manejo de escala y responsividad
global SCALE_X, SCALE_Y
SCALE_X = 1.0  # Factor de escala horizontal
SCALE_Y = 1.0  # Factor de escala vertical
BASE_WIDTH = 1024  # Ancho base de diseño
BASE_HEIGHT = 768  # Alto base de diseño

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
if hasattr(cfg, 'FULLSCREEN') and cfg.FULLSCREEN:
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pygame.display.set_caption(cfg.TITLE)

# Cargar imágenes de fondo
background_images = []
background_filenames = ["background.png", "background_dos.png", "background_tres.png"]

for bg_file in background_filenames:
    try:
        img = pygame.image.load(f"imagenes/{bg_file}").convert()
        # Escalar la imagen para que cubra toda la pantalla
        img = pygame.transform.scale(img, (cfg.WIDTH, cfg.HEIGHT))
        background_images.append(img)
    except pygame.error as e:
        print(f"Error al cargar la imagen de fondo {bg_file}: {e}")

# Si no se pudo cargar ninguna imagen, background_images estará vacío
if not background_images:
    print("No se pudo cargar ninguna imagen de fondo")

# Variable para seguir el índice de la imagen actual
current_background_index = 0

# Calcular factores de escala basados en la resolución actual
SCALE_X = cfg.WIDTH / BASE_WIDTH
SCALE_Y = cfg.HEIGHT / BASE_HEIGHT

# Sistema de escalado inteligente y adaptativo
def scale_value(value, is_horizontal=True, min_value=None, max_value=None):
    """
    Escala valores de forma inteligente según la resolución
    
    Args:
        value: Valor base a escalar
        is_horizontal: Si es dimensión horizontal (True) o vertical (False)
        min_value: Valor mínimo permitido después del escalado
        max_value: Valor máximo permitido después del escalado
    """
    if is_horizontal:
        scaled = int(value * SCALE_X)
    else:
        scaled = int(value * SCALE_Y)
    
    # Aplicar límites si se especifican
    if min_value is not None:
        scaled = max(scaled, min_value)
    if max_value is not None:
        scaled = min(scaled, max_value)
    
    return scaled

def get_responsive_layout():
    """
    Determina el layout óptimo según la resolución actual
    """
    aspect_ratio = cfg.WIDTH / cfg.HEIGHT
    
    # Clasificar el tipo de pantalla
    if aspect_ratio > 2.0:
        layout_type = "ultrawide"
    elif aspect_ratio > 1.6:
        layout_type = "widescreen"
    elif aspect_ratio > 1.2:
        layout_type = "standard"
    else:
        layout_type = "portrait"
    
    # Determinar tamaño de pantalla
    total_pixels = cfg.WIDTH * cfg.HEIGHT
    if total_pixels > 6000000:  # > 6MP (ej: 4K)
        size_category = "large"
    elif total_pixels > 2000000:  # > 2MP (ej: 1080p)
        size_category = "medium"
    else:
        size_category = "small"
    
    return {
        "type": layout_type,
        "size": size_category,
        "aspect_ratio": aspect_ratio,
        "is_high_res": total_pixels > 4000000,
        "scale_factor": min(SCALE_X, SCALE_Y)  # Factor de escala conservador
    }

# Función para escalar una posición (x,y)
def scale_pos(pos):
    return (scale_value(pos[0]), scale_value(pos[1], False))

# Función para escalar un rectángulo 
def scale_rect(x, y, width, height):
    return pygame.Rect(
        scale_value(x), 
        scale_value(y, False),
        scale_value(width),
        scale_value(height, False)
    )

# Colores - usar desde config
WHITE = cfg.WHITE
BLACK = cfg.BLACK
RED = cfg.RED
GREEN = cfg.GREEN
BLUE = cfg.BLUE
YELLOW = cfg.YELLOW
PURPLE = cfg.PURPLE
ORANGE = cfg.ORANGE
COLORS = cfg.COLORS

# Fuentes - usando tipografía sans-serif moderna (similar a Inter)
font_names = ['Arial', 'Helvetica', 'sans-serif']

# Variables globales para las fuentes
font_big = None
font_medium = None
font_small = None
font_smallest = None
fonts = {}

# Función para cargar fuentes con tamaño responsivo
def get_adaptive_config():
    """
    Obtiene configuración adaptativa según la resolución y layout usando config.py
    """
    # Usar la configuración de resolución del config.py
    resolution_config = cfg.get_resolution_config()
    layout = get_responsive_layout()
    
    # Configuraciones base mejoradas según el tipo de pantalla
    configs = {
        "ultrawide": {
            "board_cell_size": resolution_config["board_cell_size"] + 15,  # Mucho más grande
            "history_width_ratio": 0.16,
            "current_number_size": resolution_config["current_number_size"] + 40,
            "button_height": 80,
            "spacing_multiplier": resolution_config["spacing_multiplier"] + 0.2,
            "title_margin": resolution_config["title_margin"] + 20,
            "board_margin_top": resolution_config["board_margin_top"] + 40
        },
        "widescreen": {
            "board_cell_size": resolution_config["board_cell_size"] + 10,  # Mucho más grande
            "history_width_ratio": 0.20,
            "current_number_size": resolution_config["current_number_size"] + 20,
            "button_height": 75,
            "spacing_multiplier": resolution_config["spacing_multiplier"] + 0.1,
            "title_margin": resolution_config["title_margin"] + 10,
            "board_margin_top": resolution_config["board_margin_top"] + 20
        },
        "standard": {
            "board_cell_size": resolution_config["board_cell_size"],  # Usar tamaño base mejorado
            "history_width_ratio": 0.22,
            "current_number_size": resolution_config["current_number_size"],
            "button_height": 70,
            "spacing_multiplier": resolution_config["spacing_multiplier"],
            "title_margin": resolution_config["title_margin"],
            "board_margin_top": resolution_config["board_margin_top"]
        },
        "portrait": {
            "board_cell_size": max(40, resolution_config["board_cell_size"] - 5),  # Mínimo 40px
            "history_width_ratio": 0.25,
            "current_number_size": max(140, resolution_config["current_number_size"] - 20),
            "button_height": 65,
            "spacing_multiplier": max(0.7, resolution_config["spacing_multiplier"] - 0.1),
            "title_margin": max(50, resolution_config["title_margin"] - 10),
            "board_margin_top": max(140, resolution_config["board_margin_top"] - 20)
        }
    }
    
    base_config = configs[layout["type"]]
    
    # Ajustar según el tamaño de pantalla con multiplicadores más agresivos
    size_multipliers = {
        "large": 1.3,   # Aumentado de 1.2 a 1.3
        "medium": 1.0,
        "small": 0.85   # Aumentado de 0.8 a 0.85
    }
    
    multiplier = size_multipliers[layout["size"]]
    
    # Aplicar multiplicador
    adaptive_config = {}
    for key, value in base_config.items():
        if key.endswith("_ratio"):
            adaptive_config[key] = value  # Los ratios no se escalan
        else:
            adaptive_config[key] = int(value * multiplier)
    
    return adaptive_config

def load_responsive_fonts():
    """Carga las fuentes con JetBrains Mono y tamaños adaptados a la resolución actual"""
    global font_big, font_medium, font_small, font_smallest, fonts
    
    # Usar JetBrains Mono para una apariencia profesional y moderna
    font_big = cfg.get_font(scale_value(cfg.FONTS['SIZES']['NUMBER_LARGE']), bold=True)
    font_medium = cfg.get_font(scale_value(cfg.FONTS['SIZES']['HEADING']), bold=True)
    font_small = cfg.get_font(scale_value(cfg.FONTS['SIZES']['BODY']))
    font_smallest = cfg.get_font(scale_value(cfg.FONTS['SIZES']['SMALL']))
    
    # Diccionario de fuentes adicionales con JetBrains Mono
    fonts = {
        "title": cfg.get_font(scale_value(cfg.FONTS['SIZES']['TITLE']), bold=True),
        "title_small": cfg.get_font(scale_value(cfg.FONTS['SIZES']['SUBTITLE']), bold=True),
        "button": cfg.get_font(scale_value(cfg.FONTS['SIZES']['BODY']), bold=True),
        "timer": cfg.get_font(scale_value(cfg.FONTS['SIZES']['HEADING']), bold=True),
        "bingo": cfg.get_font(scale_value(cfg.FONTS['SIZES']['TITLE']), bold=True),
        "number_large": cfg.get_font(scale_value(cfg.FONTS['SIZES']['NUMBER_LARGE']), bold=True),
        "number_medium": cfg.get_font(scale_value(cfg.FONTS['SIZES']['NUMBER_MEDIUM']), bold=True),
        "number_small": cfg.get_font(scale_value(cfg.FONTS['SIZES']['NUMBER_SMALL']))
    }

# Cargar fuentes iniciales
load_responsive_fonts()

# Estado del juego
class TooltipManager:
    """Maneja tooltips informativos"""
    
    def __init__(self):
        self.active_tooltip = None
        self.tooltip_timer = 0
        self.show_delay = 800  # ms antes de mostrar tooltip
        self.fade_duration = 200  # ms para fade in/out
        
    def set_tooltip(self, text, position, delay=None):
        """Establece un tooltip para mostrar"""
        if delay is None:
            delay = self.show_delay
            
        self.active_tooltip = {
            'text': text,
            'position': position,
            'start_time': pygame.time.get_ticks(),
            'delay': delay,
            'visible': False,
            'alpha': 0
        }
    
    def clear_tooltip(self):
        """Limpia el tooltip actual"""
        if self.active_tooltip:
            self.active_tooltip['visible'] = False
    
    def update(self):
        """Actualiza el estado del tooltip"""
        if not self.active_tooltip:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.active_tooltip['start_time']
        
        if elapsed >= self.active_tooltip['delay'] and not self.active_tooltip['visible']:
            self.active_tooltip['visible'] = True
            
        if self.active_tooltip['visible']:
            # Fade in
            fade_progress = min(1.0, (elapsed - self.active_tooltip['delay']) / self.fade_duration)
            self.active_tooltip['alpha'] = int(255 * fade_progress)
    
    def draw(self, screen):
        """Dibuja el tooltip si está activo"""
        if not self.active_tooltip or not self.active_tooltip['visible'] or self.active_tooltip['alpha'] <= 0:
            return
            
        tooltip = self.active_tooltip
        text = tooltip['text']
        pos = tooltip['position']
        alpha = tooltip['alpha']
        
        # Configuración del tooltip
        padding = scale_value(12)
        corner_radius = scale_value(6)
        font = fonts["number_small"]
        
        # Renderizar texto
        text_surface = font.render(text, True, cfg.TEXT_COLOR)
        text_rect = text_surface.get_rect()
        
        # Calcular dimensiones del tooltip
        tooltip_width = text_rect.width + padding * 2
        tooltip_height = text_rect.height + padding * 2
        
        # Posicionar tooltip (evitar bordes de pantalla)
        tooltip_x = pos[0] - tooltip_width // 2
        tooltip_y = pos[1] - tooltip_height - scale_value(10)
        
        # Ajustar si se sale de la pantalla
        if tooltip_x < scale_value(10):
            tooltip_x = scale_value(10)
        elif tooltip_x + tooltip_width > cfg.WIDTH - scale_value(10):
            tooltip_x = cfg.WIDTH - tooltip_width - scale_value(10)
            
        if tooltip_y < scale_value(10):
            tooltip_y = pos[1] + scale_value(10)
        
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        
        # Crear superficie con alpha
        tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        
        # Fondo del tooltip
        bg_color = (*cfg.DARK_GRAY[:3], min(220, alpha))
        draw_rounded_rect(tooltip_surface, bg_color, 
                         pygame.Rect(0, 0, tooltip_width, tooltip_height), corner_radius)
        
        # Borde del tooltip
        border_color = (*cfg.BORDER_COLOR[:3], alpha)
        draw_rounded_rect_outline(tooltip_surface, border_color,
                                pygame.Rect(0, 0, tooltip_width, tooltip_height), corner_radius, 1)
        
        # Texto del tooltip
        text_surface.set_alpha(alpha)
        text_pos = (padding, padding)
        tooltip_surface.blit(text_surface, text_pos)
        
        # Dibujar tooltip en pantalla
        screen.blit(tooltip_surface, tooltip_rect)

class TransitionManager:
    """Maneja transiciones suaves entre estados"""
    
    def __init__(self):
        self.transitions = {}
        self.easing_functions = {
            'linear': lambda t: t,
            'ease_in': lambda t: t * t,
            'ease_out': lambda t: 1 - (1 - t) * (1 - t),
            'ease_in_out': lambda t: 2 * t * t if t < 0.5 else 1 - 2 * (1 - t) * (1 - t),
            'bounce': lambda t: 1 - abs(math.sin(t * math.pi * 2)) * (1 - t)
        }
    
    def start_transition(self, name, start_value, end_value, duration, easing='ease_out'):
        """Inicia una nueva transición"""
        self.transitions[name] = {
            'start_value': start_value,
            'end_value': end_value,
            'duration': duration,
            'start_time': pygame.time.get_ticks(),
            'easing': easing,
            'active': True
        }
    
    def get_value(self, name, default=0):
        """Obtiene el valor actual de una transición"""
        if name not in self.transitions:
            return default
        
        transition = self.transitions[name]
        if not transition['active']:
            return transition['end_value']
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - transition['start_time']
        progress = min(1.0, elapsed / transition['duration'])
        
        if progress >= 1.0:
            transition['active'] = False
            return transition['end_value']
        
        # Aplicar función de easing
        eased_progress = self.easing_functions[transition['easing']](progress)
        
        # Interpolar entre valores
        start = transition['start_value']
        end = transition['end_value']
        
        if isinstance(start, (int, float)):
            return start + (end - start) * eased_progress
        elif isinstance(start, tuple):  # Para colores RGB
            return tuple(int(start[i] + (end[i] - start[i]) * eased_progress) for i in range(len(start)))
        
        return end
    
    def is_active(self, name):
        """Verifica si una transición está activa"""
        return name in self.transitions and self.transitions[name]['active']

class GameState:
    def __init__(self):
        self.running = True
        self.show_title_screen = True
        self.show_mode_selection = False  # Nueva: pantalla de selección de modo
        self.game_started = False
        self.game_over = False
        self.board = [[None for _ in range(cfg.BOARD_COLS)] for _ in range(cfg.BOARD_ROWS)]
        self.current_number = None
        self.drawn_numbers = set()
        self.balls = []
        self.bingo_called = False
        
        # Variables para animaciones y efectos visuales
        self.bingo_animation_start = 0
        self.bingo_animation_duration = 2500  # 2.5 segundos (velocidad x2)
        self.bingo_animation_scale = 1.0
        self.bingo_animation_rotation = 0
        self.bingo_animation_active = False
        
        # Variables para nuevas animaciones
        self.number_animation_start = 0
        self.number_animation_duration = 500  # 0.5 segundos (velocidad x2)
        self.number_animation_active = False
        self.number_scale = 1.0
        self.button_hover = None  # Para efecto hover en botones
        self.show_confetti = False  # Para animación de confeti al ganar
        self.confetti_particles = []  # Para partículas de confeti
        self.start_time = pygame.time.get_ticks()  # Para cronometrar el juego
        
        # Inicialización del tablero
        self.initialize_board()
        
        # Sistema de transiciones y tooltips
        self.transitions = TransitionManager()
        self.tooltips = TooltipManager()
    
    def initialize_board(self):
        # Inicializar el tablero con los números según el modo de juego
        num = 1
        for row in range(cfg.BOARD_ROWS):
            for col in range(cfg.BOARD_COLS):
                if num <= cfg.TOTAL_NUMBERS:
                    self.board[row][col] = num
                    num += 1

game_state = GameState()

# Crear instancia de la pantalla de título
title_screen = TitleScreen(screen)
title_screen.start_animation()

# Crear instancia del selector de modo
mode_selection = ModeSelection(screen)

# Obtener gestor multijugador
multiplayer_manager = get_multiplayer_manager()

# Clase para las pelotas
class Ball:
    # Variable estática para rastrear la posición horizontal de la última bola
    last_ball_x = scale_value(cfg.BALL_RADIUS + 10)  # Margen izquierdo inicial escalado
    # Posición inicial de la fila (parte inferior de la pantalla)
    row_y = cfg.HEIGHT - scale_value(80, False)  # Borde inferior menos margen escalado
    
    # Método para reiniciar las posiciones estáticas
    @classmethod
    def reset_positions(cls):
        cls.last_ball_x = scale_value(cfg.BALL_RADIUS + 10)
        cls.row_y = cfg.HEIGHT - scale_value(80, False)
    
    def __init__(self, number):
        self.number = number
        self.radius = scale_value(cfg.BALL_RADIUS - 3)  # Pelotas escaladas
        
        # Calcular posición final en la "estantería" de izquierda a derecha, desde abajo hacia arriba
        self.final_x = Ball.last_ball_x
        self.final_y = Ball.row_y  # Altura en la parte inferior
        
        # Actualizar la posición para la próxima pelota (con espaciado)
        Ball.last_ball_x += self.radius * 2 + scale_value(6)  # Espacio entre pelotas
        
        # Cuando llegamos al borde, pasamos a la siguiente fila hacia arriba
        if Ball.last_ball_x > cfg.WIDTH - self.radius - scale_value(10):
            Ball.last_ball_x = scale_value(cfg.BALL_RADIUS + 10)  # Reiniciar a la izquierda
            Ball.row_y -= self.radius * 2 + scale_value(5)  # Subir a la siguiente fila (hacia arriba)
            self.final_y = Ball.row_y
            
        # Posición inicial (para animación de caída)
        self.x = self.final_x
        self.y = -self.radius * 2  # Comienza arriba de la pantalla
        self.velocity_y = cfg.INITIAL_VELOCITY * 1.5  # Velocidad inicial más rápida
        
        # Determinar colores según el rango del número y la nueva paleta retro Vegas
        if cfg.TOTAL_NUMBERS == 90:
            # Modo normal: rangos 1-30, 31-60, 61-90
            if self.number <= 30:
                self.color = cfg.BUTTON_COLOR
                self.border_color = (200, 0, 0)
                self.text_color = cfg.TEXT_COLOR
            elif self.number <= 60:
                self.color = cfg.GLOW_COLOR
                self.border_color = (200, 160, 0)
                self.text_color = cfg.BLACK
            else:
                self.color = cfg.BORDER_COLOR
                self.border_color = (200, 80, 0)
                self.text_color = cfg.TEXT_COLOR
        else:
            # Modo alterno: rangos 1-25, 26-50, 51-75
            if self.number <= 25:
                self.color = cfg.BUTTON_COLOR
                self.border_color = (200, 0, 0)
                self.text_color = cfg.TEXT_COLOR
            elif self.number <= 50:
                self.color = cfg.GLOW_COLOR
                self.border_color = (200, 160, 0)
                self.text_color = cfg.BLACK
            else:
                self.color = cfg.BORDER_COLOR
                self.border_color = (200, 80, 0)
                self.text_color = cfg.TEXT_COLOR
        
        self.falling = True
        self.played_audio = False
        self.bounce_count = 0
        self.max_bounces = 1  # Menos rebotes para animación más rápida
    
    def update(self):
        if self.falling:
            # Simular gravedad con movimiento más directo
            self.velocity_y += cfg.GRAVITY * 1.2
            self.y += self.velocity_y
            
            # Rebote cuando alcanza la posición final
            if self.y + self.radius > self.final_y:
                self.y = self.final_y - self.radius
                self.velocity_y = -self.velocity_y * cfg.BOUNCE_DAMPING
                self.bounce_count += 1
                
                # Después de algunos rebotes, la pelota se detiene
                if self.bounce_count >= self.max_bounces:
                    self.falling = False
                    self.y = self.final_y - self.radius  # Asegurar posición exacta
                    self.play_audio()
    
    def draw(self):
        # Dibujo con estilo retro Vegas
        # Círculo con borde más grueso para efecto neón
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, self.border_color, (int(self.x), int(self.y)), self.radius, scale_value(2))
        
        # Efecto de brillo interior sutil
        inner_radius = self.radius - scale_value(4)
        if inner_radius > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), inner_radius)
        
        # Número con el color de texto adecuado para contraste
        number_text = font_small.render(str(self.number), True, self.text_color)
        text_rect = number_text.get_rect(center=(self.x, self.y))
        screen.blit(number_text, text_rect)
    
    def play_audio(self):
        if not self.played_audio:
            self.played_audio = True
            # Reproducir el audio correspondiente al número en un hilo separado
            audio_thread = threading.Thread(target=self._play_audio_file)
            audio_thread.start()
    
    def _play_audio_file(self):
        try:
            # Armar la ruta del archivo de audio - corregida para usar carpetas y nombres existentes
            audio_file = f"{cfg.AUDIO_FOLDER}/numero_{self.number}.{cfg.AUDIO_FILE_FORMAT}"
            
            # Si el archivo existe, reproducirlo
            if os.path.isfile(audio_file):
                sound = pygame.mixer.Sound(audio_file)
                sound.play()
                self.played_audio = True
        except Exception as e:
            print(f"Error reproduciendo audio para el número {self.number}: {e}")

def draw_board():
    """Dibuja el tablero principal del bingo con diseño moderno y profesional."""
    # Obtener configuración adaptativa
    adaptive_config = get_adaptive_config()
    
    # Configuración responsiva del tablero con mejor escalado
    cell_size = scale_value(adaptive_config["board_cell_size"], min_value=50, max_value=120)  # Aumentado mínimo y máximo
    cell_spacing = scale_value(int(adaptive_config["board_cell_size"] * 0.12), min_value=5, max_value=18)  # Más espaciado
    corner_radius = scale_value(10, min_value=6, max_value=20)  # Bordes más redondeados
    
    # Calcular dimensiones del tablero
    board_width = cfg.BOARD_COLS * cell_size + (cfg.BOARD_COLS - 1) * cell_spacing
    board_height = cfg.BOARD_ROWS * cell_size + (cfg.BOARD_ROWS - 1) * cell_spacing
    
    # Posicionamiento centrado con margen superior mejorado para evitar superposición
    board_x = (cfg.WIDTH - board_width) // 2
    board_y = scale_value(adaptive_config["board_margin_top"], False, min_value=200, max_value=400)  # Usar margen del config
    
    # Contenedor del tablero con diseño moderno
    container_padding = scale_value(20)
    container_rect = pygame.Rect(
        board_x - container_padding,
        board_y - container_padding,
        board_width + container_padding * 2,
        board_height + container_padding * 2
    )
    
    # Sombra del contenedor
    shadow_rect = container_rect.copy()
    shadow_rect.x += scale_value(6)
    shadow_rect.y += scale_value(6)
    draw_rounded_rect(screen, (0, 0, 0, 32), shadow_rect, scale_value(12))
    
    # Fondo del contenedor
    draw_rounded_rect(screen, cfg.FRAME_COLOR, container_rect, scale_value(12))
    
    # Borde del contenedor
    draw_rounded_rect_outline(screen, cfg.BORDER_COLOR, container_rect, scale_value(12), scale_value(2))
    
    # Título del tablero moderno con mejor espaciado
    title_y = container_rect.top - scale_value(70, False, min_value=50, max_value=100)
    title_font = fonts["title_small"]
    title_text = title_font.render("TABLERO DE NÚMEROS", True, cfg.TEXT_COLOR)
    title_rect = title_text.get_rect(center=(container_rect.centerx, title_y))
    screen.blit(title_text, title_rect)
    

    
    # Dibujar celdas del tablero con diseño moderno
    for row in range(cfg.BOARD_ROWS):
        for col in range(cfg.BOARD_COLS):
            number = row * cfg.BOARD_COLS + col + 1
            
            if number <= cfg.TOTAL_NUMBERS:
                # Calcular posición de la celda
                cell_x = board_x + col * (cell_size + cell_spacing)
                cell_y = board_y + row * (cell_size + cell_spacing)
                cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
                
                # Determinar colores según el rango
                range_color, glow_color = get_number_color_and_glow(number)
                
                # Estado de la celda
                is_drawn = number in game_state.drawn_numbers
                is_current = number == game_state.current_number
                
                if is_drawn:
                    # Número ya sorteado - celda activa
                    if is_current:
                        # Número actual - efecto especial
                        current_time = pygame.time.get_ticks()
                        pulse = 0.8 + 0.2 * math.sin(current_time / 300)
                        
                        # Brillo pulsante alrededor
                        glow_rect = cell_rect.inflate(scale_value(8), scale_value(8))
                        glow_alpha = int(120 * pulse)
                        draw_rounded_rect(screen, (*glow_color[:3], glow_alpha), glow_rect, corner_radius + scale_value(2))
                        
                        # Fondo con color intenso
                        draw_rounded_rect(screen, range_color, cell_rect, corner_radius)
                        
                        # Borde brillante
                        draw_rounded_rect_outline(screen, cfg.HIGHLIGHT_COLOR, cell_rect, corner_radius, scale_value(3))
                        
                        # Texto con color contrastante
                        text_color = cfg.BLACK if range_color == cfg.ACCENT_COLOR else cfg.TEXT_COLOR
                    else:
                        # Número sorteado normal
                        # Fondo con color del rango
                        draw_rounded_rect(screen, range_color, cell_rect, corner_radius)
                        
                        # Borde sutil
                        draw_rounded_rect_outline(screen, cfg.BORDER_COLOR, cell_rect, corner_radius, scale_value(1))
                        
                        # Texto con color contrastante
                        text_color = cfg.BLACK if range_color == cfg.ACCENT_COLOR else cfg.TEXT_COLOR
                else:
                    # Número no sorteado - celda inactiva
                    # Fondo neutro
                    draw_rounded_rect(screen, cfg.DARK_GRAY, cell_rect, corner_radius)
                    
                    # Borde sutil
                    draw_rounded_rect_outline(screen, cfg.BORDER_COLOR, cell_rect, corner_radius, scale_value(1))
                    
                    # Texto apagado
                    text_color = cfg.GRAY
                
                # Renderizar número
                number_font = fonts["number_medium"]
                number_surface = number_font.render(str(number), True, text_color)
                number_rect = number_surface.get_rect(center=cell_rect.center)
                screen.blit(number_surface, number_rect)
                
                # Tooltip para celdas (solo si el mouse está sobre una celda)
                mouse_pos = pygame.mouse.get_pos()
                if cell_rect.collidepoint(mouse_pos):
                    if is_drawn:
                        if is_current:
                            tooltip_text = f"Número {number} - ¡ACTUAL!"
                        else:
                            tooltip_text = f"Número {number} - Ya sorteado"
                    else:
                        tooltip_text = f"Número {number} - Pendiente"
                    
                    game_state.tooltips.set_tooltip(tooltip_text, (cell_rect.centerx, cell_rect.top), delay=500)
    
    # Estadísticas del tablero
    drawn_count = len(game_state.drawn_numbers)
    remaining_count = cfg.TOTAL_NUMBERS - drawn_count
    progress_percentage = (drawn_count / cfg.TOTAL_NUMBERS) * 100
    
    # Barra de progreso moderna
    progress_bar_y = container_rect.bottom + scale_value(15, False)
    progress_bar_width = board_width
    progress_bar_height = scale_value(8, False)
    progress_bar_rect = pygame.Rect(board_x, progress_bar_y, progress_bar_width, progress_bar_height)
    
    # Fondo de la barra de progreso
    draw_rounded_rect(screen, cfg.DARK_GRAY, progress_bar_rect, scale_value(4))
    
    # Progreso actual
    if drawn_count > 0:
        progress_width = int(progress_bar_width * (drawn_count / cfg.TOTAL_NUMBERS))
        progress_rect = pygame.Rect(board_x, progress_bar_y, progress_width, progress_bar_height)
        draw_rounded_rect(screen, cfg.PRIMARY_COLOR, progress_rect, scale_value(4))
    
    # Texto de estadísticas
    stats_y = progress_bar_y + scale_value(25, False)
    stats_font = fonts["number_small"]
    
    # Números sorteados
    drawn_text = f"Sorteados: {drawn_count}"
    drawn_surface = stats_font.render(drawn_text, True, cfg.TEXT_COLOR)
    drawn_rect = drawn_surface.get_rect(left=board_x, centery=stats_y)
    screen.blit(drawn_surface, drawn_rect)
    
    # Porcentaje
    percentage_text = f"{progress_percentage:.1f}%"
    percentage_surface = stats_font.render(percentage_text, True, cfg.ACCENT_COLOR)
    percentage_rect = percentage_surface.get_rect(center=(container_rect.centerx, stats_y))
    screen.blit(percentage_surface, percentage_rect)
    
    # Números restantes
    remaining_text = f"Restantes: {remaining_count}"
    remaining_surface = stats_font.render(remaining_text, True, cfg.GRAY)
    remaining_rect = remaining_surface.get_rect(right=board_x + board_width, centery=stats_y)
    screen.blit(remaining_surface, remaining_rect)

def draw_buttons():
    """Dibuja los botones del juego con diseño moderno y profesional."""
    # Obtener configuración adaptativa
    adaptive_config = get_adaptive_config()
    
    # Configuración de botones con diseño más limpio
    btn_height = scale_value(adaptive_config["button_height"], False, min_value=40, max_value=80)
    corner_radius = scale_value(8, min_value=4, max_value=12)
    
    # Dimensiones y posiciones optimizadas
    start_btn_width = scale_value(280)
    side_btn_width = scale_value(120)
    bottom_margin = scale_value(80, False)
    button_spacing = scale_value(16)
    
    # Crear rectángulos para los botones con mejor espaciado
    start_button_rect = pygame.Rect(
        cfg.WIDTH // 2 - start_btn_width // 2,
        cfg.HEIGHT - bottom_margin, 
        start_btn_width, 
        btn_height
    )
    bingo_button_rect = pygame.Rect(
        cfg.WIDTH - side_btn_width - scale_value(24), 
        cfg.HEIGHT - bottom_margin, 
        side_btn_width, 
        btn_height
    )
    reset_button_rect = pygame.Rect(
        scale_value(24), 
        cfg.HEIGHT - bottom_margin, 
        side_btn_width, 
        btn_height
    )
    
    # Guardar los rectángulos para la detección de clicks
    game_state.buttons = {
        "start": start_button_rect,
        "bingo": bingo_button_rect,
        "reset": reset_button_rect
    }
    
    # Detectar hover states con transiciones y tooltips
    mouse_pos = pygame.mouse.get_pos()
    start_hover = start_button_rect.collidepoint(mouse_pos)
    bingo_hover = bingo_button_rect.collidepoint(mouse_pos)
    reset_hover = reset_button_rect.collidepoint(mouse_pos)
    
    # Gestionar tooltips
    if start_hover:
        tooltip_text = "Sortear siguiente número" if game_state.game_started else "Comenzar el juego"
        game_state.tooltips.set_tooltip(tooltip_text, (start_button_rect.centerx, start_button_rect.top))
    elif bingo_hover and game_state.game_started:
        game_state.tooltips.set_tooltip("¡Cantar BINGO!", (bingo_button_rect.centerx, bingo_button_rect.top))
    elif reset_hover:
        game_state.tooltips.set_tooltip("Reiniciar juego", (reset_button_rect.centerx, reset_button_rect.top))
    else:
        game_state.tooltips.clear_tooltip()
    
    # Gestionar transiciones de hover
    if start_hover and not game_state.transitions.is_active('start_hover'):
        game_state.transitions.start_transition('start_hover', 0.0, 1.0, 200, 'ease_out')
    elif not start_hover and not game_state.transitions.is_active('start_hover'):
        game_state.transitions.start_transition('start_hover', 1.0, 0.0, 200, 'ease_out')
    
    if bingo_hover and not game_state.transitions.is_active('bingo_hover'):
        game_state.transitions.start_transition('bingo_hover', 0.0, 1.0, 200, 'ease_out')
    elif not bingo_hover and not game_state.transitions.is_active('bingo_hover'):
        game_state.transitions.start_transition('bingo_hover', 1.0, 0.0, 200, 'ease_out')
    
    if reset_hover and not game_state.transitions.is_active('reset_hover'):
        game_state.transitions.start_transition('reset_hover', 0.0, 1.0, 200, 'ease_out')
    elif not reset_hover and not game_state.transitions.is_active('reset_hover'):
        game_state.transitions.start_transition('reset_hover', 1.0, 0.0, 200, 'ease_out')
    
    # ==== BOTÓN PRINCIPAL (INICIAR/SIGUIENTE) ====
    button_text = "INICIAR" if not game_state.game_started else "SIGUIENTE"
    
    # Colores según estado con transiciones suaves
    hover_intensity = game_state.transitions.get_value('start_hover', 0.0)
    
    # Interpolar colores
    normal_color = cfg.BUTTON_COLOR
    hover_color = cfg.BUTTON_HOVER_COLOR
    bg_color = tuple(int(normal_color[i] + (hover_color[i] - normal_color[i]) * hover_intensity) for i in range(3))
    
    shadow_color = (0, 0, 0, 64)
    shadow_offset = scale_value(4 - 2 * hover_intensity)
    
    # Sombra del botón
    shadow_rect = start_button_rect.copy()
    shadow_rect.x += shadow_offset
    shadow_rect.y += shadow_offset
    draw_rounded_rect(screen, shadow_color, shadow_rect, corner_radius)
    
    # Botón principal
    draw_rounded_rect(screen, bg_color, start_button_rect, corner_radius)
    
    # Borde sutil
    draw_rounded_rect_outline(screen, cfg.BORDER_COLOR, start_button_rect, corner_radius, scale_value(1))
    
    # Texto del botón
    text_surface = fonts["button"].render(button_text, True, cfg.TEXT_COLOR)
    text_rect = text_surface.get_rect(center=start_button_rect.center)
    screen.blit(text_surface, text_rect)
    
    # ==== BOTÓN BINGO ====
    # Color según estado del juego
    if game_state.game_started and not game_state.game_over:
        if bingo_hover:
            bg_color = cfg.SECONDARY_COLOR
        else:
            bg_color = cfg.ACCENT_COLOR
        text_color = cfg.TEXT_COLOR
    else:
        bg_color = cfg.FRAME_COLOR
        text_color = cfg.GRAY
    
    # Sombra del botón
    shadow_rect = bingo_button_rect.copy()
    shadow_rect.x += scale_value(2) if bingo_hover else scale_value(4)
    shadow_rect.y += scale_value(2) if bingo_hover else scale_value(4)
    draw_rounded_rect(screen, shadow_color, shadow_rect, corner_radius)
    
    # Botón BINGO
    draw_rounded_rect(screen, bg_color, bingo_button_rect, corner_radius)
    draw_rounded_rect_outline(screen, cfg.BORDER_COLOR, bingo_button_rect, corner_radius, scale_value(1))
    
    # Texto BINGO
    bingo_text_surface = fonts["button"].render("BINGO", True, text_color)
    bingo_text_rect = bingo_text_surface.get_rect(center=bingo_button_rect.center)
    screen.blit(bingo_text_surface, bingo_text_rect)
    
    # ==== BOTÓN REINICIAR ====
    if reset_hover:
        bg_color = (255, 108, 96)  # Rojo hover
    else:
        bg_color = (248, 81, 73)   # Rojo normal
    
    # Sombra del botón
    shadow_rect = reset_button_rect.copy()
    shadow_rect.x += scale_value(2) if reset_hover else scale_value(4)
    shadow_rect.y += scale_value(2) if reset_hover else scale_value(4)
    draw_rounded_rect(screen, shadow_color, shadow_rect, corner_radius)
    
    # Botón REINICIAR
    draw_rounded_rect(screen, bg_color, reset_button_rect, corner_radius)
    draw_rounded_rect_outline(screen, cfg.BORDER_COLOR, reset_button_rect, corner_radius, scale_value(1))
    
    # Texto REINICIAR
    reset_text_surface = fonts["button"].render("RESET", True, cfg.TEXT_COLOR)
    reset_text_rect = reset_text_surface.get_rect(center=reset_button_rect.center)
    screen.blit(reset_text_surface, reset_text_rect)

def draw_current_number():
    """Dibuja el número actual con diseño moderno y profesional"""
    if game_state.current_number is not None:
        # Obtener configuración adaptativa
        adaptive_config = get_adaptive_config()
        
        # Configuración del contenedor moderno con tamaño optimizado
        base_size = adaptive_config["current_number_size"]
        container_width = scale_value(base_size * 1.2, min_value=250, max_value=400)  # Más compacto
        container_height = scale_value(base_size * 0.7, min_value=160, max_value=280)  # Más bajo para evitar interferencia
        
        # Posicionamiento alineado con el historial para mejor balance visual
        container_x = scale_value(60, min_value=40, max_value=120)  # Margen izquierdo
        # Posicionar a la misma altura que el historial (lado derecho) - 1px más abajo
        container_y = scale_value(25, False, min_value=17, max_value=49)  # Misma Y que el historial + 1px
        corner_radius = scale_value(18, min_value=10, max_value=25)  # Bordes más redondeados
        
        # Determinar colores según el rango del número
        number_color, glow_color = get_number_color_and_glow(game_state.current_number)
        
        # Animación de escala suave con transiciones
        scale = game_state.transitions.get_value('number_scale', 1.0)
        glow_intensity_transition = game_state.transitions.get_value('number_glow', 0.3)
        
        # Aplicar escala
        scaled_width = int(container_width * scale)
        scaled_height = int(container_height * scale)
        scaled_x = container_x + (container_width - scaled_width) // 2
        scaled_y = container_y + (container_height - scaled_height) // 2
        
        container_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Sombra del contenedor
        shadow_rect = container_rect.copy()
        shadow_rect.x += scale_value(4)
        shadow_rect.y += scale_value(4)
        draw_rounded_rect(screen, (0, 0, 0, 64), shadow_rect, corner_radius)
        
        # Fondo del contenedor
        draw_rounded_rect(screen, cfg.FRAME_COLOR, container_rect, corner_radius)
        
        # Borde con color del rango
        draw_rounded_rect_outline(screen, number_color, container_rect, corner_radius, scale_value(2))
        
        # Efecto de brillo sutil en el borde con transición
        current_time = pygame.time.get_ticks()
        base_glow = 0.3 + 0.2 * math.sin(current_time / 1000)
        glow_intensity = base_glow * glow_intensity_transition
        glow_rect = container_rect.inflate(scale_value(4), scale_value(4))
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        glow_alpha = int(60 * glow_intensity)
        glow_surface_rect = pygame.Rect(0, 0, glow_rect.width, glow_rect.height)
        draw_rounded_rect(glow_surface, (*number_color[:3], glow_alpha), 
                         glow_surface_rect, corner_radius + scale_value(2))
        screen.blit(glow_surface, glow_rect)
        
        # Número principal
        number_font = fonts["number_large"]
        number_text = number_font.render(str(game_state.current_number), True, number_color)
        number_rect = number_text.get_rect(center=(container_rect.centerx, container_rect.centery - scale_value(8)))
        screen.blit(number_text, number_rect)
        
        # Etiqueta "ACTUAL"
        label_font = fonts["number_small"]
        label_text = label_font.render("ACTUAL", True, cfg.GRAY)
        label_rect = label_text.get_rect(center=(container_rect.centerx, container_rect.top + scale_value(16)))
        screen.blit(label_text, label_rect)
        
        # Contador de progreso
        counter_text = f"{len(game_state.drawn_numbers)}/{cfg.TOTAL_NUMBERS}"
        counter_font = fonts["number_small"]
        counter_surface = counter_font.render(counter_text, True, cfg.LIGHT_GRAY)
        counter_rect = counter_surface.get_rect(center=(container_rect.centerx, container_rect.bottom - scale_value(16)))
        screen.blit(counter_surface, counter_rect)

def select_number():
    """Selecciona un número aleatorio que no haya salido previamente.
    Actualiza el número actual y reproduce el audio inmediatamente."""
    try:
        # Obtener números disponibles (que no hayan salido)
        available_numbers = [i for i in range(1, cfg.TOTAL_NUMBERS + 1) if i not in game_state.drawn_numbers]
        if available_numbers:
            number = random.choice(available_numbers)
            game_state.current_number = number
            game_state.drawn_numbers.add(number)
            
            # Activar animación para el nuevo número
            game_state.number_animation_start = pygame.time.get_ticks()
            game_state.number_animation_active = True
            
            # Iniciar transiciones suaves
            game_state.transitions.start_transition('number_scale', 0.5, 1.0, 600, 'bounce')
            game_state.transitions.start_transition('number_glow', 0.0, 1.0, 400, 'ease_out')
            
            # Si estamos en modo servidor, enviar el número a los clientes
            if multiplayer_manager.is_server_mode():
                multiplayer_manager.send_number_to_clients(number)
                print(f"Número {number} enviado a los clientes")
            
            # Reproducir audio inmediatamente
            try:
                audio_path = f"audios_wav/numero_{number}.wav"
                if os.path.exists(audio_path):
                    number_sound = pygame.mixer.Sound(audio_path)
                    number_sound.play()
                    print(f"Reproduciendo audio: {audio_path}")
                    # Enviar audio a espectadores si hay servidor
                    try:
                        server = multiplayer_manager.server
                        if multiplayer_manager.is_server_mode() and server and hasattr(server, 'loop') and server.loop:
                            with open(audio_path, 'rb') as af:
                                audio_bytes = af.read()
                            payload = {
                                'type': 'spectator_audio',
                                'format': 'wav',
                                'data': base64.b64encode(audio_bytes).decode('ascii')
                            }

                            async def send_audio():
                                await server.broadcast_message_filtered(payload, role_filter='spectator')

                            try:
                                import asyncio as _asyncio
                                _asyncio.run_coroutine_threadsafe(send_audio(), server.loop)
                            except Exception as e:
                                print(f"Error enviando audio a espectadores: {e}")
                    except Exception as stream_error:
                        print(f"Error preparando audio para espectadores: {stream_error}")
                else:
                    print(f"Archivo de audio no encontrado: {audio_path}")
            except Exception as audio_error:
                print(f"Error reproduciendo sonido del número {number}: {audio_error}")
                # Intentar con formato alternativo
                try:
                    alt_audio_path = f"audios/{number}.wav"
                    if os.path.exists(alt_audio_path):
                        number_sound = pygame.mixer.Sound(alt_audio_path)
                        number_sound.play()
                        print(f"Reproduciendo audio alternativo: {alt_audio_path}")
                except Exception as alt_error:
                    print(f"Error con audio alternativo: {alt_error}")
            
            return number
        else:
            game_state.game_over = True
            return None
    except Exception as e:
        print(f"Error en select_number: {e}")
        return None

def draw_rounded_rect(surface, color, rect, radius):
    """Dibuja un rectángulo con esquinas redondeadas"""
    if len(color) == 4:  # Color con alpha
        # Crear superficie temporal para alpha blending
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color, (0, 0, rect.width, rect.height), border_radius=radius)
        surface.blit(temp_surface, rect)
    else:
        pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_rounded_rect_outline(surface, color, rect, radius, width):
    """Dibuja el contorno de un rectángulo con esquinas redondeadas"""
    pygame.draw.rect(surface, color, rect, width, border_radius=radius)

def get_number_color_and_glow(num):
    """Determina el color y brillo de un número según el modo de juego"""
    if cfg.TOTAL_NUMBERS == 90:
        # Modo normal: rangos 1-30, 31-60, 61-90
        if num <= 30:
            return cfg.RANGE_1_30, (130, 134, 251)
        elif num <= 60:
            return cfg.RANGE_31_60, (253, 253, 150)
        else:
            return cfg.RANGE_61_90, (255, 0, 110)
    else:
        # Modo alterno: rangos 1-25, 26-50, 51-75
        if num <= 25:
            return cfg.RANGE_1_30, (130, 134, 251)
        elif num <= 50:
            return cfg.RANGE_31_60, (253, 253, 150)
        else:
            return cfg.RANGE_61_90, (255, 0, 110)

def draw_number_history():
    """Dibuja el historial de números sorteados con diseño moderno tipo cards."""
    # Obtener configuración adaptativa
    adaptive_config = get_adaptive_config()
    
    # Configuración responsiva del panel
    panel_width = int(cfg.WIDTH * adaptive_config["history_width_ratio"])
    panel_height = int(cfg.HEIGHT * 0.7)  # Mantener proporción vertical
    panel_x = cfg.WIDTH - panel_width - scale_value(24, min_value=16, max_value=32)
    panel_y = scale_value(25, False, min_value=17, max_value=49)
    
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    corner_radius = scale_value(12)
    
    # Sombra del panel
    shadow_rect = panel_rect.copy()
    shadow_rect.x += scale_value(6)
    shadow_rect.y += scale_value(6)
    draw_rounded_rect(screen, (0, 0, 0, 32), shadow_rect, corner_radius)
    
    # Fondo del panel
    draw_rounded_rect(screen, cfg.FRAME_COLOR, panel_rect, corner_radius)
    
    # Borde del panel
    draw_rounded_rect_outline(screen, cfg.BORDER_COLOR, panel_rect, corner_radius, scale_value(2))
    
    # Header del panel
    header_height = scale_value(60, False)
    header_rect = pygame.Rect(panel_x, panel_y, panel_width, header_height)
    
    # Título moderno
    title_font = fonts["title_small"]
    title_text = title_font.render("HISTORIAL", True, cfg.TEXT_COLOR)
    title_rect = title_text.get_rect(center=(header_rect.centerx, header_rect.centery - scale_value(8, False)))
    screen.blit(title_text, title_rect)
    
    # Contador de números
    if game_state.drawn_numbers:
        count_text = f"{len(game_state.drawn_numbers)} números sorteados"
        count_font = fonts["number_small"]
        count_surface = count_font.render(count_text, True, cfg.GRAY)
        count_rect = count_surface.get_rect(center=(header_rect.centerx, header_rect.centery + scale_value(12, False)))
        screen.blit(count_surface, count_rect)
    
    # Línea separadora
    separator_y = panel_y + header_height
    separator_rect = pygame.Rect(panel_x + scale_value(16), separator_y, panel_width - scale_value(32), scale_value(1))
    pygame.draw.rect(screen, cfg.BORDER_COLOR, separator_rect)
    
    if not game_state.drawn_numbers:
        # Estado vacío con diseño moderno
        empty_y = panel_rect.centery
        empty_font = fonts["number_small"]
        
        # Icono placeholder (usando texto)
        icon_text = "○"
        icon_font = fonts["title_small"]
        icon_surface = icon_font.render(icon_text, True, cfg.GRAY)
        icon_rect = icon_surface.get_rect(center=(panel_rect.centerx, empty_y - scale_value(20, False)))
        screen.blit(icon_surface, icon_rect)
        
        # Mensaje
        message_text = "Sin números sorteados"
        message_surface = empty_font.render(message_text, True, cfg.GRAY)
        message_rect = message_surface.get_rect(center=(panel_rect.centerx, empty_y + scale_value(10, False)))
        screen.blit(message_surface, message_rect)
        
        return
    
    # Área de contenido
    content_y = separator_y + scale_value(16, False)
    content_height = panel_height - header_height - scale_value(32, False)
    content_rect = pygame.Rect(panel_x + scale_value(16), content_y, panel_width - scale_value(32), content_height)
    
    # Configuración adaptativa de la grilla
    sorted_numbers = sorted(game_state.drawn_numbers)
    num_count = len(sorted_numbers)
    
    # Determinar layout óptimo
    if num_count <= 15:
        cols = 3
        card_size = scale_value(36)
        font_to_use = fonts["number_small"]
        spacing = scale_value(8)
    elif num_count <= 30:
        cols = 4
        card_size = scale_value(32)
        font_to_use = fonts["number_small"]
        spacing = scale_value(6)
    elif num_count <= 50:
        cols = 4
        card_size = scale_value(28)
        font_to_use = font_smallest
        spacing = scale_value(5)
    else:
        cols = 5
        card_size = scale_value(24)
        font_to_use = font_smallest
        spacing = scale_value(4)
    
    # Calcular posiciones
    grid_width = cols * card_size + (cols - 1) * spacing
    grid_start_x = content_rect.x + (content_rect.width - grid_width) // 2
    
    # Dibujar números como cards modernas
    max_visible = min(num_count, 60)  # Límite para performance
    
    for i, number in enumerate(sorted_numbers[:max_visible]):
        row = i // cols
        col = i % cols
        
        # Posición de la card
        card_x = grid_start_x + col * (card_size + spacing)
        card_y = content_y + row * (card_size + spacing)
        
        # Verificar si cabe en el área visible
        if card_y + card_size > content_rect.bottom:
            # Mostrar indicador de números restantes
            remaining = num_count - i
            if remaining > 0:
                more_y = content_rect.bottom - scale_value(20, False)
                more_text = f"+ {remaining} más"
                more_font = font_smallest
                more_surface = more_font.render(more_text, True, cfg.GRAY)
                more_rect = more_surface.get_rect(center=(content_rect.centerx, more_y))
                screen.blit(more_surface, more_rect)
            break
        
        card_rect = pygame.Rect(card_x, card_y, card_size, card_size)
        
        # Determinar colores
        range_color, glow_color = get_number_color_and_glow(number)
        
        # Estado especial para número actual
        is_current = number == game_state.current_number
        
        if is_current:
            # Efecto de brillo para número actual
            current_time = pygame.time.get_ticks()
            pulse = 0.7 + 0.3 * math.sin(current_time / 400)
            
            # Brillo exterior
            glow_rect = card_rect.inflate(scale_value(6), scale_value(6))
            glow_alpha = int(100 * pulse)
            draw_rounded_rect(screen, (*glow_color[:3], glow_alpha), glow_rect, scale_value(6))
            
            # Card con color intenso
            draw_rounded_rect(screen, range_color, card_rect, scale_value(4))
            
            # Borde brillante
            draw_rounded_rect_outline(screen, cfg.HIGHLIGHT_COLOR, card_rect, scale_value(4), scale_value(2))
            
            # Texto contrastante
            text_color = cfg.BLACK if range_color == cfg.ACCENT_COLOR else cfg.TEXT_COLOR
        else:
            # Card normal
            # Fondo con color del rango pero más sutil
            bg_color = tuple(int(c * 0.8) for c in range_color[:3])  # 80% del color original
            draw_rounded_rect(screen, bg_color, card_rect, scale_value(4))
            
            # Borde sutil
            draw_rounded_rect_outline(screen, range_color, card_rect, scale_value(4), scale_value(1))
            
            # Texto con color del rango
            text_color = range_color
        
        # Renderizar número
        number_surface = font_to_use.render(str(number), True, text_color)
        number_rect = number_surface.get_rect(center=card_rect.center)
        screen.blit(number_surface, number_rect)
    
    # Leyenda de colores en la parte inferior
    if num_count > 0:
        legend_y = panel_rect.bottom - scale_value(50, False)
        legend_font = font_smallest
        
        # Determinar rangos según el modo
        if cfg.TOTAL_NUMBERS == 90:
            ranges = [("1-30", cfg.RANGE_1_30), ("31-60", cfg.RANGE_31_60), ("61-90", cfg.RANGE_61_90)]
        else:
            ranges = [("1-25", cfg.RANGE_1_30), ("26-50", cfg.RANGE_31_60), ("51-75", cfg.RANGE_61_90)]
        
        # Dibujar leyenda horizontal
        legend_width = panel_width - scale_value(32)
        legend_item_width = legend_width // 3
        
        for i, (range_text, color) in enumerate(ranges):
            item_x = panel_x + scale_value(16) + i * legend_item_width
            item_center_x = item_x + legend_item_width // 2
            
            # Círculo de color
            circle_radius = scale_value(4)
            pygame.draw.circle(screen, color, (item_center_x - scale_value(15), legend_y), circle_radius)
            
            # Texto del rango
            range_surface = legend_font.render(range_text, True, cfg.GRAY)
            range_rect = range_surface.get_rect(left=item_center_x - scale_value(8), centery=legend_y)
            screen.blit(range_surface, range_rect)

def draw_bingo_animation():
    """Muestra una animación estilo Las Vegas cuando se presiona el botón BINGO."""
    if game_state.bingo_called and game_state.bingo_animation_time > 0:
        # Cálculo del progreso de la animación
        elapsed = pygame.time.get_ticks() - game_state.bingo_animation_start
        progress = min(1.0, elapsed / game_state.bingo_animation_time)
        
        # Desvanecimiento del fondo con color oscuro
        alpha = int(180 * (1 - progress*0.5))  # Mantenemos algo de opacidad para efecto Vegas
        overlay = pygame.Surface((cfg.WIDTH, cfg.HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 0, 0, alpha))  # Fondo rojo oscuro semi-transparente (nueva paleta)
        screen.blit(overlay, (0, 0))
        
        # Efecto de destellos/brillos aleatorios estilo Vegas con nueva paleta
        current_time = pygame.time.get_ticks()
        for _ in range(20):  # Más destellos para un efecto más intenso
            # Posiciones aleatorias para los destellos
            x = random.randint(0, cfg.WIDTH)
            y = random.randint(0, cfg.HEIGHT)
            size = random.randint(2, 8)
            
            # Colores aleatorios de la nueva paleta: rojo, dorado, amarillo, naranja
            colors = [cfg.BUTTON_COLOR, cfg.GLOW_COLOR, cfg.ALT_GLOW_COLOR, cfg.BORDER_COLOR]
            color = random.choice(colors)
            
            # Dibujar destello
            pygame.draw.circle(screen, color, (x, y), size)
            
            # Algunos con brillo adicional
            if random.random() > 0.7:
                for i in range(3, 0, -1):
                    alpha = int(100 - i * 30)
                    s = pygame.Surface((size*2*i, size*2*i), pygame.SRCALPHA)
                    s.fill((*color[:3], alpha))
                    screen.blit(s, (x - size*i, y - size*i))
        
        # Tamaño del texto "BINGO" con efecto de escala más dinámico
        if progress < 0.3:
            # Fase 1: Crecer rápidamente con rebote
            scale = 0.2 + progress * 3.5
        elif progress < 0.7:
            # Fase 2: Pulsar ligeramente
            pulse = 0.1 * math.sin(progress * 20)
            scale = 1.0 + pulse
        else:
            # Fase 3: Reducir gradualmente
            scale = 1.0 - (progress - 0.7) / 0.3
        
        # Calculamos un ángulo oscilante para rotación
        angle = math.sin(current_time / 150) * 5 * (1 - progress)  # Disminuye con el progreso
            
        # Texto "BINGO" grande y centrado con estilo Vegas
        font_size = int(140 * scale)
        if font_size > 0:  # Evitar tamaños de fuente negativos o cero
            # Usar JetBrains Mono para estilo profesional
            bingo_font = cfg.get_font(font_size, bold=True)
            
            # Varias capas de texto para efecto neón/resplandor con nueva paleta
            # Capa de resplandor externa - alternando dorado y rojo
            for i in range(8, 0, -1):
                glow_color = cfg.GLOW_COLOR if i % 2 == 0 else cfg.BUTTON_COLOR  # Dorado o Rojo
                glow_alpha = max(50 - i * 5, 0)
                glow_text = bingo_font.render("¡BINGO!", True, (*glow_color[:3], glow_alpha))
                glow_rect = glow_text.get_rect(center=(cfg.WIDTH // 2 + i, cfg.HEIGHT // 2 + i))
                screen.blit(glow_text, glow_rect)
            
            # Sombra oscura para profundidad
            shadow_text = bingo_font.render("¡BINGO!", True, cfg.BLACK)
            shadow_rect = shadow_text.get_rect(center=(cfg.WIDTH // 2 + 4, cfg.HEIGHT // 2 + 4))
            screen.blit(shadow_text, shadow_rect)
            
            # Texto principal con color dorado brillante de la nueva paleta
            bingo_text = bingo_font.render("¡BINGO!", True, cfg.GLOW_COLOR)  # Dorado
            text_rect = bingo_text.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2))
            screen.blit(bingo_text, text_rect)
            
            # Texto adicional "GANADOR" en la parte inferior
            if progress > 0.3 and progress < 0.9:
                winner_scale = min(1.0, (progress - 0.3) * 3)
                winner_size = int(50 * winner_scale)
                winner_font = cfg.get_font(winner_size, bold=True)
                
                # Texto con sombra
                winner_shadow = winner_font.render("¡GANADOR!", True, cfg.BLACK)
                winner_shadow_rect = winner_shadow.get_rect(center=(cfg.WIDTH // 2 + 2, cfg.HEIGHT // 2 + 100 + 2))
                screen.blit(winner_shadow, winner_shadow_rect)
                
                # Texto principal con color amarillo brillante de la nueva paleta
                winner_text = winner_font.render("¡GANADOR!", True, cfg.ALT_GLOW_COLOR)  # Amarillo
                winner_rect = winner_text.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2 + 100))
                screen.blit(winner_text, winner_rect)
                
        # Añadir instrucciones para continuar jugando cuando está cerca de terminar
        if progress > 0.7:
            continue_font = cfg.get_font(30, bold=True)
            continue_text = continue_font.render("Presiona REINICIAR para jugar otra partida", True, cfg.TEXT_COLOR)
            continue_rect = continue_text.get_rect(center=(cfg.WIDTH//2, cfg.HEIGHT//2 + 170))
            screen.blit(continue_text, continue_rect)
            
        # Terminar la animación cuando se complete
        if progress >= 1.0:
            game_state.bingo_animation_time = 0
def draw_timer():
    """Dibuja el temporizador con estilo Las Vegas."""
    if game_state.game_started and not game_state.game_over:
        # Calcular tiempo transcurrido
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - game_state.start_time) // 1000  # En segundos
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        # Crear rectángulo para el temporizador - estilo neón, escalado para responsividad
        timer_width = scale_value(150)
        timer_height = scale_value(40, False)
        timer_margin = scale_value(10)
        
        timer_rect = pygame.Rect(timer_margin, timer_margin, timer_width, timer_height)
        
        # Efecto de borde neón para el temporizador
        for i in range(3, 0, -1):
            glow_rect = timer_rect.inflate(i*2, i*2)
            alpha = int(80 - i * 15)
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            s.fill((37, 99, 235, alpha))  # Azul neón con alpha
            screen.blit(s, (glow_rect.x, glow_rect.y))
            
        pygame.draw.rect(screen, cfg.BACKGROUND_DARK, timer_rect)
        pygame.draw.rect(screen, cfg.PRIMARY_COLOR, timer_rect, 2, border_radius=5)
        
        # Texto del temporizador con sombra para estilo neón
        time_text = font_small.render(f"TIEMPO: {minutes:02d}:{seconds:02d}", True, cfg.WHITE)
        
        # Sombra
        shadow_text = font_small.render(f"TIEMPO: {minutes:02d}:{seconds:02d}", True, cfg.BLACK)
        shadow_rect = shadow_text.get_rect(center=(timer_rect.center[0]+1, timer_rect.center[1]+1))
        screen.blit(shadow_text, shadow_rect)
        
        # Texto principal
        text_rect = time_text.get_rect(center=timer_rect.center)
        screen.blit(time_text, text_rect)
    else:
        # Botón BINGO deshabilitado con estilo gris opaco
        pygame.draw.rect(screen, cfg.DISABLED, bingo_button_rect, border_radius=8)
        
        # Borde interno más claro
        inner_rect = bingo_button_rect.inflate(-10, -10)
        pygame.draw.rect(screen, cfg.FRAME_COLOR, inner_rect, border_radius=6)
        
        # Texto del botón deshabilitado
        bingo_text = font_medium.render("BINGO", True, (180, 180, 180))
        bingo_text_rect = bingo_text.get_rect(center=bingo_button_rect.center)
        screen.blit(bingo_text, bingo_text_rect)

def reset_game():
    """Reinicia completamente el juego a su estado inicial."""
    global current_background_index
    
    # Alternar al siguiente fondo
    if background_images:  # Verificar que tengamos imágenes cargadas
        current_background_index = (current_background_index + 1) % len(background_images)
    
    # Reiniciar estado del juego
    game_state.game_started = False
    game_state.game_over = False
    game_state.current_number = None
    game_state.drawn_numbers.clear()
    game_state.balls.clear()
    game_state.bingo_called = False
    
    # Reiniciar animaciones
    game_state.bingo_animation_active = False
    game_state.number_animation_active = False
    game_state.number_scale = 1.0
    game_state.button_hover = None
    game_state.bingo_animation_time = 0
    game_state.bingo_animation_start = 0
    
    # Reiniciar tiempo
    game_state.start_time = pygame.time.get_ticks()
    
    # Ya no usamos pelotas, así que no es necesario reiniciar sus posiciones
    # Ball.reset_positions()  # Comentado porque ya no se usa
    
    # Reinicializar el tablero
    game_state.initialize_board()
    
    # Si estamos en modo servidor, enviar señal de reset a los clientes
    if multiplayer_manager.is_server_mode():
        multiplayer_manager.send_game_reset()
        print("Señal de reset enviada a los clientes")
    
    # Si estamos en modo cliente, reiniciar la cartilla
    if multiplayer_manager.is_client_mode() and multiplayer_manager.player_card:
        multiplayer_manager.player_card.marked.clear()
        print("Cartilla reiniciada")
    
    # Reproducir sonido de reinicio
    try:
        reset_sound = pygame.mixer.Sound(f"{cfg.AUDIO_FOLDER}/reset.{cfg.AUDIO_FILE_FORMAT}")
        reset_sound.play()
    except Exception as e:
        print(f"Error reproduciendo sonido de reinicio: {e}")

def check_button_click(pos):
    # Comprobar si se ha hecho clic en un botón
    # Definir rectángulos de botones (deben coincidir con los de draw_buttons)
    btn_height = scale_value(60, False)
    
    # Botones escalados y posicionados proporcionalmente a la pantalla
    start_btn_width = scale_value(340)
    side_btn_width = scale_value(140)
    bottom_margin = scale_value(110, False)
    
    start_button_rect = pygame.Rect(
        cfg.WIDTH // 2 - start_btn_width // 2,
        cfg.HEIGHT - bottom_margin, 
        start_btn_width, 
        btn_height
    )
    bingo_button_rect = pygame.Rect(
        cfg.WIDTH - side_btn_width - scale_value(30), 
        cfg.HEIGHT - bottom_margin, 
        side_btn_width, 
        btn_height
    )
    reset_button_rect = pygame.Rect(
        scale_value(30), 
        cfg.HEIGHT - bottom_margin, 
        side_btn_width, 
        btn_height
    )
    
    # Comprobar si se hizo clic en el botón INICIAR/SIGUIENTE
    if start_button_rect.collidepoint(pos):
        if not game_state.game_started:
            # Primera ejecución - iniciar el juego
            game_state.game_started = True
            # Reiniciar tiempo
            game_state.start_time = pygame.time.get_ticks()
            # Iniciar con el primer número
            select_number()
            # Iniciar el juego (sin sonido ya que no tenemos start.wav)
            game_state.game_started = True
            game_state.start_time = pygame.time.get_ticks()
        else:
            # Siguiente número
            try:
                select_number()
                game_state.number_animation_start = pygame.time.get_ticks()
            except Exception as e:
                print(f"Error al seleccionar siguiente número: {e}")
    
    # Comprobar si se hizo clic en el botón BINGO
    elif bingo_button_rect.collidepoint(pos):
            # Llamar "BINGO" - mostrar animación
            # Nota: No hay archivo de sonido bingo.wav, por lo que no intentamos reproducir audio
            game_state.bingo_called = True
            # Ya no establecemos game_over a True para evitar que el juego se cierre
            game_state.bingo_animation_start = pygame.time.get_ticks()
            game_state.bingo_animation_active = True
            # Configurar la animación de BINGO
            game_state.bingo_animation_time = game_state.bingo_animation_duration
                
    # Comprobar si se hizo clic en el botón REINICIAR
    elif reset_button_rect.collidepoint(pos):
        # Reiniciar juego (sin sonido ya que no tenemos reset.wav)
        reset_game()

# Bucle principal del juego
clock = pygame.time.Clock()

while game_state.running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            game_state.running = False
            continue
            
        # Manejar eventos según el estado actual
        if game_state.show_title_screen:
            # Manejar eventos de la pantalla de título
            result = title_screen.handle_event(event)
            if result:
                print(f"🔍 DEBUG: title_screen retornó: {result}")
            if result == "start_normal_game" or result == "show_mode_selection":
                # Ir a la selección de modo en lugar de iniciar directamente
                game_state.show_title_screen = False
                game_state.show_mode_selection = True
                reset_multiplayer_manager()
                print("✅ Mostrando selección de modo")
                print(f"   show_title_screen: {game_state.show_title_screen}")
                print(f"   show_mode_selection: {game_state.show_mode_selection}")
            elif result == "start_alt_game":
                # Modo alterno no soportado en multijugador por ahora
                cfg.BOARD_ROWS = 7
                cfg.BOARD_COLS = 11
                cfg.TOTAL_NUMBERS = 75
                game_state.__init__()
                game_state.show_title_screen = False
                game_state.game_started = True
                print(f"✅ Iniciando juego ALTERNO: Tablero {cfg.BOARD_ROWS}x{cfg.BOARD_COLS}, números 1-{cfg.TOTAL_NUMBERS}")
            elif result == "exit_game":
                pygame.quit()
                sys.exit()
                
        elif game_state.show_mode_selection:
            # Manejar eventos de la selección de modo
            if event.type == MOUSEBUTTONDOWN:
                action = mode_selection.handle_click(event.pos)
                
                if action == "start_local":
                    # Modo local (juego tradicional)
                    config = mode_selection.get_config()
                    if config["game_mode"] == "normal":
                        cfg.BOARD_ROWS = 9
                        cfg.BOARD_COLS = 10
                        cfg.TOTAL_NUMBERS = 90
                        print("✅ Modo LOCAL iniciado (Normal: 90 números)")
                    else:
                        cfg.BOARD_ROWS = 7
                        cfg.BOARD_COLS = 11
                        cfg.TOTAL_NUMBERS = 75
                        print("✅ Modo LOCAL iniciado (Alterno: 75 números)")
                    game_state.__init__()
                    game_state.show_title_screen = False
                    game_state.show_mode_selection = False
                    game_state.game_started = True
                    
                elif action == "start_server":
                    # Modo servidor
                    config = mode_selection.get_config()
                    if config["game_mode"] == "normal":
                        cfg.BOARD_ROWS = 9
                        cfg.BOARD_COLS = 10
                        cfg.TOTAL_NUMBERS = 90
                        print(f"✅ Configurando servidor con modo Normal (90 números)")
                    else:
                        cfg.BOARD_ROWS = 7
                        cfg.BOARD_COLS = 11
                        cfg.TOTAL_NUMBERS = 75
                        print(f"✅ Configurando servidor con modo Alterno (75 números)")
                    
                    # Iniciar servidor
                    success = multiplayer_manager.start_server_mode(config["nickname"])
                    if success:
                        game_state.__init__()
                        game_state.show_title_screen = False
                        game_state.show_mode_selection = False
                        game_state.game_started = False
                        # Asociar la pantalla del host para poder transmitir a espectadores
                        try:
                            # Intervalo reducido para mayor fluidez (0.05s = ~20 FPS)
                            multiplayer_manager.set_server_screen(screen, interval=0.05)
                        except Exception as e:
                            print(f"No se pudo iniciar el streamer de pantalla: {e}")
                        print(f"✅ Modo SERVIDOR iniciado como '{config['nickname']}'")
                    else:
                        mode_selection.set_error("Error iniciando servidor")
                        
                elif action == "start_client":
                    # Modo cliente
                    config = mode_selection.get_config()
                    cfg.BOARD_ROWS = 9
                    cfg.BOARD_COLS = 10
                    cfg.TOTAL_NUMBERS = 90
                    
                    card_position = (50, 300)
                    success = multiplayer_manager.start_client_mode(
                        config["nickname"],
                        config["server_ip"],
                        screen=screen,
                        position=card_position
                    )
                    
                    if success:
                        game_state.__init__()
                        game_state.show_title_screen = False
                        game_state.show_mode_selection = False
                        game_state.game_started = False
                        print(f"✅ Modo CLIENTE iniciado como '{config['nickname']}'")
                    else:
                        mode_selection.set_error("Error conectando al servidor")
                        
            elif event.type == KEYDOWN:
                action = mode_selection.handle_keypress(event)
                if action == "start_server":
                    # Iniciar modo servidor
                    config = mode_selection.get_config()
                    if config["game_mode"] == "normal":
                        cfg.BOARD_ROWS = 9
                        cfg.BOARD_COLS = 10
                        cfg.TOTAL_NUMBERS = 90
                        print(f"✅ Configurando servidor con modo Normal (90 números)")
                    else:
                        cfg.BOARD_ROWS = 7
                        cfg.BOARD_COLS = 11
                        cfg.TOTAL_NUMBERS = 75
                        print(f"✅ Configurando servidor con modo Alterno (75 números)")
                    
                    success = multiplayer_manager.start_server_mode(config["nickname"])
                    if success:
                        game_state.__init__()
                        game_state.show_title_screen = False
                        game_state.show_mode_selection = False
                        game_state.game_started = False
                        try:
                            # Intervalo reducido para mayor fluidez (0.05s = ~20 FPS)
                            multiplayer_manager.set_server_screen(screen, interval=0.05)
                        except Exception as e:
                            print(f"No se pudo iniciar el streamer de pantalla: {e}")
                        print(f"✅ Modo SERVIDOR iniciado como '{config['nickname']}'")
                    else:
                        mode_selection.set_error("Error iniciando servidor")
                        
                elif action == "start_client":
                    # Iniciar modo cliente
                    config = mode_selection.get_config()
                    cfg.BOARD_ROWS = 9
                    cfg.BOARD_COLS = 10
                    cfg.TOTAL_NUMBERS = 90
                    
                    card_position = (50, 300)
                    success = multiplayer_manager.start_client_mode(
                        config["nickname"],
                        config["server_ip"],
                        screen=screen,
                        position=card_position
                    )
                    
                    if success:
                        game_state.__init__()
                        game_state.show_title_screen = False
                        game_state.show_mode_selection = False
                        game_state.game_started = False
                        print(f"✅ Modo CLIENTE iniciado como '{config['nickname']}'")
                    else:
                        mode_selection.set_error("Error conectando al servidor")
                        
                elif action == "start_local":
                    # Iniciar modo local desde teclado (Enter)
                    config = mode_selection.get_config()
                    if config["game_mode"] == "normal":
                        cfg.BOARD_ROWS = 9
                        cfg.BOARD_COLS = 10
                        cfg.TOTAL_NUMBERS = 90
                        print("✅ Modo LOCAL iniciado (Normal: 90 números)")
                    else:
                        cfg.BOARD_ROWS = 7
                        cfg.BOARD_COLS = 11
                        cfg.TOTAL_NUMBERS = 75
                        print("✅ Modo LOCAL iniciado (Alterno: 75 números)")
                    game_state.__init__()
                    game_state.show_title_screen = False
                    game_state.show_mode_selection = False
                    game_state.game_started = True
        else:
            # Manejar eventos del juego principal
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_state.running = False
                elif event.key == K_SPACE:
                    # Tecla ESPACIO: sortear siguiente número (solo en modo local o servidor)
                    if not game_state.show_title_screen and not game_state.show_mode_selection:
                        # Solo permitir en modo local o servidor (no en modo cliente)
                        if multiplayer_manager.is_local_mode() or multiplayer_manager.is_server_mode():
                            if game_state.game_started:
                                # Sortear siguiente número
                                try:
                                    select_number()
                                    game_state.number_animation_start = pygame.time.get_ticks()
                                    print("⌨️  Número sorteado con ESPACIO")
                                except Exception as e:
                                    print(f"Error al sortear con ESPACIO: {e}")
                            else:
                                # Si el juego no ha empezado, iniciarlo con ESPACIO
                                game_state.game_started = True
                                game_state.start_time = pygame.time.get_ticks()
                                try:
                                    select_number()
                                    game_state.number_animation_start = pygame.time.get_ticks()
                                    print("⌨️  Juego iniciado con ESPACIO")
                                except Exception as e:
                                    print(f"Error al iniciar con ESPACIO: {e}")
            
            elif event.type == MOUSEMOTION:
                # Comprobar efectos hover en botones
                mouse_pos = pygame.mouse.get_pos()
                
                # Dimensiones de los botones - IDÉNTICAS a las de draw_buttons
                start_button_rect = pygame.Rect(cfg.WIDTH // 2 - 150, cfg.HEIGHT - 100, 300, 50)
                bingo_button_rect = pygame.Rect(cfg.WIDTH - 150, cfg.HEIGHT - 100, 120, 50)
                reset_button_rect = pygame.Rect(30, cfg.HEIGHT - 100, 120, 50)  # Nuevo botón REINICIAR
                
                if start_button_rect.collidepoint(mouse_pos):
                    game_state.button_hover = "start"
                elif bingo_button_rect.collidepoint(mouse_pos):
                    game_state.button_hover = "bingo"
                elif reset_button_rect.collidepoint(mouse_pos):
                    game_state.button_hover = "reset"
                else:
                    game_state.button_hover = None
            elif event.type == MOUSEBUTTONDOWN:
                check_button_click(event.pos)
    
    # Actualizar animaciones
    current_time = pygame.time.get_ticks()
    
    if game_state.show_title_screen:
        # Actualizar la pantalla de título
        title_screen.update()
    elif game_state.show_mode_selection:
        # No hay actualización necesaria para la pantalla de selección de modo
        pass
    else:
        # Actualizar el gestor multijugador (procesar mensajes de clientes)
        if multiplayer_manager.is_client_mode():
            multiplayer_manager.update()
        # Actualizar animación de BINGO
        if game_state.bingo_animation_active:
            if current_time - game_state.bingo_animation_start > game_state.bingo_animation_duration:
                game_state.bingo_animation_active = False
                # Activar efecto de confeti al terminar la animación de bingo
                if not game_state.show_confetti:
                    game_state.show_confetti = True
                    # Crear partículas de confeti
                    for _ in range(100):
                        particle = {
                            'x': random.randint(0, cfg.WIDTH),
                            'y': random.randint(-100, -10),
                            'velocity_y': random.uniform(1, 3),
                            'velocity_x': random.uniform(-1, 1),
                            'color': random.choice([cfg.PRIMARY, cfg.SECONDARY, cfg.ACCENT]),
                            'size': random.randint(5, 15),
                            'rotation': random.uniform(0, 360)
                        }
                        game_state.confetti_particles.append(particle)
        
        # Actualizar confeti
        if game_state.show_confetti:
            for particle in game_state.confetti_particles:
                particle['y'] += particle['velocity_y']
                particle['x'] += particle['velocity_x']
                particle['rotation'] += 2
                
                # Eliminar partículas fuera de la pantalla
                if particle['y'] > cfg.HEIGHT:
                    game_state.confetti_particles.remove(particle)
                    
            # Desactivar confeti cuando ya no hay partículas
            if len(game_state.confetti_particles) == 0:
                game_state.show_confetti = False
        
        # Las pelotas han sido eliminadas - no es necesario actualizarlas
        pass
    
    # --------- RENDERIZADO ----------
    if game_state.show_title_screen:
        # Mostrar la pantalla de título
        title_screen.draw()
    elif game_state.show_mode_selection:
        # Mostrar la pantalla de selección de modo
        print("🎮 RENDERIZANDO PANTALLA DE SELECCIÓN DE MODO")
        mode_selection.draw()
    else:
        # Limpiar la pantalla con el fondo adecuado
        if background_images:  # Verificar que tengamos al menos una imagen
            # Usar la imagen de fondo actual
            screen.blit(background_images[current_background_index], (0, 0))
        else:
            # Si no se pudo cargar ninguna imagen, usar el color de fondo como respaldo
            screen.fill(cfg.BACKGROUND)
        
        # Dibujar el número actual grande (ahora en la parte superior)
        draw_current_number()
        
        # Dibujar el historial de números sorteados
        draw_number_history()
        
        # Dibujar el tablero (ahora más pequeño y posicionado mejor)
        draw_board()
        
        # Ya no se dibujan pelotas - fueron eliminadas
        
        # Dibujar cartilla del cliente si está en modo cliente
        if multiplayer_manager.is_client_mode():
            multiplayer_manager.draw_card(screen)
            
            # Mostrar estado de conexión
            status = multiplayer_manager.get_connection_status()
            status_font = cfg.get_font(24)
            status_text = f"Conectado: {status['nickname']} | Jugadores: {status['total_players']}"
            status_color = cfg.SUCCESS if status['connected'] else cfg.DANGER
            status_surface = status_font.render(status_text, True, status_color)
            screen.blit(status_surface, (50, 50))
        
        # Mostrar información del servidor si está en modo servidor
        if multiplayer_manager.is_server_mode():
            status = multiplayer_manager.get_connection_status()
            status_font = cfg.get_font(24)
            # Mostrar la URL web completa para que el usuario sepa dónde conectar
            web_url = status.get('http_url', f"http://{status['ip']}:8080")
            server_text = f"Servidor: {status['nickname']} | Web: {web_url} | Clientes: {status['connected_clients']}"
            status_surface = status_font.render(server_text, True, cfg.PRIMARY_COLOR)
            screen.blit(status_surface, (50, 50))
        
        # Dibujar los botones con efectos de hover
        draw_buttons()
        
        # Dibujar la animación de bingo si corresponde
        if game_state.bingo_called:
            draw_bingo_animation()
        
        # Dibujar confeti si está activo
        if game_state.show_confetti:
            for particle in game_state.confetti_particles:
                # Dibujar rectángulos rotados como confeti
                surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
                pygame.draw.rect(surface, particle['color'], (0, 0, particle['size'], particle['size']))
                rotated = pygame.transform.rotate(surface, particle['rotation'])
                rect = rotated.get_rect(center=(particle['x'], particle['y']))
                screen.blit(rotated, rect)
        
        # Mostrar tiempo transcurrido si el juego está activo
        if game_state.game_started and not game_state.game_over:
            elapsed = (current_time - game_state.start_time) // 1000  # En segundos
            minutes = elapsed // 60
            seconds = elapsed % 60
            time_text = font_small.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, cfg.BLACK)
            screen.blit(time_text, (10, 10))
    
    # Actualizar tooltips
    if not game_state.show_title_screen:
        game_state.tooltips.update()
        game_state.tooltips.draw(screen)
    
    # Recargar fuentes si la resolución cambió (solo durante pruebas)
    if cfg.WIDTH != int(BASE_WIDTH * SCALE_X) or cfg.HEIGHT != int(BASE_HEIGHT * SCALE_Y):
        # Actualizar factores de escala
        SCALE_X = cfg.WIDTH / BASE_WIDTH
        SCALE_Y = cfg.HEIGHT / BASE_HEIGHT
        # Recargar fuentes con nuevos tamaños
        load_responsive_fonts()
    
    # Actualizar la pantalla y controlar FPS
    pygame.display.flip()
    
    # Transmitir pantalla si estamos en modo servidor
    if multiplayer_manager.is_server_mode():
        multiplayer_manager.broadcast_screen(screen)
        
    clock.tick(120)  # FPS aumentados para mayor fluidez



pygame.quit()
sys.exit()

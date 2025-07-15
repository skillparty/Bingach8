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

# Importar configuración
import config as cfg

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

# Función auxiliar para escalar valores según la resolución
def scale_value(value, is_horizontal=True):
    if is_horizontal:
        return int(value * SCALE_X)
    else:
        return int(value * SCALE_Y)

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
def load_responsive_fonts():
    """Carga las fuentes con tamaños adaptados a la resolución actual"""
    global font_big, font_medium, font_small, font_smallest, fonts
    
    # Para un estilo retro Vegas, usamos fuentes sans-serif con tamaño escalado y negrita
    font_big = pygame.font.SysFont(font_names, scale_value(80), bold=True)
    font_medium = pygame.font.SysFont(font_names, scale_value(36), bold=True)
    font_small = pygame.font.SysFont(font_names, scale_value(24))
    font_smallest = pygame.font.SysFont(font_names, scale_value(14))
    
    # Diccionario de fuentes adicionales
    fonts = {
        "title": pygame.font.SysFont(font_names, scale_value(32), bold=True),
        "title_small": pygame.font.SysFont(font_names, scale_value(24), bold=True),
        "button": pygame.font.SysFont(font_names, scale_value(26), bold=True),
        "timer": pygame.font.SysFont(font_names, scale_value(32), bold=True),
        "bingo": pygame.font.SysFont(font_names, scale_value(80), bold=True)
    }

# Cargar fuentes iniciales
load_responsive_fonts()

# Estado del juego
class GameState:
    def __init__(self):
        self.running = True
        self.game_started = False
        self.game_over = False
        self.board = [[None for _ in range(cfg.BOARD_COLS)] for _ in range(cfg.BOARD_ROWS)]
        self.current_number = None
        self.drawn_numbers = set()
        self.balls = []
        self.bingo_called = False
        
        # Variables para animaciones y efectos visuales
        self.bingo_animation_start = 0
        self.bingo_animation_duration = 5000  # 5 segundos
        self.bingo_animation_scale = 1.0
        self.bingo_animation_rotation = 0
        self.bingo_animation_active = False
        
        # Variables para nuevas animaciones
        self.number_animation_start = 0
        self.number_animation_duration = 1000  # 1 segundo
        self.number_animation_active = False
        self.number_scale = 1.0
        self.button_hover = None  # Para efecto hover en botones
        self.show_confetti = False  # Para animación de confeti al ganar
        self.confetti_particles = []  # Para partículas de confeti
        self.start_time = pygame.time.get_ticks()  # Para cronometrar el juego
        
        # Inicialización del tablero
        self.initialize_board()
    
    def initialize_board(self):
        # Inicializar el tablero con los números del 1 al 90
        num = 1
        for row in range(cfg.BOARD_ROWS):
            for col in range(cfg.BOARD_COLS):
                if num <= cfg.TOTAL_NUMBERS:
                    self.board[row][col] = num
                    num += 1

game_state = GameState()

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
        if self.number <= 30:
            # Rango 1-30: Rojo
            self.color = cfg.BUTTON_COLOR  # Rojo
            self.border_color = (200, 0, 0)  # Borde rojo más oscuro
            self.text_color = cfg.TEXT_COLOR  # Texto blanco para contraste
        elif self.number <= 60:
            # Rango 31-60: Dorado
            self.color = cfg.GLOW_COLOR  # Dorado
            self.border_color = (200, 160, 0)  # Borde dorado más oscuro
            self.text_color = cfg.BLACK  # Texto negro para contraste con dorado
        else:
            # Rango 61-90: Naranja
            self.color = cfg.BORDER_COLOR  # Naranja
            self.border_color = (200, 80, 0)  # Borde naranja más oscuro
            self.text_color = cfg.TEXT_COLOR  # Texto blanco para contraste
        
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
    # Dibujar tablero de bingo 9x10 con estilo retro Las Vegas
    cell_size = scale_value(48)  # Tamaño de celda escalado
    board_width = cfg.BOARD_COLS * cell_size
    board_height = cfg.BOARD_ROWS * cell_size
    board_x = (cfg.WIDTH - board_width) // 2
    board_y = scale_value(110, False)  # Alineado a la misma altura que los demás elementos, escalado verticalmente
    
    # Fondo del tablero con borde neón brillante estilo Vegas
    # Primero dibujar un efecto de resplandor para el tablero con la nueva paleta
    for i in range(5, 0, -1):
        glow_rect = pygame.Rect(board_x-i-2, board_y-i-2, board_width+i*2+4, board_height+i*2+4)
        alpha = int(50 - i * 8)  # Disminuir alpha gradualmente
        s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        s.fill((180, 0, 0, alpha))  # Rojo con transparencia (nueva paleta)
        screen.blit(s, (glow_rect.x, glow_rect.y))
    
    # Borde con estilo retro Vegas usando la nueva paleta
    pygame.draw.rect(screen, cfg.BUTTON_COLOR, (board_x-4, board_y-4, board_width+8, board_height+8), 2)  # Rojo
    
    # Título del tablero con estilo Vegas
    # Texto con sombra para efecto retro
    shadow_offset = 2
    board_title_shadow = font_medium.render("TABLERO", True, cfg.BLACK)
    title_shadow_rect = board_title_shadow.get_rect(midtop=(board_x + board_width // 2 + shadow_offset, board_y - 45 + shadow_offset))
    screen.blit(board_title_shadow, title_shadow_rect)
    
    # Texto principal con color dorado de la nueva paleta
    board_title = font_medium.render("TABLERO", True, cfg.GLOW_COLOR)  # Dorado
    title_rect = board_title.get_rect(midtop=(board_x + board_width // 2, board_y - 45))
    screen.blit(board_title, title_rect)
    
    # Dibujar celdas del tablero y números con estilo Vegas
    for row in range(cfg.BOARD_ROWS):
        for col in range(cfg.BOARD_COLS):
            cell_x = board_x + col * 48
            cell_y = board_y + row * 48
            cell_size = 46  # Celdas ligeramente más grandes
            
            # Dibujar celda con estilo Vegas - bordes redondeados
            number = row * cfg.BOARD_COLS + col + 1
            if number <= 90:  # Solo hay 90 números en el bingo
                # Determinar el color basado en el rango del número - nueva paleta Vegas
                if number <= 30:
                    range_color = cfg.BUTTON_COLOR  # Rojo
                elif number <= 60:
                    range_color = cfg.GLOW_COLOR    # Dorado
                else:
                    range_color = cfg.BORDER_COLOR  # Naranja
                
                # Estado de la celda basado en si el número ha sido extraído
                if number in game_state.drawn_numbers:
                    # Número sorteado - estilo destacado con nueva paleta
                    pygame.draw.rect(screen, cfg.FRAME_COLOR, (cell_x, cell_y, cell_size, cell_size), border_radius=5)  # Plateado
                    text_color = range_color  # Color según rango (rojo, dorado o naranja)
                    
                    # Destacar con efecto brillante si es el número actual
                    if number == game_state.current_number:
                        # Efecto de brillo para el número actual
                        for i in range(3, 0, -1):
                            glow_rect = pygame.Rect(cell_x-i, cell_y-i, cell_size+i*2, cell_size+i*2)
                            alpha = int(70 - i * 20) 
                            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                            # Color del brillo según el rango del número
                            if number <= 30:
                                glow_color = (180, 0, 0, alpha)     # Rojo con transparencia
                            elif number <= 60:
                                glow_color = (255, 215, 0, alpha)   # Dorado con transparencia
                            else:
                                glow_color = (255, 140, 0, alpha)   # Naranja con transparencia
                            s.fill(glow_color)
                            screen.blit(s, (glow_rect.x, glow_rect.y))
                            
                        pygame.draw.rect(screen, cfg.ALT_GLOW_COLOR, (cell_x, cell_y, cell_size, cell_size), border_radius=5)  # Amarillo
                        text_color = cfg.BLACK  # Máximo contraste para el actual
                else:
                    # Número no sorteado - estilo más sutil
                    pygame.draw.rect(screen, cfg.WHITE, (cell_x, cell_y, cell_size, cell_size), border_radius=5)
                    pygame.draw.rect(screen, cfg.SECONDARY, (cell_x, cell_y, cell_size, cell_size), 1, border_radius=5)  # Plateado
                    text_color = cfg.SECONDARY  # Plateado para números no sorteados
                
                # Número con tipografía sans-serif
                num_text = font_small.render(str(number), True, text_color)
                text_rect = num_text.get_rect(center=(cell_x + cell_size//2, cell_y + cell_size//2))
                screen.blit(num_text, text_rect)

def draw_buttons():
    """Dibuja los botones del juego con estilo Vegas."""
    # Definición de botones - más grandes y llamativos para estilo Vegas, escalados para responsividad
    btn_height = scale_value(60, False)
    
    # Botones escalados y posicionados proporcionalmente a la pantalla
    start_btn_width = scale_value(340)
    side_btn_width = scale_value(140)
    bottom_margin = scale_value(110, False)
    
    # Crear rectángulos para los botones
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
    
    # Guardar los rectángulos para la detección de clicks
    game_state.buttons = {
        "start": start_button_rect,
        "bingo": bingo_button_rect,
        "reset": reset_button_rect
    }
    
    # Comprobar si el ratón está sobre algún botón para efecto hover
    mouse_pos = pygame.mouse.get_pos()
    start_hover = start_button_rect.collidepoint(mouse_pos)
    bingo_hover = bingo_button_rect.collidepoint(mouse_pos)
    reset_hover = reset_button_rect.collidepoint(mouse_pos)
    
    # Tiempo para el efecto pulsante estilo neón
    current_time = pygame.time.get_ticks()
    pulse = 0.7 + 0.3 * math.sin(current_time / 500)
    
    # Colores de los botones según estado hover - nueva paleta
    start_color = cfg.BUTTON_HOVER_COLOR if start_hover else cfg.BUTTON_COLOR     # Naranja rojizo/Rojo
    bingo_color = cfg.BUTTON_HOVER_COLOR if bingo_hover else cfg.BUTTON_COLOR     # Naranja rojizo/Rojo
    reset_color = cfg.BUTTON_HOVER_COLOR if reset_hover else cfg.BUTTON_COLOR     # Naranja rojizo/Rojo
    
    # ==== BOTÓN INICIAR/SIGUIENTE ====
    # Efecto de resplandor exterior
    glow_color = cfg.GLOW_COLOR  # Dorado
    for i in range(4, 0, -1):
        glow_size = int(i * pulse * 1.5)  # Tamaño del resplandor varía con el pulso
        glow_rect = start_button_rect.inflate(glow_size, glow_size)
        pygame.draw.rect(screen, glow_color, glow_rect, border_radius=scale_value(12))

    # Rectángulo principal del botón
    pygame.draw.rect(screen, start_color, start_button_rect, border_radius=scale_value(10))
    pygame.draw.rect(screen, cfg.BORDER_COLOR, start_button_rect, scale_value(2), border_radius=scale_value(10))  # Naranja

    # Texto INICIAR/SIGUIENTE con sombra para efecto 3D
    button_text = "INICIAR" if not game_state.game_started else "SIGUIENTE"
    start_text = fonts["button"].render(button_text, True, cfg.TEXT_COLOR)  # Blanco
    text_shadow = fonts["button"].render(button_text, True, cfg.BLACK)
    
    # Posición del texto
    text_rect = start_text.get_rect(center=start_button_rect.center)
    shadow_rect = text_shadow.get_rect(center=(text_rect.centerx + scale_value(2), text_rect.centery + scale_value(2)))
    
    # Dibujar sombra primero, luego el texto
    screen.blit(text_shadow, shadow_rect)
    screen.blit(start_text, text_rect)
    
    # ==== BOTÓN BINGO ====
    # Efecto de resplandor si el juego está en curso
    if game_state.game_started and not game_state.game_over:
        glow_color = cfg.ALT_GLOW_COLOR  # Amarillo
        for i in range(3, 0, -1):
            glow_size = int(i * pulse * 1.5)
            glow_rect = bingo_button_rect.inflate(glow_size, glow_size)
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=scale_value(12))
    
    # Rectángulo principal del botón
    pygame.draw.rect(screen, bingo_color, bingo_button_rect, border_radius=scale_value(10))
    pygame.draw.rect(screen, cfg.BORDER_COLOR, bingo_button_rect, scale_value(2), border_radius=scale_value(10))  # Naranja
    
    # Texto BINGO con sombra
    bingo_text = fonts["button"].render("BINGO", True, cfg.TEXT_COLOR)  # Blanco
    bingo_shadow = fonts["button"].render("BINGO", True, cfg.BLACK)
    
    text_rect = bingo_text.get_rect(center=bingo_button_rect.center)
    shadow_rect = bingo_shadow.get_rect(center=(text_rect.centerx + scale_value(2), text_rect.centery + scale_value(2)))
    
    screen.blit(bingo_shadow, shadow_rect)
    screen.blit(bingo_text, text_rect)
    
    # ==== BOTÓN REINICIAR ====
    # Efecto de resplandor para el botón reiniciar
    glow_color = cfg.FRAME_COLOR  # Plateado
    for i in range(3, 0, -1):
        glow_size = int(i * pulse * 1.5)
        glow_rect = reset_button_rect.inflate(glow_size, glow_size)
        pygame.draw.rect(screen, glow_color, glow_rect, border_radius=scale_value(12))
        
    # Botón REINICIAR
    pygame.draw.rect(screen, reset_color, reset_button_rect, border_radius=scale_value(10))
    pygame.draw.rect(screen, cfg.BORDER_COLOR, reset_button_rect, scale_value(2), border_radius=scale_value(10))  # Naranja
    
    # Texto REINICIAR con sombra
    reset_text = fonts["button"].render("REINICIAR", True, cfg.TEXT_COLOR)  # Blanco
    reset_shadow = fonts["button"].render("REINICIAR", True, cfg.BLACK)
    
    text_rect = reset_text.get_rect(center=reset_button_rect.center)
    shadow_rect = reset_shadow.get_rect(center=(text_rect.centerx + scale_value(2), text_rect.centery + scale_value(2)))
    
    screen.blit(reset_shadow, shadow_rect)
    screen.blit(reset_text, text_rect)

def draw_current_number():
    if game_state.current_number is not None:
        # Marco para el número actual con estilo Vegas - posicionado a la izquierda y escalado
        frame_width = scale_value(220)
        frame_height = scale_value(240, False)
        frame_x = scale_value(70)
        frame_y = scale_value(200, False)
        
        # Efecto pulsante para el marco
        current_time = pygame.time.get_ticks()
        pulse = 0.5 + 0.5 * math.sin(current_time / 500)  # Pulsación suave para efecto neón
    
        # Determinar el color basado en el rango del número actual - con nueva paleta
        if game_state.current_number <= 30:
            number_color = cfg.BUTTON_COLOR  # Rojo
            glow_color = (180, 0, 0)         # Rojo brillante para neón
        elif game_state.current_number <= 60:
            number_color = cfg.GLOW_COLOR    # Dorado
            glow_color = (255, 215, 0)       # Dorado brillante para neón
        else:
            number_color = cfg.BORDER_COLOR  # Naranja
            glow_color = (255, 165, 0)       # Naranja brillante para neón
            
        # Aplicar efecto de escala con animación más llamativa para estilo Vegas
        scale = 1.0
        if game_state.number_animation_active:
            elapsed = pygame.time.get_ticks() - game_state.number_animation_start
            progress = min(1.0, elapsed / game_state.number_animation_duration)
            
            # Efecto de aparición con rebote para estilo Vegas
            if progress < 0.5:
                scale = 0.5 + 1.2 * progress  # Crece rápido y se pasa
            else:
                scale = 1.1 - 0.1 * (progress - 0.5) * 2  # Se estabiliza
                
            # Desactivar la animación cuando termine
            if progress >= 1.0:
                game_state.number_animation_active = False
        
        # Posición común para todos los elementos - alineados a la misma altura
        common_y = 110  # Altura común para todos los elementos principales
        
        # Dimensiones para el marco estilo Las Vegas
        rect_width = 200 * scale  
        rect_height = 200 * scale
        
        # Nueva posición: lado izquierdo alineado con el tablero y el historial
        rect_center = (rect_width // 2 + 20, common_y + rect_height // 2)
        rect_pos = (rect_center[0] - rect_width // 2, rect_center[1] - rect_height // 2)
        
        # Efecto de brillo neón alrededor del número actual
        current_time = pygame.time.get_ticks()
        pulse = 0.7 + 0.3 * math.sin(current_time / 500)  # Pulsación para efecto neón
        
        # Crear efecto de resplandor neón alrededor del rectángulo principal
        for i in range(6, 0, -1):
            glow_size = i * pulse
            glow_rect = pygame.Rect(
                rect_pos[0] - glow_size,
                rect_pos[1] - glow_size,
                rect_width + glow_size * 2,
                rect_height + glow_size * 2
            )
            alpha = int(40 - i * 6)  # Disminuir alpha gradualmente
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            s.fill((*glow_color, alpha))  # Color según rango con transparencia
            screen.blit(s, (glow_rect.x, glow_rect.y))
        
        # Estilo Vegas: rectángulo con bordes redondeados
        pygame.draw.rect(screen, cfg.WHITE, 
                       (rect_pos[0], rect_pos[1], rect_width, rect_height), 
                       border_radius=10)
        
        # Borde neón
        pygame.draw.rect(screen, number_color, 
                       (rect_pos[0], rect_pos[1], rect_width, rect_height), 3, 
                       border_radius=10)
        
        # Sombra para el número (efecto Vegas)
        shadow_offset = 4
        
        # Texto con sombra para efecto retro
        shadow_text = font_big.render(str(game_state.current_number), True, cfg.BLACK)
        shadow_rect = shadow_text.get_rect(center=(rect_center[0]+shadow_offset, rect_center[1]+shadow_offset))
        screen.blit(shadow_text, shadow_rect)
        
        # Dibujar el número grande con tipografía sans-serif
        number_text = font_big.render(str(game_state.current_number), True, number_color)
        text_rect = number_text.get_rect(center=rect_center)
        screen.blit(number_text, text_rect)
        
        # Título con estilo Las Vegas (más llamativo)
        # Sombra para el texto - texto más corto para que quepa en el marco
        shadow_label = font_small.render("NÚMERO", True, cfg.BLACK)
        shadow_label_rect = shadow_label.get_rect(center=(rect_center[0]+2, rect_center[1] - rect_height // 2 - 15 + 2))
        screen.blit(shadow_label, shadow_label_rect)
        
        # Texto principal dorado estilo Vegas
        label_text = font_small.render("NÚMERO", True, cfg.GLOW_COLOR)
        label_rect = label_text.get_rect(center=(rect_center[0], rect_center[1] - rect_height // 2 - 15))
        screen.blit(label_text, label_rect)
        
        # Contador con estilo Vegas (dorado brillante)
        # Sombra para el contador
        shadow_count = font_medium.render(f"{len(game_state.drawn_numbers)}/90", True, cfg.BLACK)
        shadow_count_rect = shadow_count.get_rect(center=(rect_center[0]+2, rect_center[1] + rect_height // 2 + 30 + 2))
        screen.blit(shadow_count, shadow_count_rect)
        
        # Contador principal
        count_text = font_medium.render(f"{len(game_state.drawn_numbers)}/90", True, cfg.VEGAS_GOLD)
        count_rect = count_text.get_rect(center=(rect_center[0], rect_center[1] + rect_height // 2 + 30))
        screen.blit(count_text, count_rect)

def select_number():
    """Selecciona un número aleatorio del rango disponible."""
    available_numbers = [i for i in range(1, cfg.TOTAL_NUMBERS + 1) if i not in game_state.drawn_numbers]
    if available_numbers:
        number = random.choice(available_numbers)
        game_state.current_number = number
        game_state.drawn_numbers.add(number)
        game_state.balls.append(Ball(number))
        
        # Activar animación para el nuevo número
        game_state.number_animation_start = pygame.time.get_ticks()
        game_state.number_animation_active = True
        
        return number
    else:
        game_state.game_over = True
        return None

def draw_number_history():
    """Dibuja el historial de números sorteados con estilo retro Las Vegas."""
    # Definir área para el historial con más espacio y diseño Vegas
    history_rect = pygame.Rect(cfg.WIDTH - scale_value(200), scale_value(110), scale_value(180), scale_value(400))
    
    # Efecto de brillo neón alrededor del historial
    for i in range(5, 0, -1):
        glow_rect = pygame.Rect(history_rect.x-i, history_rect.y-i, history_rect.width+i*2, history_rect.height+i*2)
        alpha = int(50 - i * 8)  # Disminuir alpha gradualmente
        s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        s.fill((255, 165, 0, alpha))  # Naranja con transparencia (nueva paleta)
        screen.blit(s, (glow_rect.x, glow_rect.y))
    
    # Marco estilo Vegas
    pygame.draw.rect(screen, cfg.WHITE, history_rect, border_radius=10)
    pygame.draw.rect(screen, cfg.BORDER_COLOR, history_rect, 2, border_radius=10)
    
    # Título del historial con estilo Vegas
    # Sombra para el título - usando fuente pequeña para que quepa en el marco
    shadow_title = font_small.render("HISTORIAL", True, cfg.BLACK)
    shadow_title_rect = shadow_title.get_rect(midtop=(history_rect.centerx+2, history_rect.top + scale_value(15)+2))
    screen.blit(shadow_title, shadow_title_rect)
    
    # Título principal con color dorado Vegas
    title_text = font_small.render("HISTORIAL", True, cfg.GLOW_COLOR)
    title_rect = title_text.get_rect(midtop=(history_rect.centerx, history_rect.top + scale_value(15)))
    screen.blit(title_text, title_rect)
    
    if not game_state.drawn_numbers:
        # Mensaje cuando no hay números - estilo Vegas con nueva paleta
        text_shadow = font_medium.render("Sin números", True, cfg.BLACK)
        text_rect_shadow = text_shadow.get_rect(center=(history_rect.centerx+2, history_rect.centery+2))
        screen.blit(text_shadow, text_rect_shadow)
        
        text = font_medium.render("Sin números", True, cfg.BUTTON_COLOR)  # Rojo de la nueva paleta
        text_rect = text.get_rect(center=(history_rect.centerx, history_rect.centery))
        screen.blit(text, text_rect)
        return
    
    # Organizar en una cuadrícula de 3 columnas
    sorted_numbers = sorted(game_state.drawn_numbers)
    cols = 3
    rows = (len(sorted_numbers) + cols - 1) // cols
    
    cell_width = (history_rect.width - 30) // cols  # Más espacio entre columnas
    cell_height = 34  # Celdas más grandes para estilo Vegas
    
    # Títulos de rango con estilo Vegas - nueva paleta de colores
    range_titles = ["1-30", "31-60", "61-90"]
    # Nuevos colores para los rangos según la nueva paleta
    range_colors = [cfg.BUTTON_COLOR, cfg.GLOW_COLOR, cfg.BORDER_COLOR]  # Rojo, Dorado, Naranja
    
    # Barra de títulos con rangos - más espaciada
    range_bar_y = history_rect.top + scale_value(50)
    range_bar_height = scale_value(30)
    range_bar = pygame.Rect(history_rect.left + scale_value(10), range_bar_y, history_rect.width - scale_value(20), range_bar_height)
    pygame.draw.rect(screen, cfg.FRAME_COLOR, range_bar, border_radius=5)  # Usando plateado
    
    # Etiquetas individuales para evitar superposición
    for i in range(3):
        # Calcular posición para cada rango - distribuidos horizontalmente con más espacio
        label_width = scale_value(45)  # Ancho reducido para las etiquetas
        x_pos = history_rect.left + scale_value(15) + i * (label_width + scale_value(10))
        
        # Mini rectángulo para cada etiqueta
        label_rect = pygame.Rect(x_pos, range_bar_y, label_width, range_bar_height)
        pygame.draw.rect(screen, cfg.BLACK, label_rect, 1, border_radius=3)
        
        # Texto con sombra - fuente más pequeña para que quepa
        shadow_text = font_smallest.render(range_titles[i], True, cfg.BLACK)
        shadow_rect = shadow_text.get_rect(center=(label_rect.centerx + 1, label_rect.centery + 1))
        screen.blit(shadow_text, shadow_rect)
        
        # Texto principal
        range_text = font_smallest.render(range_titles[i], True, range_colors[i])
        range_rect = range_text.get_rect(center=(label_rect.centerx, label_rect.centery))
        screen.blit(range_text, range_rect)
    
    for i, num in enumerate(sorted_numbers):
        # Calcular posición en la cuadrícula
        col = i % cols
        row = i // cols
        
        # Si hay demasiados números, dejar de dibujar para evitar salirse del área
        if row >= 9:  # Aumentamos a 9 filas (27 números) visibles con el nuevo diseño
            # Indicador con estilo Vegas de que hay más números
            more_shadow = font_small.render(f"+ {len(sorted_numbers) - 27} más", True, cfg.BLACK)
            more_shadow_rect = more_shadow.get_rect(center=(history_rect.centerx+1, history_rect.bottom - 25+1))
            screen.blit(more_shadow, more_shadow_rect)
            
            more_text = font_small.render(f"+ {len(sorted_numbers) - 27} más", True, cfg.GLOW_COLOR)  # Dorado
            more_rect = more_text.get_rect(center=(history_rect.centerx, history_rect.bottom - 25))
            screen.blit(more_text, more_rect)
            break
        
        # Posición de la celda
        x = history_rect.left + 15 + col * cell_width
        y = history_rect.top + 85 + row * cell_height
        
        # Determinar color basado en el rango del número - nueva paleta Vegas
        if num <= 30:
            number_color = cfg.RANGE_1_30     # Rojo para números 1-30
            glow_color = (180, 0, 0)         # Rojo brillante para neón
        elif num <= 60:
            number_color = cfg.RANGE_31_60    # Dorado para números 31-60
            glow_color = (255, 215, 0)       # Dorado brillante para neón
        else:
            number_color = cfg.RANGE_61_90    # Naranja para números 61-90
            glow_color = (255, 165, 0)       # Naranja brillante para neón
        
        # Dibujar celda con estilo Vegas
        cell_rect = pygame.Rect(x, y, cell_width - 10, cell_height - 6)
        
        # Destacar el número actual con efecto neón usando la nueva paleta
        if num == game_state.current_number:
            # Efecto de brillo para el número actual con el color según su rango
            for i in range(3, 0, -1):
                glow_rect = pygame.Rect(cell_rect.x-i, cell_rect.y-i, cell_rect.width+i*2, cell_rect.height+i*2)
                alpha = int(80 - i * 20) 
                s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                s.fill((*glow_color, alpha))  # Color basado en el rango con transparencia
                screen.blit(s, (glow_rect.x, glow_rect.y))
                
            # Número actual con fondo según su rango
            pygame.draw.rect(screen, number_color, cell_rect, border_radius=5)
            # Usar color de texto con buen contraste
            text_color = cfg.BLACK if num > 30 and num <= 60 else cfg.TEXT_COLOR  # Negro para dorado, blanco para rojo/naranja
            num_text = font_small.render(str(num), True, text_color)
        else:
            # Números normales con borde de color según rango
            pygame.draw.rect(screen, cfg.WHITE, cell_rect, border_radius=5)
            pygame.draw.rect(screen, number_color, cell_rect, 1, border_radius=5)
            num_text = font_small.render(str(num), True, number_color)
        
        # Número con tipografía sans-serif
        num_rect = num_text.get_rect(center=cell_rect.center)
        screen.blit(num_text, num_rect)

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
            # Usar fuente sans-serif para estilo Vegas
            bingo_font = pygame.font.SysFont(font_names, font_size, bold=True)
            
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
                winner_font = pygame.font.SysFont(font_names, winner_size, bold=True)
                
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
            continue_font = pygame.font.SysFont(font_names, 30, bold=True)
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
        pygame.draw.rect(screen, cfg.VEGAS_BLUE, timer_rect, 2, border_radius=5)
        
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
        pygame.draw.rect(screen, cfg.VEGAS_MEDIUM_GRAY, inner_rect, border_radius=6)
        
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
    
    # Reiniciar posiciones de pelotas
    Ball.reset_positions()
    
    # Reinicializar el tablero
    game_state.initialize_board()
    
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
            select_number()
            game_state.number_animation_start = pygame.time.get_ticks()
    
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
    
    # Actualizar todas las pelotas
    for ball in game_state.balls:
        ball.update()
    
    # --------- RENDERIZADO ----------
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
    
    # Dibujar las pelotas
    for ball in game_state.balls:
        ball.draw()
    
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
    
    # Recargar fuentes si la resolución cambió (solo durante pruebas)
    if cfg.WIDTH != int(BASE_WIDTH * SCALE_X) or cfg.HEIGHT != int(BASE_HEIGHT * SCALE_Y):
        # Actualizar factores de escala
        SCALE_X = cfg.WIDTH / BASE_WIDTH
        SCALE_Y = cfg.HEIGHT / BASE_HEIGHT
        # Recargar fuentes con nuevos tamaños
        load_responsive_fonts()
    
    # Actualizar la pantalla y controlar FPS
    pygame.display.flip()
    clock.tick(60)



pygame.quit()
sys.exit()

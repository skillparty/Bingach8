"""
Pantalla de título moderna para el juego Bingacho
Diseño elegante con animaciones fluidas y efectos visuales modernos
"""

import pygame
import math
import random
import time
from pygame.locals import *
import config as cfg
from dataclasses import dataclass

@dataclass
class BinaryBackgroundConfig:
    """Configuración para el fondo binario animado"""
    density: float = 0.7
    animation_speed: float = 1.0
    base_opacity: float = 0.3
    text_opacity: float = 0.5
    transition_duration: float = 1.25
    color_scheme: tuple = (100, 150, 200)

@dataclass
class BinaryChar:
    """Estructura de datos para un carácter binario"""
    value: int
    target_value: int
    transition_time: float
    opacity: float
    is_text: bool
    text_char: str

class BinaryBackground:
    """Fondo binario animado inspirado en VS Code"""
    
    def __init__(self, width, height, config=None):
        self.width = width
        self.height = height
        self.config = config or BinaryBackgroundConfig()
        
        # Configuración de fuente más grande
        self.char_size = 18  # Aumentado de 13 a 18
        self.line_height = 22  # Aumentado proporcionalmente
        self.font = pygame.font.Font(None, self.char_size)
        
        # Calcular dimensiones de la grilla
        self.cols = int(width // self.char_size)
        self.rows = int(height // self.line_height)
        
        # Inicializar componentes
        self.grid = self._generate_initial_grid()
        self.text_positions = self._calculate_text_positions()
        self.animation_time = 0
        
    def _generate_initial_grid(self):
        """Genera la matriz inicial de caracteres binarios"""
        grid = []
        for row in range(self.rows):
            grid_row = []
            for col in range(self.cols):
                value = random.randint(0, 1)
                target_value = random.randint(0, 1)
                
                char = BinaryChar(
                    value=value,
                    target_value=target_value,
                    transition_time=0.0,
                    opacity=random.uniform(0.1, self.config.base_opacity),
                    is_text=False,
                    text_char=""
                )
                grid_row.append(char)
            grid.append(grid_row)
        return grid
    
    def _calculate_text_positions(self):
        """Calcula posiciones para el texto 'Bingacho_joseAlejandro'"""
        text = "Bingacho_joseAlejandro"
        positions = []
        
        for i in range(3):
            attempts = 0
            while attempts < 10:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, max(0, self.cols - len(text)))
                
                center_row = self.rows // 2
                center_col = self.cols // 2
                
                if (abs(row - center_row) > 5 or abs(col - center_col) > 15):
                    positions.append({
                        'row': row,
                        'col': col,
                        'text': text,
                        'fade_state': random.uniform(0, 1),
                        'visible': True
                    })
                    break
                attempts += 1
        
        return positions
    
    def update(self, delta_time):
        """Actualiza la animación del fondo binario"""
        self.animation_time += delta_time
        
        for row in range(self.rows):
            for col in range(self.cols):
                char = self.grid[row][col]
                
                char.transition_time += delta_time * self.config.animation_speed
                
                if char.transition_time >= self.config.transition_duration:
                    char.value = char.target_value
                    char.target_value = random.randint(0, 1)
                    char.transition_time = 0.0
                
                base_opacity = self.config.base_opacity
                opacity_variation = 0.1 * math.sin(self.animation_time * 2 + row * 0.1 + col * 0.1)
                char.opacity = max(0.05, base_opacity + opacity_variation)
        
        for text_pos in self.text_positions:
            text_pos['fade_state'] += delta_time * 0.5
            if text_pos['fade_state'] > 2.0:
                text_pos['fade_state'] = 0.0
    
    def draw(self, surface):
        """Renderiza el fondo binario en la superficie"""
        binary_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        for row in range(self.rows):
            for col in range(self.cols):
                char = self.grid[row][col]
                
                x = col * self.char_size
                y = row * self.line_height
                
                display_char = str(char.value)
                is_text_char = False
                
                for text_pos in self.text_positions:
                    if (text_pos['row'] == row and 
                        col >= text_pos['col'] and 
                        col < text_pos['col'] + len(text_pos['text']) and
                        text_pos['visible']):
                        
                        char_index = col - text_pos['col']
                        display_char = text_pos['text'][char_index]
                        is_text_char = True
                        break
                
                if is_text_char:
                    opacity = int(255 * self.config.text_opacity * 
                                (0.7 + 0.3 * math.sin(text_pos['fade_state'] * math.pi)))
                    color = (*self.config.color_scheme, opacity)
                else:
                    opacity = int(255 * char.opacity)
                    color = (*self.config.color_scheme, opacity)
                
                if opacity > 10:
                    char_surface = self.font.render(display_char, True, color[:3])
                    char_surface.set_alpha(opacity)
                    binary_surface.blit(char_surface, (x, y))
        
        surface.blit(binary_surface, (0, 0))

class FloatingParticle:
    """Partícula flotante moderna con efectos suaves y números del bingo"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.size = random.randint(25, 40)  # Tamaño mucho más grande
        self.speed = random.uniform(0.5, 2.0)
        self.amplitude = random.uniform(20, 60)
        self.frequency = random.uniform(0.01, 0.03)
        self.phase = random.uniform(0, math.pi * 2)
        self.opacity = random.uniform(0.4, 0.9)  # Más opacidad
        self.color = random.choice([
            cfg.PRIMARY_COLOR,
            cfg.SECONDARY_COLOR,
            cfg.HIGHLIGHT_COLOR,
            cfg.WHITE
        ])
        self.life_time = 0
        self.number = random.randint(1, 90)  # Número aleatorio del 1 al 90
        self.font = pygame.font.Font(None, int(self.size * 0.8))  # Fuente proporcional al tamaño
        
    def update(self, delta_time):
        self.life_time += delta_time
        
        # Movimiento ondulatorio suave
        self.x = self.base_x + math.sin(self.life_time * self.frequency + self.phase) * self.amplitude
        self.y = self.base_y + math.cos(self.life_time * self.frequency * 0.7 + self.phase) * self.amplitude * 0.5
        
        # Movimiento vertical lento
        self.base_y -= self.speed * delta_time * 10
        
        # Reiniciar si sale de la pantalla
        if self.base_y < -50:
            self.base_y = cfg.HEIGHT + 50
            self.base_x = random.randint(0, cfg.WIDTH)
            self.number = random.randint(1, 90)  # Nuevo número aleatorio
            
        # Variación de opacidad
        self.opacity = 0.4 + 0.5 * abs(math.sin(self.life_time * 0.02))
        
    def draw(self, surface):
        alpha = int(255 * self.opacity)
        color_with_alpha = (*self.color[:3], alpha)
        
        # Crear superficie con alpha más grande
        particle_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        
        # Efecto de brillo más pronunciado
        for i in range(5, 0, -1):
            glow_alpha = alpha // (i + 1)
            glow_color = (*self.color[:3], glow_alpha)
            pygame.draw.circle(particle_surface, glow_color, 
                             (self.size * 1.5, self.size * 1.5), self.size + i * 2)
        
        # Fondo circular de la partícula
        pygame.draw.circle(particle_surface, color_with_alpha, 
                         (int(self.size * 1.5), int(self.size * 1.5)), self.size)
        
        # Dibujar el número en el centro
        number_text = self.font.render(str(self.number), True, cfg.WHITE)
        number_rect = number_text.get_rect(center=(self.size * 1.5, self.size * 1.5))
        particle_surface.blit(number_text, number_rect)
        
        surface.blit(particle_surface, (self.x - self.size * 1.5, self.y - self.size * 1.5))

class TitleScreen:
    """Pantalla de título moderna y elegante"""
    
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Fuentes modernas con JetBrains Mono
        self.font_title = cfg.get_font(cfg.FONTS['SIZES']['TITLE'], bold=True)
        self.font_subtitle = cfg.get_font(cfg.FONTS['SIZES']['SUBTITLE'])
        self.font_button = cfg.get_font(cfg.FONTS['SIZES']['BODY'], bold=True)
        self.font_small = cfg.get_font(cfg.FONTS['SIZES']['SMALL'])
        
        # Configurar fondo binario más visible
        binary_config = BinaryBackgroundConfig(
            density=0.8,  # Más densidad
            animation_speed=1.0,
            base_opacity=0.25,  # Más opacidad
            text_opacity=0.4,   # Más opacidad para el texto
            color_scheme=(80, 120, 160)  # Colores más brillantes
        )
        self.binary_background = BinaryBackground(cfg.WIDTH, cfg.HEIGHT, binary_config)
        
        # Partículas flotantes (más cantidad)
        self.particles = []
        for _ in range(80):  # Aumentado de 50 a 80
            x = random.randint(0, cfg.WIDTH)
            y = random.randint(0, cfg.HEIGHT)
            self.particles.append(FloatingParticle(x, y))
        
        # Estado de animación
        self.animation_time = 0
        self.title_animation_phase = 0
        self.title_letters = "BINGACHO"
        self.visible_letters = 0
        self.letter_reveal_time = 0.3  # Tiempo entre letras
        self.last_letter_time = 0
        
        # Estado del menú
        self.show_game_menu = False
        self.selected_game_mode = 0  # 0 = normal, 1 = alterno
        
        # Botones de juego
        self.setup_buttons()
        
        # Efectos visuales
        self.pulse_time = 0
        self.glow_intensity = 0
        
        # Estado de animación para compatibilidad
        self.animation_started = False
        
    def start_animation(self):
        """Inicia la animación (compatibilidad con main.py)"""
        self.animation_started = True
        self.animation_time = 0
        
    def setup_buttons(self):
        """Configura los botones del menú"""
        button_width = 350
        button_height = 70
        
        # Botón principal de inicio
        self.start_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.start_button_rect.center = (cfg.WIDTH // 2, cfg.HEIGHT - 200)
        self.start_button_hover = False
        
        # Botones de modo de juego
        game_button_width = 400
        game_button_height = 80
        
        # Botón juego normal
        self.normal_game_rect = pygame.Rect(0, 0, game_button_width, game_button_height)
        self.normal_game_rect.center = (cfg.WIDTH // 2, cfg.HEIGHT // 2 + 100)
        self.normal_game_hover = False
        
        # Botón juego alterno
        self.alt_game_rect = pygame.Rect(0, 0, game_button_width, game_button_height)
        self.alt_game_rect.center = (cfg.WIDTH // 2, cfg.HEIGHT // 2 + 200)
        self.alt_game_hover = False
        
        # Botón volver
        back_button_width = 200
        back_button_height = 50
        self.back_button_rect = pygame.Rect(0, 0, back_button_width, back_button_height)
        self.back_button_rect.center = (cfg.WIDTH // 2, cfg.HEIGHT // 2 + 320)
        self.back_button_hover = False
        
    def update(self):
        """Actualiza todos los elementos de la pantalla"""
        delta_time = self.clock.tick(60) / 1000.0
        self.animation_time += delta_time
        self.pulse_time += delta_time
        
        # Actualizar fondo binario
        self.binary_background.update(delta_time)
        
        # Actualizar partículas
        for particle in self.particles:
            particle.update(delta_time)
        
        # Animación del título
        self.update_title_animation(delta_time)
        
        # Efectos de brillo
        self.glow_intensity = 0.5 + 0.5 * math.sin(self.pulse_time * 2)
        
    def update_title_animation(self, delta_time):
        """Actualiza la animación del título"""
        if self.animation_time > 1.0:  # Esperar 1 segundo antes de empezar
            if self.visible_letters < len(self.title_letters):
                if self.animation_time - self.last_letter_time > self.letter_reveal_time:
                    self.visible_letters += 1
                    self.last_letter_time = self.animation_time
            else:
                # Reiniciar después de 5 segundos
                if self.animation_time - self.last_letter_time > 5.0:
                    self.visible_letters = 0
                    self.last_letter_time = self.animation_time
    
    def handle_event(self, event):
        """Maneja los eventos de entrada"""
        if event.type == MOUSEMOTION:
            if not self.show_game_menu:
                self.start_button_hover = self.start_button_rect.collidepoint(event.pos)
            else:
                self.normal_game_hover = self.normal_game_rect.collidepoint(event.pos)
                self.alt_game_hover = self.alt_game_rect.collidepoint(event.pos)
                self.back_button_hover = self.back_button_rect.collidepoint(event.pos)
                
        elif event.type == MOUSEBUTTONDOWN:
            if not self.show_game_menu:
                if self.start_button_rect.collidepoint(event.pos):
                    self.show_game_menu = True
            else:
                if self.normal_game_rect.collidepoint(event.pos):
                    return "start_normal_game"
                elif self.alt_game_rect.collidepoint(event.pos):
                    return "start_alt_game"
                elif self.back_button_rect.collidepoint(event.pos):
                    self.show_game_menu = False
                    
        elif event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_RETURN:
                if not self.show_game_menu:
                    self.show_game_menu = True
                else:
                    return "start_normal_game"  # Por defecto juego normal
            elif event.key == K_ESCAPE:
                if self.show_game_menu:
                    self.show_game_menu = False
                else:
                    return "exit_game"
        return None
    
    def draw(self):
        """Dibuja toda la pantalla"""
        # Fondo degradado
        self.draw_gradient_background()
        
        # Fondo binario
        self.binary_background.draw(self.screen)
        
        # Partículas flotantes
        for particle in self.particles:
            particle.draw(self.screen)
        
        if not self.show_game_menu:
            # Pantalla principal
            # Título principal
            self.draw_title()
            
            # Subtítulo
            self.draw_subtitle()
            
            # Botón de inicio
            self.draw_start_button()
            
            # Instrucciones
            self.draw_instructions()
        else:
            # Menú de selección de juego
            self.draw_game_menu()
        
    def draw_gradient_background(self):
        """Dibuja un fondo con degradado moderno"""
        for y in range(cfg.HEIGHT):
            ratio = y / cfg.HEIGHT
            
            # Degradado de azul oscuro a negro
            r = int(15 * (1 - ratio))
            g = int(25 * (1 - ratio))
            b = int(45 * (1 - ratio))
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (cfg.WIDTH, y))
    
    def draw_title(self):
        """Dibuja el título con animación letra por letra"""
        title_y = cfg.HEIGHT // 2 - 100
        
        # Mostrar solo las letras visibles
        visible_text = self.title_letters[:self.visible_letters]
        
        if visible_text:
            # Efecto de brillo
            for i in range(5, 0, -1):
                glow_alpha = int(30 * self.glow_intensity / i)
                glow_surface = pygame.Surface((cfg.WIDTH, 200), pygame.SRCALPHA)
                
                glow_text = self.font_title.render(visible_text, True, 
                                                 (*cfg.HIGHLIGHT_COLOR[:3], glow_alpha))
                glow_rect = glow_text.get_rect(center=(cfg.WIDTH // 2 + i, title_y + i))
                glow_surface.blit(glow_text, glow_rect)
                self.screen.blit(glow_surface, (0, 0))
            
            # Sombra
            shadow_text = self.font_title.render(visible_text, True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(cfg.WIDTH // 2 + 3, title_y + 3))
            self.screen.blit(shadow_text, shadow_rect)
            
            # Texto principal
            main_text = self.font_title.render(visible_text, True, cfg.HIGHLIGHT_COLOR)
            main_rect = main_text.get_rect(center=(cfg.WIDTH // 2, title_y))
            self.screen.blit(main_text, main_rect)
    
    def draw_subtitle(self):
        """Dibuja el subtítulo"""
        subtitle_y = cfg.HEIGHT // 2 + 50
        subtitle_text = "Bingach8 by joseAlejandro"
        
        # Sombra
        shadow = self.font_subtitle.render(subtitle_text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(cfg.WIDTH // 2 + 2, subtitle_y + 2))
        self.screen.blit(shadow, shadow_rect)
        
        # Texto principal
        text = self.font_subtitle.render(subtitle_text, True, cfg.PRIMARY_COLOR)
        text_rect = text.get_rect(center=(cfg.WIDTH // 2, subtitle_y))
        self.screen.blit(text, text_rect)
        
        # Línea decorativa
        line_y = subtitle_y + 30
        line_start = cfg.WIDTH // 2 - 150
        line_end = cfg.WIDTH // 2 + 150
        
        for i in range(3):
            alpha = int(255 * (1 - i * 0.3))
            color = (*cfg.PRIMARY_COLOR[:3], alpha)
            pygame.draw.line(self.screen, color, 
                           (line_start, line_y + i), (line_end, line_y + i), 2)
    
    def draw_start_button(self):
        """Dibuja el botón de inicio moderno"""
        # Color del botón
        if self.start_button_hover:
            button_color = cfg.SECONDARY_COLOR
            glow_size = 8
        else:
            button_color = cfg.PRIMARY_COLOR
            glow_size = 4
        
        # Efecto de brillo
        for i in range(glow_size, 0, -1):
            glow_alpha = int(50 * self.glow_intensity / i)
            glow_rect = self.start_button_rect.inflate(i * 2, i * 2)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_surface.fill((*button_color[:3], glow_alpha))
            self.screen.blit(glow_surface, glow_rect)
        
        # Botón principal
        pygame.draw.rect(self.screen, button_color, self.start_button_rect, border_radius=15)
        pygame.draw.rect(self.screen, cfg.WHITE, self.start_button_rect, 2, border_radius=15)
        
        # Texto del botón
        button_text = self.font_button.render("SELECCIONAR JUEGO", True, cfg.WHITE)
        button_rect = button_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(button_text, button_rect)
    
    def draw_game_menu(self):
        """Dibuja el menú de selección de modo de juego"""
        # Título del menú
        menu_title = self.font_title.render("SELECCIONA MODO", True, cfg.HIGHLIGHT_COLOR)
        title_rect = menu_title.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2 - 100))
        
        # Sombra del título
        shadow_title = self.font_title.render("SELECCIONA MODO", True, (0, 0, 0))
        shadow_rect = shadow_title.get_rect(center=(cfg.WIDTH // 2 + 3, cfg.HEIGHT // 2 - 97))
        self.screen.blit(shadow_title, shadow_rect)
        self.screen.blit(menu_title, title_rect)
        
        # Botón Juego Normal
        normal_color = cfg.PRIMARY_COLOR if not self.normal_game_hover else cfg.SECONDARY_COLOR
        glow_size = 8 if self.normal_game_hover else 4
        
        # Efecto de brillo para juego normal
        for i in range(glow_size, 0, -1):
            glow_alpha = int(50 * self.glow_intensity / i)
            glow_rect = self.normal_game_rect.inflate(i * 2, i * 2)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_surface.fill((*normal_color[:3], glow_alpha))
            self.screen.blit(glow_surface, glow_rect)
        
        pygame.draw.rect(self.screen, normal_color, self.normal_game_rect, border_radius=15)
        pygame.draw.rect(self.screen, cfg.WHITE, self.normal_game_rect, 3, border_radius=15)
        
        # Texto del botón normal
        normal_title = self.font_button.render("JUEGO NORMAL", True, cfg.WHITE)
        normal_desc = self.font_small.render("Tablero 9x10 - Números 1 al 90", True, cfg.LIGHT_GRAY)
        
        normal_title_rect = normal_title.get_rect(center=(self.normal_game_rect.centerx, self.normal_game_rect.centery - 15))
        normal_desc_rect = normal_desc.get_rect(center=(self.normal_game_rect.centerx, self.normal_game_rect.centery + 15))
        
        self.screen.blit(normal_title, normal_title_rect)
        self.screen.blit(normal_desc, normal_desc_rect)
        
        # Botón Juego Alterno
        alt_color = cfg.ACCENT_COLOR if not self.alt_game_hover else cfg.SECONDARY_COLOR
        glow_size = 8 if self.alt_game_hover else 4
        
        # Efecto de brillo para juego alterno
        for i in range(glow_size, 0, -1):
            glow_alpha = int(50 * self.glow_intensity / i)
            glow_rect = self.alt_game_rect.inflate(i * 2, i * 2)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_surface.fill((*alt_color[:3], glow_alpha))
            self.screen.blit(glow_surface, glow_rect)
        
        pygame.draw.rect(self.screen, alt_color, self.alt_game_rect, border_radius=15)
        pygame.draw.rect(self.screen, cfg.WHITE, self.alt_game_rect, 3, border_radius=15)
        
        # Texto del botón alterno
        alt_title = self.font_button.render("JUEGO ALTERNO", True, cfg.WHITE)
        alt_desc = self.font_small.render("Tablero 7x11 - Números 1 al 75", True, cfg.LIGHT_GRAY)
        
        alt_title_rect = alt_title.get_rect(center=(self.alt_game_rect.centerx, self.alt_game_rect.centery - 15))
        alt_desc_rect = alt_desc.get_rect(center=(self.alt_game_rect.centerx, self.alt_game_rect.centery + 15))
        
        self.screen.blit(alt_title, alt_title_rect)
        self.screen.blit(alt_desc, alt_desc_rect)
        
        # Botón Volver
        back_color = cfg.GRAY if not self.back_button_hover else cfg.LIGHT_GRAY
        
        pygame.draw.rect(self.screen, back_color, self.back_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, cfg.WHITE, self.back_button_rect, 2, border_radius=10)
        
        back_text = self.font_small.render("VOLVER", True, cfg.WHITE)
        back_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_rect)
    
    def draw_instructions(self):
        """Dibuja las instrucciones"""
        instructions_y = cfg.HEIGHT - 100
        
        # Instrucción principal
        instruction1 = "Presiona ESPACIO, ENTER o haz clic para seleccionar modo"
        text1 = self.font_small.render(instruction1, True, cfg.LIGHT_GRAY)
        rect1 = text1.get_rect(center=(cfg.WIDTH // 2, instructions_y))
        self.screen.blit(text1, rect1)
        
        # Instrucción de salida
        instruction2 = "Presiona ESC para salir"
        text2 = self.font_small.render(instruction2, True, cfg.GRAY)
        rect2 = text2.get_rect(center=(cfg.WIDTH // 2, instructions_y + 25))
        self.screen.blit(text2, rect2)
        
        # Créditos
        credits = "Creado por Jose Alejandro"
        credits_text = self.font_small.render(credits, True, cfg.GRAY)
        credits_rect = credits_text.get_rect(center=(cfg.WIDTH // 2, instructions_y + 50))
        self.screen.blit(credits_text, credits_rect)

# Función principal para pruebas
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pygame.display.set_caption("Bingacho - Pantalla de Título")
    
    title_screen = TitleScreen(screen)
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            result = title_screen.handle_event(event)
            if result == "start_game":
                print("Iniciando juego...")
                running = False
            elif result == "exit_game":
                running = False
        
        title_screen.update()
        title_screen.draw()
        pygame.display.flip()
    
    pygame.quit()
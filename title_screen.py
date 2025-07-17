"""
Pantalla de título para el juego Bingacho
Incluye flipcards con unos y ceros formando "Bing8" y efecto de ola estilo Hokusai
"""

import pygame
import math
import random
import time
from pygame.locals import *
import config as cfg

class FlipCard:
    def __init__(self, x, y, size, value, target_value, delay=0):
        self.x = x
        self.y = y
        self.size = size
        self.initial_value = value
        self.target_value = target_value
        self.current_value = value
        self.delay = delay
        self.flip_progress = 0
        self.is_flipping = False
        self.flip_speed = 0.1
        self.start_time = 0
        self.animation_phase = 0  # 0 = inicial, 1 = objetivo
        self.cycle_time = 1.5  # Tiempo para un ciclo completo - más rápido
        
    def start_flip(self):
        if not self.is_flipping:
            if self.start_time == 0:  # Primera vez que se llama
                self.start_time = time.time()
            if time.time() > self.start_time + self.delay:
                self.is_flipping = True
                self.flip_progress = 0  # Reiniciar progreso
            
    def update(self):
        if self.start_time > 0:  # Solo si la animación ha comenzado
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.delay:
                # Alternar entre valor inicial y objetivo usando cycle_time
                cycle_progress = (elapsed_time - self.delay) % self.cycle_time
                
                if cycle_progress < (self.cycle_time / 2):
                    # Primera mitad: mostrar valor inicial (random)
                    self.current_value = self.initial_value
                else:
                    # Segunda mitad: mostrar valor objetivo (patrón de letra)
                    self.current_value = self.target_value
                
    def draw(self, screen):
        # Calcular el factor de escala para el efecto de flip
        scale_factor = abs(math.cos(self.flip_progress * math.pi)) if self.is_flipping else 1.0
        
        # Usar el valor actual
        display_value = self.current_value
            
        # Crear la superficie de la carta
        card_surface = pygame.Surface((self.size, self.size))
        
        # Color de fondo de la carta
        bg_color = cfg.HIGHLIGHT_COLOR if display_value == 1 else cfg.PRIMARY_COLOR
        card_surface.fill(bg_color)
        
        # Borde de la carta
        pygame.draw.rect(card_surface, cfg.BLACK, (0, 0, self.size, self.size), 2)
        
        # Texto del valor
        font = pygame.font.Font(None, int(self.size * 0.6))
        text_color = cfg.BLACK if display_value == 1 else cfg.WHITE
        text = font.render(str(display_value), True, text_color)
        text_rect = text.get_rect(center=(self.size // 2, self.size // 2))
        card_surface.blit(text, text_rect)
        
        # Aplicar escala horizontal para el efecto de flip
        scaled_width = int(self.size * scale_factor)
        if scaled_width > 0:
            scaled_surface = pygame.transform.scale(card_surface, (scaled_width, self.size))
            screen.blit(scaled_surface, (self.x - scaled_width // 2 + self.size // 2, self.y))

class WaveParticle:
    def __init__(self, x, y, amplitude, frequency, phase, color):
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.color = color
        self.life = 1.0
        self.size = random.randint(15, 25)  # Tamaño más grande para mostrar números
        self.number = random.randint(1, 90)  # Número aleatorio del 1 al 90
        
    def update(self, wave_time):
        # Movimiento ondulatorio estilo Hokusai
        self.x = self.base_x + math.sin(wave_time * self.frequency + self.phase) * self.amplitude * 0.5
        self.y = self.base_y + math.cos(wave_time * self.frequency * 0.7 + self.phase) * self.amplitude * 0.3
        
        # Efecto de desvanecimiento
        self.life -= 0.002
        if self.life <= 0:
            self.life = 1.0
            self.number = random.randint(1, 90)  # Cambiar número cuando se reinicia la partícula
            
    def draw(self, screen):
        alpha = int(255 * self.life)
        color_with_alpha = (*self.color, alpha)
        
        # Crear superficie con alpha para el número
        font = pygame.font.Font(None, self.size)
        text_surface = font.render(str(self.number), True, color_with_alpha)
        
        # Crear superficie con alpha
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Dibujar círculo de fondo semi-transparente
        bg_color = (*cfg.HIGHLIGHT_COLOR, alpha // 3)  # Fondo ámbar semi-transparente
        pygame.draw.circle(particle_surface, bg_color, (self.size, self.size), self.size // 2)
        
        # Centrar el texto en la superficie
        text_rect = text_surface.get_rect(center=(self.size, self.size))
        particle_surface.blit(text_surface, text_rect)
        
        screen.blit(particle_surface, (self.x - self.size, self.y - self.size))

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Configurar patrones para la animación
        self.setup_patterns()
        
        # Control del bucle de patrones
        self.current_pattern_index = 0
        self.pattern_change_interval = 3.0  # Cambiar cada 3 segundos
        self.last_pattern_change = time.time()
        
        # Configurar las cartas
        self.setup_cards()
        
        # Configurar partículas de ola
        self.setup_wave_particles()
        
        # Estado de animación
        self.animation_started = False
        self.animation_start_time = 0
        self.wave_time = 0
        self.pattern_duration = 2.0  # Duración de cada letra en segundos - más tiempo para apreciar
        self.flip_in_progress = False
        
        # Botón de iniciar
        self.button_rect = pygame.Rect(
            cfg.WIDTH // 2 - 150, 
            cfg.HEIGHT - 120, 
            300, 
            60
        )
        self.button_hover = False
        
    def setup_patterns(self):
        """Configura patrones individuales para cada letra de BINGO"""
        
        # Patrón para la letra "B" - 30 filas x 60 columnas
        self.b_pattern = [
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
        ]
        
        # Patrón para la letra "I" - 30 filas x 60 columnas
        self.i_pattern = [
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
        ]
        
        # Patrón para la letra "N" - 30 filas x 60 columnas
        self.n_pattern = [
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
        ]
        
        # Patrón para la letra "G" - 30 filas x 60 columnas
        self.g_pattern = [
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
        ]

        # Patrón para la letra "O" - 30 filas x 60 columnas
        self.o_pattern = [
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
            [0]*60,
        ]

        # Lista de patrones - cada letra individual
        self.patterns = [self.b_pattern, self.i_pattern, self.n_pattern, self.g_pattern, self.o_pattern]

    def setup_cards(self):
        self.cards = []
        # Configuración de las cartas para matriz 30x60
        rows, cols = 30, 60
        card_size = 10  # Tamaño de carta más pequeño para matriz más grande
        spacing = 2     # Espaciado reducido
        
        # Calcular posición inicial para centrar la matriz
        total_width = cols * (card_size + spacing) - spacing
        total_height = rows * (card_size + spacing) - spacing
        start_x = (cfg.WIDTH - total_width) // 2
        start_y = (cfg.HEIGHT - total_height) // 2 - 80
        
        # Usar el patrón actual del bucle
        current_pattern = self.patterns[self.current_pattern_index]
        
        # Crear las cartas
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (card_size + spacing)
                y = start_y + row * (card_size + spacing)
                
                # Valor inicial aleatorio (0 o 1)
                initial_value = random.randint(0, 1)
                # Verificar límites del patrón
                if row < len(current_pattern) and col < len(current_pattern[0]):
                    target_value = current_pattern[row][col]
                else:
                    target_value = 0  # Valor por defecto fuera del patrón
                
                # Retraso progresivo basado en la distancia del centro
                center_x = cols // 2
                center_y = rows // 2
                distance = math.sqrt((col - center_x) ** 2 + (row - center_y) ** 2)
                delay = distance * 0.03  # Retraso ajustado para mejor visualización
                
                card = FlipCard(x, y, card_size, initial_value, target_value, delay)
                self.cards.append(card)
    
    def setup_wave_particles(self):
        self.wave_particles = []
        
        # Crear partículas para el efecto de ola
        for i in range(200):
            x = random.randint(0, cfg.WIDTH)
            y = random.randint(0, cfg.HEIGHT)
            amplitude = random.randint(20, 80)
            frequency = random.uniform(0.5, 2.0)
            phase = random.uniform(0, 2 * math.pi)
            color = random.choice([cfg.HIGHLIGHT_COLOR, cfg.PRIMARY_COLOR, cfg.SECONDARY_COLOR])
            
            particle = WaveParticle(x, y, amplitude, frequency, phase, color)
            self.wave_particles.append(particle)
    
    def start_animation(self):
        if not self.animation_started:
            self.animation_started = True
            self.animation_start_time = time.time()
    
    def change_pattern(self):
        """Cambiar al siguiente patrón y actualizar las cartas"""
        self.current_pattern_index = (self.current_pattern_index + 1) % len(self.patterns)
        current_pattern = self.patterns[self.current_pattern_index]
        
        # Actualizar los valores objetivo de las cartas existentes
        card_index = 0
        for row in range(len(current_pattern)):
            for col in range(len(current_pattern[row])):
                if card_index < len(self.cards):
                    self.cards[card_index].target_value = current_pattern[row][col]
                    self.cards[card_index].start_flip()
                    card_index += 1
        
        # Reiniciar el tiempo de último cambio
        self.last_pattern_change = time.time()
                
    def update(self):
        # Actualizar tiempo de ola
        self.wave_time += 0.05
        
        # Actualizar cartas
        for card in self.cards:
            card.update()
            
        # Actualizar partículas de ola
        for particle in self.wave_particles:
            particle.update(self.wave_time)
            
        # Iniciar animación de flip después de un momento
        if self.animation_started and time.time() > self.animation_start_time + 1:
            for card in self.cards:
                card.start_flip()
        
        # Cambiar patrones cada 1.5 segundos para mostrar B-I-N-G-O
        current_time = time.time()
        if current_time - self.last_pattern_change >= self.pattern_duration:
            # Cambiar al siguiente patrón
            self.current_pattern_index = (self.current_pattern_index + 1) % len(self.patterns)
            self.setup_cards()  # Reconfigurar cartas con el nuevo patrón
            self.last_pattern_change = current_time
            
            # Reiniciar animación para el nuevo patrón
            self.animation_started = True
            self.animation_start_time = current_time
    
    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.button_hover = self.button_rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                return "start_game"
        elif event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_RETURN:
                return "start_game"
            elif event.key == K_ESCAPE:
                return "exit_game"
        return None
    
    def draw(self):
        # Fondo con gradiente
        self.draw_gradient_background()
        
        # Partículas de ola
        for particle in self.wave_particles:
            particle.draw(self.screen)
        
        # Cartas
        for card in self.cards:
            card.draw(self.screen)
        
        # Título principal
        title = self.font_title.render("BINGACHO", True, cfg.HIGHLIGHT_COLOR)
        title_rect = title.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2 + 200))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_small.render("Juego de Bingo Digital - Creado por Jose Alejandro", True, cfg.WHITE)
        subtitle_rect = subtitle.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2 + 250))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Botón de iniciar
        self.draw_button()
        
        # Instrucciones
        instructions = self.font_small.render("Presiona ESPACIO, ENTER o haz clic en el botón para comenzar", True, cfg.WHITE)
        instructions_rect = instructions.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT - 80))
        self.screen.blit(instructions, instructions_rect)
        
        # Instrucción adicional para salir
        exit_instruction = self.font_small.render("Presiona ESC para salir", True, cfg.GRAY)
        exit_rect = exit_instruction.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT - 50))
        self.screen.blit(exit_instruction, exit_rect)
    
    def draw_gradient_background(self):
        # Crear un fondo con gradiente azul oscuro
        for y in range(cfg.HEIGHT):
            color_ratio = y / cfg.HEIGHT
            r = int(15 + (40 - 15) * color_ratio)
            g = int(23 + (50 - 23) * color_ratio)
            b = int(42 + (80 - 42) * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (cfg.WIDTH, y))
    
    def draw_button(self):
        # Color del botón
        if self.button_hover:
            color = cfg.BUTTON_HOVER_COLOR
            glow_radius = 10
        else:
            color = cfg.BUTTON_COLOR
            glow_radius = 5
        
        # Efecto de brillo
        for i in range(glow_radius):
            glow_color = (*cfg.HIGHLIGHT_COLOR, 255 - i * 20)
            glow_surface = pygame.Surface((self.button_rect.width + i * 2, self.button_rect.height + i * 2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, self.button_rect.width + i * 2, self.button_rect.height + i * 2), 2)
            self.screen.blit(glow_surface, (self.button_rect.x - i, self.button_rect.y - i))
        
        # Botón principal
        pygame.draw.rect(self.screen, color, self.button_rect)
        pygame.draw.rect(self.screen, cfg.HIGHLIGHT_COLOR, self.button_rect, 3)
        
        # Texto del botón
        button_text = self.font_button.render("INICIAR JUEGO", True, cfg.WHITE)
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, button_text_rect)

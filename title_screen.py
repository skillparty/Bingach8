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

class GlitchCard:
    def __init__(self, x, y, size, value, target_value, delay=0):
        self.x = x
        self.y = y
        self.size = size
        self.initial_value = value
        self.target_value = target_value
        self.current_value = value
        self.delay = delay
        self.start_time = 0
        self.cycle_time = 1.2  # Ciclo más lento para efectos dramáticos
        
        # Efectos glitch creativos
        self.glitch_intensity = random.uniform(0.3, 1.0)
        self.scan_line_offset = random.randint(0, 100)
        self.digital_noise = [random.randint(0, 255) for _ in range(10)]
        self.hologram_phase = random.uniform(0, math.pi * 2)
        self.matrix_trail = []
        self.energy_level = 0
        
        # Efectos Nothing Phone
        self.led_brightness = 0
        self.pulse_phase = random.uniform(0, math.pi * 2)
        self.circuit_pattern = self.generate_circuit_pattern()
        
    def generate_circuit_pattern(self):
        """Genera un patrón de circuito único para cada carta"""
        pattern = []
        for i in range(5):
            pattern.append({
                'start': (random.randint(0, self.size), random.randint(0, self.size)),
                'end': (random.randint(0, self.size), random.randint(0, self.size)),
                'active': False
            })
        return pattern
        
    def start_animation(self):
        """Inicia la animación glitch"""
        if self.start_time == 0:
            self.start_time = time.time()
            
    def update(self):
        """Actualiza todos los efectos glitch y Nothing Phone"""
        if self.start_time > 0:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            
            if elapsed_time >= self.delay:
                # Ciclo principal de animación
                cycle_progress = (elapsed_time - self.delay) % self.cycle_time
                phase = cycle_progress / self.cycle_time
                
                # Determinar estado actual con transiciones dramáticas
                if phase < 0.3:
                    # Fase de caos digital
                    self.current_value = random.choice([0, 1, self.initial_value])
                    self.energy_level = random.uniform(0.7, 1.0)
                elif phase < 0.4:
                    # Fase de transición glitch
                    self.current_value = random.choice([0, 1])
                    self.energy_level = 1.0
                else:
                    # Fase de revelación
                    self.current_value = self.target_value
                    self.energy_level = 0.8 if self.target_value == 1 else 0.2
                
                # Actualizar efectos
                self.update_glitch_effects(current_time)
                self.update_nothing_effects(current_time)
                
    def update_glitch_effects(self, current_time):
        """Actualiza efectos de glitch digital"""
        # Actualizar ruido digital
        if random.random() > 0.9:
            self.digital_noise = [random.randint(0, 255) for _ in range(10)]
        
        # Actualizar líneas de escaneo
        self.scan_line_offset = (self.scan_line_offset + 2) % (self.size * 2)
        
        # Actualizar fase de holograma
        self.hologram_phase += 0.1
        
    def update_nothing_effects(self, current_time):
        """Actualiza efectos estilo Nothing Phone"""
        # Brillo LED pulsante
        self.led_brightness = 0.5 + 0.5 * math.sin(current_time * 3 + self.pulse_phase)
        
        # Activar circuitos aleatoriamente
        for circuit in self.circuit_pattern:
            if random.random() > 0.95:
                circuit['active'] = not circuit['active']
                
    def draw(self, screen):
        """Dibuja la carta con efectos glitch y Nothing Phone espectaculares"""
        current_time = pygame.time.get_ticks()
        display_value = self.current_value
        
        # Crear superficie para efectos complejos
        card_surface = pygame.Surface((self.size + 8, self.size + 8), pygame.SRCALPHA)
        
        if display_value == 1:
            # ===== EFECTO NOTHING PHONE PARA VALOR 1 =====
            self.draw_nothing_phone_effect(card_surface, current_time)
        else:
            # ===== EFECTO GLITCH PARA VALOR 0 =====
            self.draw_glitch_effect(card_surface, current_time)
        
        # Dibujar en pantalla
        screen.blit(card_surface, (self.x - 4, self.y - 4))
        
        # Efectos adicionales en pantalla
        self.draw_screen_effects(screen, current_time)
    
    def draw_nothing_phone_effect(self, surface, current_time):
        """Efecto inspirado en Nothing Phone para las letras BINGO"""
        # Fondo transparente con circuitos LED
        surface.fill((0, 0, 0, 0))
        
        # Circuitos LED brillantes
        for circuit in self.circuit_pattern:
            if circuit['active']:
                # Línea LED brillante
                led_color = (255, 255, 255, int(255 * self.led_brightness))
                start_pos = (circuit['start'][0] + 4, circuit['start'][1] + 4)
                end_pos = (circuit['end'][0] + 4, circuit['end'][1] + 4)
                
                # Dibujar línea con grosor variable
                thickness = int(2 + self.led_brightness * 2)
                pygame.draw.line(surface, cfg.WHITE, start_pos, end_pos, thickness)
                
                # Efecto de brillo
                glow_surface = pygame.Surface((self.size + 8, self.size + 8), pygame.SRCALPHA)
                pygame.draw.line(glow_surface, (*cfg.HIGHLIGHT_COLOR[:3], int(100 * self.led_brightness)), 
                               start_pos, end_pos, thickness + 2)
                surface.blit(glow_surface, (0, 0))
        
        # Marco LED perimetral
        led_alpha = int(200 * self.led_brightness)
        if led_alpha > 0:
            # Esquinas LED
            corner_size = 8
            corners = [
                (4, 4), (self.size - 4, 4),
                (4, self.size - 4), (self.size - 4, self.size - 4)
            ]
            
            for corner in corners:
                pygame.draw.circle(surface, (*cfg.HIGHLIGHT_COLOR[:3], led_alpha), 
                                 (corner[0] + 4, corner[1] + 4), corner_size)
        
        # Texto holográfico
        font_size = int(self.size * 0.6)
        font = pygame.font.Font(None, font_size)
        
        # Efecto holográfico con múltiples capas
        for i in range(3):
            alpha = int(255 - i * 60)
            holo_color = (*cfg.HIGHLIGHT_COLOR[:3], alpha)
            text = font.render("█", True, cfg.WHITE)  # Bloque sólido
            text_rect = text.get_rect(center=(self.size // 2 + 4 + i, self.size // 2 + 4 + i))
            surface.blit(text, text_rect)
    
    def draw_glitch_effect(self, surface, current_time):
        """Efecto glitch digital para el fondo"""
        # Fondo con ruido digital
        for i in range(0, self.size + 8, 2):
            for j in range(0, self.size + 8, 2):
                if random.random() > 0.85:
                    noise_color = random.choice([(20, 20, 30), (30, 30, 40), (10, 10, 20)])
                    pygame.draw.rect(surface, noise_color, (i, j, 2, 2))
        
        # Líneas de escaneo
        scan_y = (current_time // 50) % (self.size + 8)
        for i in range(3):
            alpha = 100 - i * 30
            if alpha > 0:
                scan_color = (0, 255, 100, alpha)
                scan_surface = pygame.Surface((self.size + 8, 2), pygame.SRCALPHA)
                scan_surface.fill(scan_color)
                surface.blit(scan_surface, (0, scan_y + i))
        
        # Fragmentos glitch
        if random.random() > 0.9:
            fragment_width = random.randint(5, 15)
            fragment_height = random.randint(2, 5)
            fragment_x = random.randint(0, self.size - fragment_width)
            fragment_y = random.randint(0, self.size - fragment_height)
            
            # Desplazar fragmento
            offset_x = random.randint(-3, 3)
            glitch_color = (random.randint(0, 100), random.randint(100, 255), random.randint(0, 100))
            pygame.draw.rect(surface, glitch_color, 
                           (fragment_x + offset_x + 4, fragment_y + 4, fragment_width, fragment_height))
        
        # Punto central sutil
        center_color = (100, 100, 120, 150)
        pygame.draw.circle(surface, cfg.GRAY, (self.size // 2 + 4, self.size // 2 + 4), 2)
    
    def draw_screen_effects(self, screen, current_time):
        """Efectos adicionales que se dibujan directamente en pantalla"""
        if self.current_value == 1 and self.energy_level > 0.7:
            # Partículas de energía
            if random.random() > 0.92:
                particle_x = self.x + random.randint(-10, self.size + 10)
                particle_y = self.y + random.randint(-10, self.size + 10)
                particle_size = random.randint(1, 4)
                particle_color = random.choice([cfg.WHITE, cfg.HIGHLIGHT_COLOR, (0, 255, 200)])
                pygame.draw.circle(screen, particle_color, (particle_x, particle_y), particle_size)
            
            # Rayos de conexión ocasionales
            if random.random() > 0.98:
                ray_end_x = self.x + random.randint(-50, 50)
                ray_end_y = self.y + random.randint(-50, 50)
                pygame.draw.line(screen, (*cfg.HIGHLIGHT_COLOR[:3], 100), 
                               (self.x + self.size // 2, self.y + self.size // 2),
                               (ray_end_x, ray_end_y), 1)

class BouncingWaveParticle:
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
        self.size = random.randint(30, 45)  # Tamaño grande como antes
        self.number = random.randint(1, 90)  # Número aleatorio del 1 al 90
        
        # Añadir velocidades para el rebote
        self.vel_x = random.uniform(-1.5, 1.5)
        self.vel_y = random.uniform(-1.5, 1.5)
        
        # Colores que cambian al rebotar
        self.colors = [
            cfg.HIGHLIGHT_COLOR,  # Ámbar
            cfg.WHITE,            # Blanco
            (0, 255, 200),        # Cian
            (255, 100, 255),      # Magenta
            (100, 255, 100),      # Verde claro
            (255, 200, 100)       # Naranja
        ]
        self.color_index = random.randint(0, len(self.colors) - 1)
        
    def update(self, wave_time):
        # Movimiento ondulatorio estilo Hokusai (como antes)
        wave_x = self.base_x + math.sin(wave_time * self.frequency + self.phase) * self.amplitude * 0.5
        wave_y = self.base_y + math.cos(wave_time * self.frequency * 0.7 + self.phase) * self.amplitude * 0.3
        
        # Añadir movimiento de rebote
        self.x = wave_x + self.vel_x * wave_time * 10
        self.y = wave_y + self.vel_y * wave_time * 10
        
        # Rebote en los bordes con cambio de color
        bounced = False
        
        # Rebote horizontal
        if self.x <= self.size or self.x >= cfg.WIDTH - self.size:
            self.vel_x = -self.vel_x
            bounced = True
            
        # Rebote vertical
        if self.y <= self.size or self.y >= cfg.HEIGHT - self.size:
            self.vel_y = -self.vel_y
            bounced = True
            
        # Cambiar color al rebotar
        if bounced:
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.number = random.randint(1, 90)
            
        # Mantener dentro de los límites
        self.x = max(self.size, min(cfg.WIDTH - self.size, self.x))
        self.y = max(self.size, min(cfg.HEIGHT - self.size, self.y))
        
        # Efecto de desvanecimiento (como antes)
        self.life -= 0.002
        if self.life <= 0:
            self.life = 1.0
            self.number = random.randint(1, 90)  # Cambiar número cuando se reinicia la partícula
            
    def draw(self, screen):
        alpha = int(255 * self.life)
        current_color = self.colors[self.color_index]
        color_with_alpha = (*current_color, alpha)
        
        # Crear superficie con alpha para el número
        font = pygame.font.Font(None, self.size)
        text_surface = font.render(str(self.number), True, color_with_alpha)
        
        # Crear superficie con alpha
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Dibujar círculo de fondo semi-transparente con color dinámico
        bg_color = (*current_color, alpha // 3)  # Fondo con color dinámico
        pygame.draw.circle(particle_surface, bg_color, (self.size, self.size), self.size // 2)
        
        # Centrar el texto en la superficie
        text_rect = text_surface.get_rect(center=(self.size, self.size))
        particle_surface.blit(text_surface, text_rect)
        
        screen.blit(particle_surface, (self.x - self.size, self.y - self.size))

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 120)  # Aumentado tamaño de la fuente del título
        self.font_button = pygame.font.Font(None, 72)   # Aumentado tamaño de la fuente del botón
        self.font_small = pygame.font.Font(None, 48)    # Aumentado tamaño de la fuente pequeña
        
        # Configurar patrones para la animación
        self.setup_patterns()
        
        # Control del bucle de patrones
        self.current_pattern_index = 0
        self.pattern_change_interval = 3.0  # Cambiar cada 3 segundos
        self.last_pattern_change = time.time()
        
        # Configurar las cartas
        self.setup_cards()
        
        # Configurar partículas de ola
        self.setup_bouncing_wave_particles()
        
        # Estado de animación
        self.animation_started = False
        self.animation_start_time = 0
        self.wave_time = 0
        self.pattern_duration = 1.5  # Duración de cada letra en segundos (1.5s es óptimo)
        self.flip_in_progress = False
        self.current_letter = "B"  # Para mostrar la letra actual
        
        # Botón de iniciar
        button_width = 400
        button_height = 80
        self.button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.button_rect.center = (cfg.WIDTH // 2, cfg.HEIGHT // 2 + 580)  # Bajado de 500 a 580
        self.button_hover = False
        
    def setup_patterns(self):
        """Configura un patrón espectacular para la palabra BINGO completa"""
        
        # Patrón ESPECTACULAR para "BINGO" - 15 filas x 45 columnas para máxima definición
        self.bingo_pattern = [
            # B        I        N        G        O
            [1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
        ]

        # La lista de patrones ahora solo contiene el patrón BINGO completo
        self.patterns = [self.bingo_pattern]

    def setup_cards(self):
        self.cards = []
        # Configuración ESPECTACULAR para matriz 15x45 (matriz gigante y detallada)
        rows, cols = 15, 45
        card_size = 25  # Tamaño optimizado para la matriz gigante
        spacing = 3     # Espaciado mínimo para máxima densidad visual
        
        # Calcular posición inicial para centrar la matriz
        total_width = cols * (card_size + spacing) - spacing
        total_height = rows * (card_size + spacing) - spacing
        start_x = (cfg.WIDTH - total_width) // 2
        start_y = (cfg.HEIGHT - total_height) // 2 - 200  # Subir más la matriz de cartas
        
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
                delay = distance * 0.02  # Retraso reducido para animación más rápida
                
                card = GlitchCard(x, y, card_size, initial_value, target_value, delay)
                self.cards.append(card)
    
    def setup_bouncing_wave_particles(self):
        self.bouncing_particles = []
        
        # Crear partículas ondulatorias con rebote (como antes pero con rebotes)
        for i in range(200):  # Cantidad original para efecto espectacular
            x = random.randint(0, cfg.WIDTH)
            y = random.randint(0, cfg.HEIGHT)
            amplitude = random.randint(20, 80)
            frequency = random.uniform(0.5, 2.0)
            phase = random.uniform(0, 2 * math.pi)
            color = random.choice([cfg.HIGHLIGHT_COLOR, cfg.PRIMARY_COLOR, cfg.SECONDARY_COLOR])
            
            particle = BouncingWaveParticle(x, y, amplitude, frequency, phase, color)
            self.bouncing_particles.append(particle)
    
    def start_animation(self):
        if not self.animation_started:
            self.animation_started = True
            self.animation_start_time = time.time()
            self.is_flipping = False
        
    def start_flipping_cards(self):
        # Iniciar la animación de flip para todas las cartas
        for card in self.cards:
            card.start_animation()
    
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
            
        # Actualizar partículas ondulatorias con rebote
        for particle in self.bouncing_particles:
            particle.update(self.wave_time)
            
        # Iniciar la animación de flip para mostrar la palabra BINGO completa
        # Solo lo hacemos una vez al inicio y luego se queda estático
        current_time = time.time()
        if not getattr(self, 'is_flipping', False) and current_time - self.animation_start_time > 1.0:
            # Iniciar la animación de revelar BINGO completo
            self.start_flipping_cards()
            self.is_flipping = True
            print("Mostrando palabra BINGO completa estática")

        # Actualizar animación del botón
        self.button_anim_time = getattr(self, 'button_anim_time', 0) + 0.05
        if self.button_hover:
            self.button_scale = 1.0 + 0.1 * abs(math.sin(self.button_anim_time * 5))
    
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
        # Fondo con gradiente espectacular
        self.draw_gradient_background()
        
        # Partículas ondulatorias con rebote
        for particle in self.bouncing_particles:
            particle.draw(self.screen)
        
        # Efecto de resplandor detrás de la matriz
        matrix_center_x = cfg.WIDTH // 2
        matrix_center_y = cfg.HEIGHT // 2 - 150
        
        # Resplandor circular detrás de la matriz
        for i in range(8, 0, -1):
            alpha = int(30 - i * 3)
            if alpha > 0:
                glow_surface = pygame.Surface((cfg.WIDTH, cfg.HEIGHT), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*cfg.HIGHLIGHT_COLOR[:3], alpha), 
                                 (matrix_center_x, matrix_center_y), i * 50)
                self.screen.blit(glow_surface, (0, 0))
        
        # Cartas con la matriz BINGO
        for card in self.cards:
            card.draw(self.screen)
        
        # Título principal con efectos
        current_time = pygame.time.get_ticks()
        title_pulse = 0.9 + 0.1 * math.sin(current_time / 1000)
        
        # Sombra del título
        title_shadow = self.font_title.render("BINGACHO", True, (0, 0, 0))
        title_shadow_rect = title_shadow.get_rect(center=(cfg.WIDTH // 2 + 4, cfg.HEIGHT // 2 + 404))
        self.screen.blit(title_shadow, title_shadow_rect)
        
        # Título principal con brillo
        title_color = (int(cfg.HIGHLIGHT_COLOR[0] * title_pulse), 
                      int(cfg.HIGHLIGHT_COLOR[1] * title_pulse), 
                      int(cfg.HIGHLIGHT_COLOR[2] * title_pulse))
        title = self.font_title.render("BINGACHO", True, title_color)
        title_rect = title.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2 + 400))
        self.screen.blit(title, title_rect)
        
        # Subtítulo elegante
        subtitle = self.font_small.render("Juego de Bingo Digital - Creado por Jose Alejandro", True, cfg.WHITE)
        subtitle_rect = subtitle.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2 + 460))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Sin texto descriptivo - la matriz habla por sí misma
        
        # Botón de iniciar
        self.draw_button()
        
        # Instrucciones - ajustadas para el botón más abajo
        instructions = self.font_small.render("Presiona ESPACIO, ENTER o haz clic en el botón para comenzar", True, cfg.WHITE)
        instructions_rect = instructions.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT - 140))  # Subidas para dar espacio al botón
        self.screen.blit(instructions, instructions_rect)
        
        # Instrucción adicional para salir
        exit_instruction = self.font_small.render("Presiona ESC para salir", True, cfg.GRAY)
        exit_rect = exit_instruction.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT - 100))  # Subida también
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

"""
Renderizador de cartillas de bingo para pygame
"""

import pygame
import config as cfg
import math

class BingoCardRenderer:
    """Renderiza una cartilla de bingo en la pantalla"""
    
    def __init__(self, screen, card, position=(50, 50), cell_size=60):
        """
        Inicializa el renderizador
        
        Args:
            screen: Superficie de pygame
            card: Instancia de BingoCard
            position: Tupla (x, y) con la posición de la cartilla
            cell_size: Tamaño de cada celda
        """
        self.screen = screen
        self.card = card
        self.position = position
        self.cell_size = cell_size
        self.cell_spacing = 3
        self.corner_radius = 8
        
        # Fuentes
        self.number_font = cfg.get_font(int(cell_size * 0.4), bold=True)
        self.title_font = cfg.get_font(int(cell_size * 0.5), bold=True)
        
        # Calcular dimensiones
        self.card_width = 9 * (cell_size + self.cell_spacing) + 20
        self.card_height = 3 * (cell_size + self.cell_spacing) + 80
    
    def draw(self, show_marked=True, highlight_current=True):
        """
        Dibuja la cartilla en la pantalla
        
        Args:
            show_marked: Si True, muestra los números marcados
            highlight_current: Si True, resalta el número actual
        """
        x, y = self.position
        
        # Contenedor de la cartilla
        container_rect = pygame.Rect(
            x, y,
            self.card_width,
            self.card_height
        )
        
        # Sombra
        shadow_rect = container_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect, border_radius=12)
        
        # Fondo
        pygame.draw.rect(self.screen, cfg.FRAME_COLOR, container_rect, border_radius=12)
        pygame.draw.rect(self.screen, cfg.BORDER_COLOR, container_rect, 3, border_radius=12)
        
        # Título
        title_y = y + 15
        title_text = self.title_font.render("TU CARTILLA", True, cfg.PRIMARY_COLOR)
        title_rect = title_text.get_rect(center=(x + self.card_width // 2, title_y))
        self.screen.blit(title_text, title_rect)
        
        # Dibujar las celdas
        start_x = x + 10
        start_y = y + 50
        
        for row_idx, row in enumerate(self.card.numbers):
            for col_idx, number in enumerate(row):
                cell_x = start_x + col_idx * (self.cell_size + self.cell_spacing)
                cell_y = start_y + row_idx * (self.cell_size + self.cell_spacing)
                
                self.draw_cell(
                    cell_x, cell_y,
                    number,
                    show_marked=show_marked,
                    highlight_current=highlight_current
                )
    
    def draw_cell(self, x, y, number, show_marked=True, highlight_current=True):
        """
        Dibuja una celda individual
        
        Args:
            x: Posición X
            y: Posición Y
            number: Número a dibujar (None si está vacío)
            show_marked: Si True, muestra si está marcado
            highlight_current: Si True, resalta números especiales
        """
        cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        
        if number is None:
            # Celda vacía
            pygame.draw.rect(self.screen, cfg.DARK_GRAY, cell_rect, border_radius=self.corner_radius)
            pygame.draw.rect(self.screen, cfg.BORDER_COLOR, cell_rect, 1, border_radius=self.corner_radius)
            return
        
        # Verificar si está marcado
        is_marked = show_marked and self.card.is_marked(number)
        
        # Determinar color según el rango
        if number <= 30:
            range_color = cfg.RANGE_1_30
        elif number <= 60:
            range_color = cfg.RANGE_31_60
        else:
            range_color = cfg.RANGE_61_90
        
        if is_marked:
            # Número marcado
            bg_color = range_color
            text_color = cfg.BLACK if range_color == cfg.RANGE_31_60 else cfg.TEXT_COLOR
            border_color = cfg.HIGHLIGHT_COLOR
            border_width = 2
            
            # Efecto de brillo
            if highlight_current:
                current_time = pygame.time.get_ticks()
                pulse = 0.8 + 0.2 * math.sin(current_time / 400)
                glow_rect = cell_rect.inflate(4, 4)
                glow_alpha = int(80 * pulse)
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*range_color[:3], glow_alpha), 
                               glow_surf.get_rect(), border_radius=self.corner_radius + 2)
                self.screen.blit(glow_surf, glow_rect)
        else:
            # Número no marcado
            bg_color = cfg.DARK_GRAY
            text_color = cfg.GRAY
            border_color = cfg.BORDER_COLOR
            border_width = 1
        
        # Dibujar celda
        pygame.draw.rect(self.screen, bg_color, cell_rect, border_radius=self.corner_radius)
        pygame.draw.rect(self.screen, border_color, cell_rect, border_width, border_radius=self.corner_radius)
        
        # Dibujar número
        number_text = self.number_font.render(str(number), True, text_color)
        number_rect = number_text.get_rect(center=cell_rect.center)
        self.screen.blit(number_text, number_rect)
    
    def get_rect(self):
        """Retorna el rectángulo de la cartilla"""
        return pygame.Rect(self.position[0], self.position[1], self.card_width, self.card_height)
    
    def draw_stats(self, position=None):
        """
        Dibuja estadísticas de la cartilla
        
        Args:
            position: Posición donde dibujar (opcional, usa posición debajo de la cartilla)
        """
        if position is None:
            position = (self.position[0], self.position[1] + self.card_height + 20)
        
        x, y = position
        
        # Obtener estadísticas
        total_numbers = sum(1 for row in self.card.numbers for num in row if num is not None)
        marked_count = len(self.card.marked)
        has_line = self.card.check_line()
        has_bingo = self.card.check_bingo()
        
        # Fuente para stats
        stats_font = cfg.get_font(24)
        
        # Números marcados
        marked_text = f"Marcados: {marked_count}/{total_numbers}"
        marked_surface = stats_font.render(marked_text, True, cfg.TEXT_COLOR)
        self.screen.blit(marked_surface, (x, y))
        
        # Línea
        if has_line:
            line_text = "¡LÍNEA!"
            line_surface = stats_font.render(line_text, True, cfg.SUCCESS)
            self.screen.blit(line_surface, (x + 200, y))
        
        # Bingo
        if has_bingo:
            bingo_text = "¡¡¡BINGO!!!"
            bingo_surface = self.title_font.render(bingo_text, True, cfg.HIGHLIGHT_COLOR)
            bingo_rect = bingo_surface.get_rect(center=(x + self.card_width // 2, y + 40))
            
            # Efecto pulsante
            current_time = pygame.time.get_ticks()
            pulse = 0.9 + 0.1 * math.sin(current_time / 200)
            scaled_width = int(bingo_surface.get_width() * pulse)
            scaled_height = int(bingo_surface.get_height() * pulse)
            scaled_surface = pygame.transform.scale(bingo_surface, (scaled_width, scaled_height))
            scaled_rect = scaled_surface.get_rect(center=bingo_rect.center)
            
            self.screen.blit(scaled_surface, scaled_rect)


class MultiCardRenderer:
    """Renderiza múltiples cartillas de bingo en una grilla"""
    
    def __init__(self, screen, cards, start_position=(50, 300), cards_per_row=2):
        """
        Inicializa el renderizador de múltiples cartillas
        
        Args:
            screen: Superficie de pygame
            cards: Lista de BingoCard
            start_position: Posición inicial
            cards_per_row: Cartillas por fila
        """
        self.screen = screen
        self.cards = cards
        self.start_position = start_position
        self.cards_per_row = cards_per_row
        
        # Crear renderizadores individuales
        self.renderers = []
        cell_size = 50  # Más pequeño para múltiples cartillas
        
        for i, card in enumerate(cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = start_position[0] + col * 600
            y = start_position[1] + row * 280
            
            renderer = BingoCardRenderer(screen, card, (x, y), cell_size)
            self.renderers.append(renderer)
    
    def draw(self, show_marked=True, highlight_current=True):
        """Dibuja todas las cartillas"""
        for renderer in self.renderers:
            renderer.draw(show_marked, highlight_current)
    
    def update_cards(self, cards):
        """Actualiza las cartillas"""
        self.cards = cards
        self.renderers = []
        cell_size = 50
        
        for i, card in enumerate(cards):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            x = self.start_position[0] + col * 600
            y = self.start_position[1] + row * 280
            
            renderer = BingoCardRenderer(self.screen, card, (x, y), cell_size)
            self.renderers.append(renderer)

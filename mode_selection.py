"""
Pantalla de selección de modo de juego
Permite elegir entre: Modo Local, Servidor (Host), Cliente (Jugador)
"""

import pygame
import config as cfg

class ModeSelection:
    """Pantalla para seleccionar el modo de juego"""
    
    def __init__(self, screen):
        """
        Inicializa la pantalla de selección
        
        Args:
            screen: Superficie de pygame para renderizar
        """
        self.screen = screen
        self.selected_mode = None  # None, "local", "server", "client"
        self.game_mode = "normal"  # "normal" (90 números) o "alt" (75 números)
        self.nickname = ""
        self.server_ip = ""
        self.is_entering_nickname = False
        self.is_entering_server_ip = False
        self.error_message = ""
        
        # Configurar fuentes
        self.title_font = cfg.get_font(80, bold=True)
        self.button_font = cfg.get_font(36, bold=True)
        self.input_font = cfg.get_font(32)
        self.subtitle_font = cfg.get_font(28)
        
        # Posiciones de botones
        self.setup_buttons()
    
    def setup_buttons(self):
        """Configura los rectángulos de los botones"""
        button_width = 500
        button_height = 80
        center_x = cfg.WIDTH // 2
        start_y = cfg.HEIGHT // 2 - 100
        spacing = 120
        
        self.local_button = pygame.Rect(
            center_x - button_width // 2,
            start_y,
            button_width,
            button_height
        )
        
        self.server_button = pygame.Rect(
            center_x - button_width // 2,
            start_y + spacing,
            button_width,
            button_height
        )
        
        self.client_button = pygame.Rect(
            center_x - button_width // 2,
            start_y + spacing * 2,
            button_width,
            button_height
        )
        
        # Botones para la pantalla de configuración
        self.back_button = pygame.Rect(50, cfg.HEIGHT - 100, 150, 60)
        self.start_button = pygame.Rect(cfg.WIDTH - 200, cfg.HEIGHT - 100, 150, 60)
        
        # Campo de entrada de texto
        input_width = 600
        input_height = 60
        self.nickname_input = pygame.Rect(
            center_x - input_width // 2,
            cfg.HEIGHT // 2 - 120,
            input_width,
            input_height
        )
        
        self.server_ip_input = pygame.Rect(
            center_x - input_width // 2,
            cfg.HEIGHT // 2 + 80,
            input_width,
            input_height
        )
        
        # Botones de modo de juego (Normal/Alterno)
        mode_button_width = 280
        mode_button_height = 60
        mode_spacing = 40
        mode_start_x = center_x - mode_button_width - mode_spacing // 2
        
        self.normal_mode_button = pygame.Rect(
            mode_start_x,
            cfg.HEIGHT // 2 + 20,
            mode_button_width,
            mode_button_height
        )
        
        self.alt_mode_button = pygame.Rect(
            mode_start_x + mode_button_width + mode_spacing,
            cfg.HEIGHT // 2 + 20,
            mode_button_width,
            mode_button_height
        )
    
    def draw_main_menu(self):
        """Dibuja el menú principal de selección de modo"""
        # Fondo
        self.screen.fill(cfg.BACKGROUND_COLOR)
        
        # Título
        title_text = self.title_font.render("BINGACHO", True, cfg.PRIMARY_COLOR)
        title_rect = title_text.get_rect(center=(cfg.WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.subtitle_font.render("Selecciona el modo de juego", True, cfg.TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(cfg.WIDTH // 2, 250))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Botones
        mouse_pos = pygame.mouse.get_pos()
        
        # Botón Modo Local
        self.draw_button(
            self.local_button,
            "MODO LOCAL",
            "Jugar solo en esta computadora",
            mouse_pos
        )
        
        # Botón Servidor
        self.draw_button(
            self.server_button,
            "CREAR PARTIDA (SERVIDOR)",
            "Ser el host y controlar el sorteo",
            mouse_pos
        )
        
        # Botón Cliente
        self.draw_button(
            self.client_button,
            "UNIRSE A PARTIDA",
            "Conectarse a una partida existente",
            mouse_pos
        )
    
    def draw_button(self, rect, text, subtitle, mouse_pos):
        """
        Dibuja un botón con efecto hover
        
        Args:
            rect: Rectángulo del botón
            text: Texto principal
            subtitle: Texto secundario
            mouse_pos: Posición del mouse
        """
        is_hover = rect.collidepoint(mouse_pos)
        
        # Color del botón
        if is_hover:
            color = cfg.BUTTON_HOVER_COLOR
            border_color = cfg.HIGHLIGHT_COLOR
            border_width = 4
        else:
            color = cfg.BUTTON_COLOR
            border_color = cfg.BORDER_COLOR
            border_width = 2
        
        # Dibujar botón
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=15)
        
        # Texto principal
        text_surface = self.button_font.render(text, True, cfg.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery - 10))
        self.screen.blit(text_surface, text_rect)
        
        # Subtítulo
        subtitle_surface = self.subtitle_font.render(subtitle, True, cfg.SUBTITLE_COLOR)
        subtitle_rect = subtitle_surface.get_rect(center=(rect.centerx, rect.centery + 25))
        self.screen.blit(subtitle_surface, subtitle_rect)
    
    def draw_config_screen(self):
        """Dibuja la pantalla de configuración según el modo seleccionado"""
        # Fondo
        self.screen.fill(cfg.BACKGROUND_COLOR)
        
        # Título según el modo
        if self.selected_mode == "server":
            title = "CONFIGURAR SERVIDOR"
            subtitle = "Ingresa tu nickname"
        elif self.selected_mode == "local":
            title = "MODO LOCAL"
            subtitle = "Configura tu partida"
        else:  # client
            title = "UNIRSE A PARTIDA"
            subtitle = "Ingresa tu nickname y la IP del servidor"
        
        title_text = self.title_font.render(title, True, cfg.PRIMARY_COLOR)
        title_rect = title_text.get_rect(center=(cfg.WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.subtitle_font.render(subtitle, True, cfg.TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(cfg.WIDTH // 2, 250))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Campo de nickname
        if self.selected_mode != "local":
            nickname_label = self.subtitle_font.render("Nickname:", True, cfg.TEXT_COLOR)
            nickname_label_rect = nickname_label.get_rect(
                bottomleft=(self.nickname_input.left, self.nickname_input.top - 10)
            )
            self.screen.blit(nickname_label, nickname_label_rect)
            
            # Dibujar campo de entrada de nickname
            pygame.draw.rect(
                self.screen,
                cfg.DARK_GRAY,
                self.nickname_input,
                border_radius=10
            )
            pygame.draw.rect(
                self.screen,
                cfg.PRIMARY_COLOR if self.is_entering_nickname else cfg.BORDER_COLOR,
                self.nickname_input,
                3,
                border_radius=10
            )
            
            # Texto del nickname
            nickname_display = self.nickname + ("|" if self.is_entering_nickname else "")
            nickname_text = self.input_font.render(nickname_display, True, cfg.TEXT_COLOR)
            nickname_text_rect = nickname_text.get_rect(
                midleft=(self.nickname_input.left + 20, self.nickname_input.centery)
            )
            self.screen.blit(nickname_text, nickname_text_rect)
        
        # Obtener posición del mouse para hover effects
        mouse_pos = pygame.mouse.get_pos()
        
        # Si es servidor o local, mostrar selección de modo de juego
        if self.selected_mode in ["server", "local"]:
            mode_label = self.subtitle_font.render("Modo de Juego:", True, cfg.TEXT_COLOR)
            mode_label_rect = mode_label.get_rect(
                bottomleft=(self.normal_mode_button.left, self.normal_mode_button.top - 10)
            )
            self.screen.blit(mode_label, mode_label_rect)
            
            # Botón Modo Normal
            is_normal_selected = self.game_mode == "normal"
            normal_color = cfg.SECONDARY_COLOR if is_normal_selected else cfg.DARK_GRAY
            normal_hover = self.normal_mode_button.collidepoint(mouse_pos)
            
            pygame.draw.rect(
                self.screen,
                cfg.BUTTON_HOVER_COLOR if (normal_hover and not is_normal_selected) else normal_color,
                self.normal_mode_button,
                border_radius=10
            )
            pygame.draw.rect(
                self.screen,
                cfg.HIGHLIGHT_COLOR if is_normal_selected else cfg.BORDER_COLOR,
                self.normal_mode_button,
                4 if is_normal_selected else 2,
                border_radius=10
            )
            
            normal_title = self.subtitle_font.render("NORMAL", True, cfg.TEXT_COLOR)
            normal_desc = self.input_font.render("90 números (9x10)", True, cfg.LIGHT_GRAY)
            normal_title_rect = normal_title.get_rect(
                center=(self.normal_mode_button.centerx, self.normal_mode_button.centery - 12)
            )
            normal_desc_rect = normal_desc.get_rect(
                center=(self.normal_mode_button.centerx, self.normal_mode_button.centery + 12)
            )
            self.screen.blit(normal_title, normal_title_rect)
            self.screen.blit(normal_desc, normal_desc_rect)
            
            # Botón Modo Alterno
            is_alt_selected = self.game_mode == "alt"
            alt_color = cfg.SECONDARY_COLOR if is_alt_selected else cfg.DARK_GRAY
            alt_hover = self.alt_mode_button.collidepoint(mouse_pos)
            
            pygame.draw.rect(
                self.screen,
                cfg.BUTTON_HOVER_COLOR if (alt_hover and not is_alt_selected) else alt_color,
                self.alt_mode_button,
                border_radius=10
            )
            pygame.draw.rect(
                self.screen,
                cfg.HIGHLIGHT_COLOR if is_alt_selected else cfg.BORDER_COLOR,
                self.alt_mode_button,
                4 if is_alt_selected else 2,
                border_radius=10
            )
            
            alt_title = self.subtitle_font.render("ALTERNO", True, cfg.TEXT_COLOR)
            alt_desc = self.input_font.render("75 números (7x11)", True, cfg.LIGHT_GRAY)
            alt_title_rect = alt_title.get_rect(
                center=(self.alt_mode_button.centerx, self.alt_mode_button.centery - 12)
            )
            alt_desc_rect = alt_desc.get_rect(
                center=(self.alt_mode_button.centerx, self.alt_mode_button.centery + 12)
            )
            self.screen.blit(alt_title, alt_title_rect)
            self.screen.blit(alt_desc, alt_desc_rect)
        
        # Si es cliente, mostrar campo de IP del servidor
        if self.selected_mode == "client":
            server_label = self.subtitle_font.render("IP del Servidor:", True, cfg.TEXT_COLOR)
            server_label_rect = server_label.get_rect(
                bottomleft=(self.server_ip_input.left, self.server_ip_input.top - 10)
            )
            self.screen.blit(server_label, server_label_rect)
            
            # Dibujar campo de entrada de IP
            pygame.draw.rect(
                self.screen,
                cfg.DARK_GRAY,
                self.server_ip_input,
                border_radius=10
            )
            pygame.draw.rect(
                self.screen,
                cfg.PRIMARY_COLOR if self.is_entering_server_ip else cfg.BORDER_COLOR,
                self.server_ip_input,
                3,
                border_radius=10
            )
            
            # Texto de la IP
            ip_display = self.server_ip + ("|" if self.is_entering_server_ip else "")
            ip_text = self.input_font.render(ip_display, True, cfg.TEXT_COLOR)
            ip_text_rect = ip_text.get_rect(
                midleft=(self.server_ip_input.left + 20, self.server_ip_input.centery)
            )
            self.screen.blit(ip_text, ip_text_rect)
        
        # Mensaje de error si existe
        if self.error_message:
            error_text = self.subtitle_font.render(self.error_message, True, cfg.RED)
            error_rect = error_text.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT - 200))
            self.screen.blit(error_text, error_rect)
        
        # Botones
        mouse_pos = pygame.mouse.get_pos()
        
        # Botón Volver
        back_hover = self.back_button.collidepoint(mouse_pos)
        pygame.draw.rect(
            self.screen,
            cfg.BUTTON_HOVER_COLOR if back_hover else cfg.BUTTON_COLOR,
            self.back_button,
            border_radius=10
        )
        pygame.draw.rect(
            self.screen,
            cfg.HIGHLIGHT_COLOR if back_hover else cfg.BORDER_COLOR,
            self.back_button,
            3 if back_hover else 2,
            border_radius=10
        )
        back_text = self.button_font.render("VOLVER", True, cfg.TEXT_COLOR)
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_rect)
        
        # Botón Iniciar
        start_hover = self.start_button.collidepoint(mouse_pos)
        can_start = self.can_start()
        start_color = cfg.SECONDARY_COLOR if can_start else cfg.DARK_GRAY
        
        pygame.draw.rect(
            self.screen,
            cfg.BUTTON_HOVER_COLOR if (start_hover and can_start) else start_color,
            self.start_button,
            border_radius=10
        )
        pygame.draw.rect(
            self.screen,
            cfg.HIGHLIGHT_COLOR if (start_hover and can_start) else cfg.BORDER_COLOR,
            self.start_button,
            3 if start_hover else 2,
            border_radius=10
        )
        start_text = self.button_font.render("INICIAR", True, cfg.TEXT_COLOR if can_start else cfg.GRAY)
        start_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_rect)
    
    def can_start(self):
        """Verifica si se puede iniciar con la configuración actual"""
        if self.selected_mode == "local":
            return True
            
        if not self.nickname or len(self.nickname) < 2:
            return False
        if self.selected_mode == "client":
            if not self.server_ip:
                return False
        return True
    
    def draw(self):
        """Dibuja la pantalla actual"""
        if self.selected_mode is None:
            self.draw_main_menu()
        else:
            self.draw_config_screen()
    
    def handle_click(self, pos):
        """
        Maneja clicks del mouse
        
        Args:
            pos: Posición del click
            
        Returns:
            String con la acción a realizar o None
        """
        if self.selected_mode is None:
            # Menú principal
            if self.local_button.collidepoint(pos):
                self.selected_mode = "local"
                return None
            elif self.server_button.collidepoint(pos):
                self.selected_mode = "server"
                self.is_entering_nickname = True
                return None
            elif self.client_button.collidepoint(pos):
                self.selected_mode = "client"
                self.is_entering_nickname = True
                return None
        else:
            # Pantalla de configuración
            if self.back_button.collidepoint(pos):
                self.reset_config()
                return None
            elif self.start_button.collidepoint(pos) and self.can_start():
                if self.selected_mode == "server":
                    return "start_server"
                elif self.selected_mode == "local":
                    return "start_local"
                else:
                    return "start_client"
            elif self.nickname_input.collidepoint(pos):
                self.is_entering_nickname = True
                self.is_entering_server_ip = False
            elif self.selected_mode == "client" and self.server_ip_input.collidepoint(pos):
                self.is_entering_nickname = False
                self.is_entering_server_ip = True
            elif self.selected_mode in ["server", "local"]:
                if self.normal_mode_button.collidepoint(pos):
                    self.game_mode = "normal"
                elif self.alt_mode_button.collidepoint(pos):
                    self.game_mode = "alt"
        
        return None
    
    def handle_keypress(self, event):
        """
        Maneja entrada de teclado
        
        Args:
            event: Evento de pygame
        """
        if event.key == pygame.K_RETURN:
            # Enter - cambiar entre campos o iniciar
            if self.is_entering_nickname and self.selected_mode == "client":
                self.is_entering_nickname = False
                self.is_entering_server_ip = True
            elif self.can_start():
                if self.selected_mode == "server":
                    return "start_server"
                elif self.selected_mode == "local":
                    return "start_local"
                else:
                    return "start_client"
        
        elif event.key == pygame.K_BACKSPACE:
            # Borrar último carácter
            if self.is_entering_nickname and self.nickname:
                self.nickname = self.nickname[:-1]
            elif self.is_entering_server_ip and self.server_ip:
                self.server_ip = self.server_ip[:-1]
        
        elif event.key == pygame.K_TAB:
            # Tab - cambiar entre campos
            if self.selected_mode == "client":
                self.is_entering_nickname = not self.is_entering_nickname
                self.is_entering_server_ip = not self.is_entering_server_ip
        
        elif event.unicode:
            # Agregar carácter
            if self.is_entering_nickname and len(self.nickname) < 20:
                self.nickname += event.unicode
            elif self.is_entering_server_ip and len(self.server_ip) < 50:
                self.server_ip += event.unicode
        
        return None
    
    def reset_config(self):
        """Reinicia la configuración al volver al menú principal"""
        self.selected_mode = None
        self.game_mode = "normal"
        self.nickname = ""
        self.server_ip = ""
        self.error_message = ""
        self.is_entering_nickname = False
        self.is_entering_server_ip = False
    
    def get_config(self):
        """
        Obtiene la configuración actual
        
        Returns:
            Diccionario con la configuración
        """
        return {
            "mode": self.selected_mode,
            "nickname": self.nickname,
            "server_ip": self.server_ip,
            "game_mode": self.game_mode
        }
    
    def set_error(self, message):
        """Establece un mensaje de error"""
        self.error_message = message

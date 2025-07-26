def draw_number_history_improved():
    """Dibuja el historial de números sorteados con estilo moderno y elegante."""
    # Definir área para el historial con posición ajustada para asegurar visibilidad correcta
    history_width = int(cfg.WIDTH * 0.22)   # 22% del ancho de pantalla (más ancho)
    history_height = int(cfg.HEIGHT * 0.7)  # 70% de la altura de pantalla
    history_rect = pygame.Rect(
        cfg.WIDTH - history_width - 25,  # Margen derecho reducido
        int(cfg.HEIGHT * 0.1),           # 10% desde la parte superior
        history_width,
        history_height
    )
    
    # Fondo con gradiente sutil y transparencia
    bg_surface = pygame.Surface((history_rect.width, history_rect.height), pygame.SRCALPHA)
    # Gradiente de fondo
    for i in range(history_rect.height):
        alpha = int(220 - (i / history_rect.height) * 50)  # Gradiente de transparencia
        color = (*cfg.BACKGROUND_COLOR, alpha)
        pygame.draw.line(bg_surface, color, (0, i), (history_rect.width, i))
    screen.blit(bg_surface, (history_rect.x, history_rect.y))
    
    # Borde elegante con múltiples capas
    # Sombra exterior
    shadow_rect = pygame.Rect(history_rect.x + 4, history_rect.y + 4, history_rect.width, history_rect.height)
    shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 60))
    screen.blit(shadow_surface, (shadow_rect.x, shadow_rect.y))
    
    # Marco principal con gradiente
    pygame.draw.rect(screen, cfg.PRIMARY_COLOR, history_rect, 4, border_radius=20)
    # Borde interno brillante
    inner_rect = pygame.Rect(history_rect.x + 3, history_rect.y + 3, history_rect.width - 6, history_rect.height - 6)
    pygame.draw.rect(screen, cfg.HIGHLIGHT_COLOR, inner_rect, 2, border_radius=17)
    # Borde más interno
    inner_rect2 = pygame.Rect(history_rect.x + 6, history_rect.y + 6, history_rect.width - 12, history_rect.height - 12)
    pygame.draw.rect(screen, cfg.WHITE, inner_rect2, 1, border_radius=14)
    
    # Título del historial con estilo moderno
    title_y = history_rect.top + 15
    title_text = font_medium.render("HISTORIAL", True, cfg.PRIMARY_COLOR)
    title_rect = title_text.get_rect(centerx=history_rect.centerx, y=title_y)
    # Sombra del título
    shadow_title = font_medium.render("HISTORIAL", True, cfg.BLACK)
    shadow_title_rect = shadow_title.get_rect(centerx=history_rect.centerx + 2, y=title_y + 2)
    screen.blit(shadow_title, shadow_title_rect)
    screen.blit(title_text, title_rect)
    
    # Línea decorativa bajo el título
    line_y = title_y + 35
    pygame.draw.line(screen, cfg.PRIMARY_COLOR, 
                    (history_rect.left + 20, line_y), 
                    (history_rect.right - 20, line_y), 3)
    
    if not game_state.drawn_numbers:
        # Mensaje cuando no hay números
        no_numbers_text = font_small.render("Sin números sorteados", True, cfg.GRAY)
        no_numbers_rect = no_numbers_text.get_rect(center=(history_rect.centerx, history_rect.centery))
        screen.blit(no_numbers_text, no_numbers_rect)
        return
    
    # Organizar números en cuadrícula
    sorted_numbers = sorted(game_state.drawn_numbers)
    cols = 3
    
    # Títulos de rangos con diseño moderno
    range_titles = ["1-30", "31-60", "61-90"]
    range_colors = [cfg.RANGE_1_30, cfg.RANGE_31_60, cfg.RANGE_61_90]
    
    # Barra de rangos
    range_bar_y = line_y + 15
    range_bar_height = 30
    
    # Distribuir etiquetas uniformemente
    label_width = (history_rect.width - 60) // 3
    for i in range(3):
        x_pos = history_rect.left + 20 + i * (label_width + 10)
        
        # Rectángulo de etiqueta con gradiente
        label_rect = pygame.Rect(x_pos, range_bar_y, label_width, range_bar_height)
        
        # Fondo con gradiente
        label_surface = pygame.Surface((label_width, range_bar_height), pygame.SRCALPHA)
        for j in range(range_bar_height):
            alpha = int(200 - (j / range_bar_height) * 100)
            color = (*range_colors[i][:3], alpha)
            pygame.draw.line(label_surface, color, (0, j), (label_width, j))
        screen.blit(label_surface, (x_pos, range_bar_y))
        
        # Borde de la etiqueta
        pygame.draw.rect(screen, range_colors[i], label_rect, 2, border_radius=8)
        
        # Texto de la etiqueta
        range_text = font_small.render(range_titles[i], True, cfg.WHITE)
        range_rect = range_text.get_rect(center=label_rect.center)
        # Sombra del texto
        shadow_range = font_small.render(range_titles[i], True, cfg.BLACK)
        shadow_range_rect = shadow_range.get_rect(center=(label_rect.centerx + 1, label_rect.centery + 1))
        screen.blit(shadow_range, shadow_range_rect)
        screen.blit(range_text, range_rect)
    
    # Dibujar números
    start_y = range_bar_y + range_bar_height + 20
    cell_width = (history_rect.width - 60) // cols
    cell_height = 35
    
    for i, num in enumerate(sorted_numbers):
        col = i % cols
        row = i // cols
        
        # Limitar número de filas visibles
        if row >= 12:  # Máximo 12 filas (36 números)
            remaining = len(sorted_numbers) - 36
            if remaining > 0:
                more_text = font_small.render(f"+ {remaining} más", True, cfg.PRIMARY_COLOR)
                more_rect = more_text.get_rect(center=(history_rect.centerx, history_rect.bottom - 30))
                screen.blit(more_text, more_rect)
            break
        
        # Posición de la celda
        x = history_rect.left + 20 + col * (cell_width + 10)
        y = start_y + row * (cell_height + 8)
        
        # Determinar color del número
        if num <= 30:
            number_color = cfg.RANGE_1_30
            glow_color = (130, 134, 251)
        elif num <= 60:
            number_color = cfg.RANGE_31_60
            glow_color = (251, 191, 36)
        else:
            number_color = cfg.RANGE_61_90
            glow_color = (236, 72, 153)
        
        # Rectángulo de la celda
        cell_rect = pygame.Rect(x, y, cell_width, cell_height)
        
        # Destacar número actual
        if num == game_state.current_number:
            # Efecto de brillo pulsante
            pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 0.5 + 0.5
            for j in range(5, 0, -1):
                glow_rect = cell_rect.inflate(j * 2, j * 2)
                alpha = int(pulse * (100 - j * 15))
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                glow_surface.fill((*glow_color, alpha))
                screen.blit(glow_surface, glow_rect)
            
            # Fondo brillante
            pygame.draw.rect(screen, number_color, cell_rect, border_radius=8)
            text_color = cfg.WHITE if num <= 30 or num > 60 else cfg.BLACK
        else:
            # Fondo normal
            pygame.draw.rect(screen, cfg.WHITE, cell_rect, border_radius=8)
            pygame.draw.rect(screen, number_color, cell_rect, 2, border_radius=8)
            text_color = number_color
        
        # Texto del número
        num_text = font_small.render(str(num), True, text_color)
        num_rect = num_text.get_rect(center=cell_rect.center)
        
        # Sombra del número si es el actual
        if num == game_state.current_number:
            shadow_num = font_small.render(str(num), True, cfg.BLACK)
            shadow_num_rect = shadow_num.get_rect(center=(cell_rect.centerx + 1, cell_rect.centery + 1))
            screen.blit(shadow_num, shadow_num_rect)
        
        screen.blit(num_text, num_rect)

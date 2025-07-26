#!/usr/bin/env python3
"""
Script para probar el nuevo posicionamiento del número actual
alineado con el historial
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config as cfg

def test_positioning():
    """Prueba el posicionamiento del número actual vs historial"""
    print("🎯 Probando posicionamiento del número actual alineado con historial")
    print("=" * 70)
    
    # Usar resolución actual
    config = cfg.get_resolution_config()
    
    # Simular factores de escala (simplificado)
    SCALE_X = cfg.WIDTH / 1024
    SCALE_Y = cfg.HEIGHT / 768
    
    def scale_value(value, is_horizontal=True, min_value=None, max_value=None):
        if is_horizontal:
            scaled = int(value * SCALE_X)
        else:
            scaled = int(value * SCALE_Y)
        
        if min_value is not None:
            scaled = max(scaled, min_value)
        if max_value is not None:
            scaled = min(scaled, max_value)
        
        return scaled
    
    # Calcular posiciones del número actual (valores actualizados - 1px más abajo)
    current_number_x = scale_value(60, min_value=40, max_value=120)
    current_number_y = scale_value(25, False, min_value=17, max_value=49)  # +1px adjustment
    current_number_width = scale_value(config["current_number_size"] * 1.2, min_value=250, max_value=400)
    current_number_height = scale_value(config["current_number_size"] * 0.7, min_value=160, max_value=280)
    
    # Calcular posiciones del historial (valores actualizados - 1px más abajo)
    history_width_ratio = 0.22  # Valor típico para standard
    history_width = int(cfg.WIDTH * history_width_ratio)
    history_x = cfg.WIDTH - history_width - scale_value(24, min_value=16, max_value=32)
    history_y = scale_value(25, False, min_value=17, max_value=49)  # +1px adjustment
    history_height = int(cfg.HEIGHT * 0.7)
    
    print(f"📱 Resolución: {cfg.WIDTH}x{cfg.HEIGHT}")
    print(f"📊 Configuración: {[k for k, v in cfg.RESOLUTION_CONFIGS.items() if v == config][0]}")
    print()
    
    print("📍 NÚMERO ACTUAL:")
    print(f"  • Posición: ({current_number_x}, {current_number_y})")
    print(f"  • Dimensiones: {current_number_width}x{current_number_height}px")
    print(f"  • Área final: ({current_number_x}, {current_number_y}) a ({current_number_x + current_number_width}, {current_number_y + current_number_height})")
    print()
    
    print("📍 HISTORIAL:")
    print(f"  • Posición: ({history_x}, {history_y})")
    print(f"  • Dimensiones: {history_width}x{history_height}px")
    print(f"  • Área final: ({history_x}, {history_y}) a ({history_x + history_width}, {history_y + history_height})")
    print()
    
    # Verificar alineación
    y_difference = abs(current_number_y - history_y)
    print("🎯 ALINEACIÓN:")
    if y_difference == 0:
        print("  ✅ Perfectamente alineados en Y")
    elif y_difference <= 5:
        print(f"  ✅ Casi perfectamente alineados (diferencia: {y_difference}px)")
    else:
        print(f"  ⚠️  Desalineados (diferencia: {y_difference}px)")
    
    # Verificar separación horizontal
    horizontal_gap = history_x - (current_number_x + current_number_width)
    print(f"  • Separación horizontal: {horizontal_gap}px")
    
    if horizontal_gap > 100:
        print("  ✅ Separación adecuada")
    elif horizontal_gap > 50:
        print("  ⚠️  Separación justa")
    else:
        print("  ❌ Separación insuficiente")
    
    # Calcular posición del tablero para verificar que no interfiere
    board_y = config["board_margin_top"]
    board_clearance = board_y - (current_number_y + current_number_height)
    
    print()
    print("🎲 TABLERO:")
    print(f"  • Posición Y: {board_y}px")
    print(f"  • Separación del número actual: {board_clearance}px")
    
    if board_clearance > 50:
        print("  ✅ Sin interferencia con el tablero")
    elif board_clearance > 20:
        print("  ⚠️  Separación justa del tablero")
    else:
        print("  ❌ Posible interferencia con el tablero")
    
    print()
    print("📐 DISTRIBUCIÓN DE PANTALLA:")
    left_section = current_number_x + current_number_width
    right_section = history_x
    center_section = right_section - left_section
    
    print(f"  • Sección izquierda (número actual): {left_section}px ({left_section/cfg.WIDTH*100:.1f}%)")
    print(f"  • Sección central (tablero): {center_section}px ({center_section/cfg.WIDTH*100:.1f}%)")
    print(f"  • Sección derecha (historial): {history_width}px ({history_width/cfg.WIDTH*100:.1f}%)")

if __name__ == "__main__":
    test_positioning()
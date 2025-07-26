#!/usr/bin/env python3
"""
Script de prueba para verificar las mejoras del sistema de resoluciones
"""

import pygame
import sys
import os

# Agregar el directorio actual al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config as cfg

def test_resolution_configs():
    """Prueba las configuraciones de resolución"""
    print("🔍 Probando configuraciones de resolución...")
    
    # Probar diferentes resoluciones
    test_resolutions = [
        (3456, 2234, "4K Ultra"),
        (2560, 1440, "2K"),
        (1920, 1080, "1080p"),
        (1366, 768, "720p"),
        (1024, 768, "Pequeña")
    ]
    
    for width, height, name in test_resolutions:
        # Simular la resolución
        cfg.WIDTH = width
        cfg.HEIGHT = height
        
        config = cfg.get_resolution_config()
        
        print(f"\n📺 {name} ({width}x{height}):")
        print(f"  • Tamaño de celda: {config['board_cell_size']}px")
        print(f"  • Tamaño número actual: {config['current_number_size']}px")
        print(f"  • Margen título: {config['title_margin']}px")
        print(f"  • Margen tablero: {config['board_margin_top']}px")
        print(f"  • Multiplicador espaciado: {config['spacing_multiplier']}")
        
        # Calcular dimensiones del tablero
        cell_size = config['board_cell_size']
        cell_spacing = int(cell_size * 0.12)
        board_width = 10 * cell_size + 9 * cell_spacing  # 10 columnas
        board_height = 9 * cell_size + 8 * cell_spacing  # 9 filas
        
        print(f"  • Dimensiones tablero: {board_width}x{board_height}px")
        print(f"  • Porcentaje pantalla: {(board_width * board_height) / (width * height) * 100:.1f}%")

def test_layout_spacing():
    """Prueba el espaciado entre elementos"""
    print("\n🎯 Probando espaciado de elementos...")
    
    # Usar resolución actual
    config = cfg.get_resolution_config()
    
    # Posiciones de elementos
    current_number_y = config['title_margin'] + 40
    board_y = config['board_margin_top']
    
    print(f"📍 Posiciones (resolución {cfg.WIDTH}x{cfg.HEIGHT}):")
    print(f"  • Número actual Y: {current_number_y}px")
    print(f"  • Tablero Y: {board_y}px")
    print(f"  • Separación: {board_y - current_number_y}px")
    
    # Verificar que no hay solapamiento
    current_number_height = config['current_number_size'] * 0.9
    if (current_number_y + current_number_height) < board_y:
        print("  ✅ Sin solapamiento detectado")
    else:
        print("  ⚠️  Posible solapamiento detectado")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del sistema de resoluciones mejorado")
    print("=" * 60)
    
    test_resolution_configs()
    test_layout_spacing()
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
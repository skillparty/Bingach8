#!/usr/bin/env python3
"""
Script para probar el juego en diferentes resoluciones
Uso: python3 test_resolutions.py [resolución]

Resoluciones disponibles:
- 4k: 3840x2160
- 2k: 2560x1440  
- 1080p: 1920x1080
- 720p: 1366x768
- small: 1024x768
- custom: Permite especificar ancho y alto
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Probar Bingacho en diferentes resoluciones')
    parser.add_argument('resolution', nargs='?', default='1080p', 
                       choices=['4k', '2k', '1080p', '720p', 'small', 'custom'],
                       help='Resolución a probar')
    parser.add_argument('--width', type=int, help='Ancho personalizado (solo con custom)')
    parser.add_argument('--height', type=int, help='Alto personalizado (solo con custom)')
    parser.add_argument('--windowed', action='store_true', help='Ejecutar en modo ventana')
    
    args = parser.parse_args()
    
    # Definir resoluciones
    resolutions = {
        '4k': (3840, 2160),
        '2k': (2560, 1440),
        '1080p': (1920, 1080),
        '720p': (1366, 768),
        'small': (1024, 768)
    }
    
    if args.resolution == 'custom':
        if not args.width or not args.height:
            print("❌ Error: Para resolución custom debes especificar --width y --height")
            sys.exit(1)
        width, height = args.width, args.height
        resolution_name = f"{width}x{height}"
    else:
        width, height = resolutions[args.resolution]
        resolution_name = args.resolution.upper()
    
    print(f"🎮 Iniciando Bingacho en resolución {resolution_name} ({width}x{height})")
    
    # Modificar config.py temporalmente
    import config as cfg
    
    # Guardar valores originales
    original_width = cfg.WIDTH
    original_height = cfg.HEIGHT
    original_fullscreen = cfg.FULLSCREEN
    
    # Establecer nueva resolución
    cfg.WIDTH = width
    cfg.HEIGHT = height
    cfg.FULLSCREEN = not args.windowed
    
    try:
        # Importar y ejecutar el juego
        import main
    except KeyboardInterrupt:
        print("\n🛑 Juego interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar el juego: {e}")
    finally:
        # Restaurar valores originales
        cfg.WIDTH = original_width
        cfg.HEIGHT = original_height
        cfg.FULLSCREEN = original_fullscreen

if __name__ == "__main__":
    main()
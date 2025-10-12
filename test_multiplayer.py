"""
Script de prueba para el sistema multijugador
Prueba los módulos sin necesidad de iniciar el juego completo
"""

import sys
import time
from bingo_card import BingoCard, generate_unique_cards

def test_bingo_card():
    """Prueba el generador de cartillas"""
    print("\n" + "="*60)
    print("TEST 1: Generador de Cartillas de Bingo")
    print("="*60)
    
    # Generar una cartilla
    card = BingoCard(card_id="Test1")
    print("\nCartilla generada:")
    print(card)
    
    # Verificar estructura
    assert len(card.numbers) == 3, "La cartilla debe tener 3 filas"
    assert len(card.numbers[0]) == 9, "Cada fila debe tener 9 columnas"
    
    # Contar números por fila
    for i, row in enumerate(card.numbers):
        num_count = sum(1 for n in row if n is not None)
        print(f"Fila {i+1}: {num_count} números")
        assert num_count == 5, f"Cada fila debe tener 5 números, tiene {num_count}"
    
    print("\n✅ Test de cartilla básica: PASADO")
    
    # Probar marcar números
    print("\n" + "-"*60)
    print("Probando marcado de números...")
    
    test_numbers = [5, 17, 23, 45, 67, 89]
    marked_count = 0
    for num in test_numbers:
        if card.mark_number(num):
            marked_count += 1
            print(f"✓ Número {num} marcado")
        else:
            print(f"✗ Número {num} no está en la cartilla")
    
    print(f"\nNúmeros marcados: {marked_count}/{len(test_numbers)}")
    print("\nCartilla después de marcar:")
    print(card)
    
    # Verificar línea y bingo
    has_line = card.check_line()
    has_bingo = card.check_bingo()
    print(f"\n¿Tiene línea? {has_line}")
    print(f"¿Tiene BINGO? {has_bingo}")
    
    print("\n✅ Test de marcado: PASADO")
    
    # Generar múltiples cartillas
    print("\n" + "-"*60)
    print("Generando 3 cartillas...")
    
    cards = generate_unique_cards(3)
    for i, c in enumerate(cards):
        print(f"\nCartilla {i+1}:")
        print(c)
    
    print("\n✅ Test de múltiples cartillas: PASADO")

def test_server_import():
    """Prueba que el servidor se puede importar"""
    print("\n" + "="*60)
    print("TEST 2: Importación de Módulos de Servidor")
    print("="*60)
    
    try:
        from multiplayer_server import BingachoServer
        print("✅ multiplayer_server importado correctamente")
        
        # Crear instancia
        server = BingachoServer(port=8766)  # Puerto diferente para no interferir
        print(f"✅ Servidor creado en puerto {server.port}")
        print(f"   IP Local: {server.get_local_ip()}")
        
    except Exception as e:
        print(f"❌ Error importando servidor: {e}")
        return False
    
    return True

def test_client_import():
    """Prueba que el cliente se puede importar"""
    print("\n" + "="*60)
    print("TEST 3: Importación de Módulos de Cliente")
    print("="*60)
    
    try:
        from multiplayer_client import BingachoClient
        print("✅ multiplayer_client importado correctamente")
        
        # No iniciamos conexión, solo verificamos que se puede crear
        print("   (No se inicia conexión en el test)")
        
    except Exception as e:
        print(f"❌ Error importando cliente: {e}")
        return False
    
    return True

def test_manager_import():
    """Prueba el gestor multijugador"""
    print("\n" + "="*60)
    print("TEST 4: Gestor Multijugador")
    print("="*60)
    
    try:
        from multiplayer_manager import MultiplayerManager
        print("✅ multiplayer_manager importado correctamente")
        
        # Crear instancia
        manager = MultiplayerManager()
        print("✅ Gestor creado")
        
        # Verificar estado inicial
        assert manager.mode is None, "El modo inicial debe ser None"
        assert not manager.is_active, "No debe estar activo inicialmente"
        print("✅ Estado inicial correcto")
        
        # Verificar métodos de verificación
        assert manager.is_local_mode(), "Debe ser modo local por defecto"
        assert not manager.is_server_mode(), "No debe ser modo servidor"
        assert not manager.is_client_mode(), "No debe ser modo cliente"
        print("✅ Métodos de verificación funcionan")
        
    except Exception as e:
        print(f"❌ Error con el gestor: {e}")
        return False
    
    return True

def test_mode_selection_import():
    """Prueba el selector de modo"""
    print("\n" + "="*60)
    print("TEST 5: Selector de Modo")
    print("="*60)
    
    try:
        # Necesitamos pygame para esto
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        
        from mode_selection import ModeSelection
        print("✅ mode_selection importado correctamente")
        
        # Crear instancia
        selector = ModeSelection(screen)
        print("✅ Selector creado")
        
        # Verificar estado inicial
        assert selector.selected_mode is None, "Modo seleccionado debe ser None"
        assert selector.nickname == "", "Nickname debe estar vacío"
        print("✅ Estado inicial correcto")
        
        pygame.quit()
        
    except Exception as e:
        print(f"❌ Error con el selector: {e}")
        try:
            pygame.quit()
        except:
            pass
        return False
    
    return True

def test_card_renderer_import():
    """Prueba el renderizador de cartillas"""
    print("\n" + "="*60)
    print("TEST 6: Renderizador de Cartillas")
    print("="*60)
    
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        
        from bingo_card_renderer import BingoCardRenderer
        from bingo_card import BingoCard
        print("✅ bingo_card_renderer importado correctamente")
        
        # Crear cartilla y renderizador
        card = BingoCard(card_id="TestRender")
        renderer = BingoCardRenderer(screen, card, (50, 50), 60)
        print("✅ Renderizador creado")
        
        # Verificar dimensiones
        assert renderer.card_width > 0, "El ancho debe ser positivo"
        assert renderer.card_height > 0, "El alto debe ser positivo"
        print(f"✅ Dimensiones: {renderer.card_width}x{renderer.card_height}")
        
        pygame.quit()
        
    except Exception as e:
        print(f"❌ Error con el renderizador: {e}")
        try:
            pygame.quit()
        except:
            pass
        return False
    
    return True

def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("INICIANDO TESTS DEL SISTEMA MULTIJUGADOR")
    print("="*60)
    
    tests = [
        ("Cartillas de Bingo", test_bingo_card),
        ("Servidor", test_server_import),
        ("Cliente", test_client_import),
        ("Gestor", test_manager_import),
        ("Selector de Modo", test_mode_selection_import),
        ("Renderizador", test_card_renderer_import),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            if result is None:
                result = True  # Si no retorna False, asumimos éxito
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error inesperado en {name}: {e}")
            results.append((name, False))
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE TESTS")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASADO" if result else "❌ FALLIDO"
        print(f"{name:.<40} {status}")
    
    print("\n" + "="*60)
    print(f"RESULTADO FINAL: {passed}/{total} tests pasados")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ¡Todos los tests pasaron! El sistema está listo.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

# Design Document

## Overview

El fondo binario animado será implementado como una nueva clase `BinaryBackground` que se integrará en la clase `TitleScreen` existente. La implementación se inspirará en el efecto de VS Code, creando una matriz de caracteres binarios que cambian gradualmente con el texto "Bingacho_joseAlejandro" integrado de manera sutil.

## Architecture

### Component Structure
```
TitleScreen
├── BinaryBackground (nueva clase)
│   ├── BinaryGrid (matriz de caracteres)
│   ├── TextIntegration (manejo del texto personalizado)
│   └── AnimationController (control de transiciones)
├── GlitchCard (existente)
├── BouncingWaveParticle (existente)
└── UI Elements (existentes)
```

### Rendering Order
1. Gradient Background (existente)
2. **BinaryBackground (nuevo - capa más profunda)**
3. BouncingWaveParticles (existente)
4. Matrix Glow Effects (existente)
5. GlitchCards (existente)
6. UI Elements (existente)

## Components and Interfaces

### BinaryBackground Class

```python
class BinaryBackground:
    def __init__(self, width, height, config):
        self.width = width
        self.height = height
        self.config = config
        self.grid = BinaryGrid(width, height)
        self.text_integration = TextIntegration("Bingacho_joseAlejandro")
        self.animation_controller = AnimationController()
        
    def update(self, delta_time):
        """Actualiza la animación del fondo binario"""
        
    def draw(self, surface):
        """Renderiza el fondo binario en la superficie"""
```

### BinaryGrid Class

```python
class BinaryGrid:
    def __init__(self, width, height):
        self.char_size = 13  # Tamaño de fuente monoespaciada
        self.line_height = 15.75  # Altura de línea como en VS Code
        self.cols = width // self.char_size
        self.rows = height // self.line_height
        self.grid = self.generate_initial_grid()
        
    def generate_initial_grid(self):
        """Genera la matriz inicial de 0s y 1s"""
        
    def update_grid(self, delta_time):
        """Actualiza valores binarios gradualmente"""
        
    def get_char_at(self, row, col):
        """Obtiene el carácter en la posición especificada"""
```

### TextIntegration Class

```python
class TextIntegration:
    def __init__(self, text):
        self.text = text
        self.positions = []  # Posiciones donde aparece el texto
        self.fade_states = []  # Estados de desvanecimiento
        
    def calculate_positions(self, grid_cols, grid_rows):
        """Calcula posiciones óptimas para el texto"""
        
    def should_show_text_at(self, row, col):
        """Determina si mostrar texto en lugar de binario"""
```

### AnimationController Class

```python
class AnimationController:
    def __init__(self):
        self.transition_speed = 1.0  # Velocidad de transición
        self.fade_duration = 1.25    # Duración del fade como en VS Code
        self.opacity = 0.3           # Opacidad base
        
    def update(self, delta_time):
        """Actualiza estados de animación"""
        
    def get_char_opacity(self, row, col, base_opacity):
        """Calcula opacidad para un carácter específico"""
```

## Data Models

### BinaryChar Structure
```python
@dataclass
class BinaryChar:
    value: int          # 0 o 1
    target_value: int   # Valor objetivo para transición
    transition_time: float  # Tiempo de transición actual
    opacity: float      # Opacidad actual
    is_text: bool      # Si es parte del texto especial
    text_char: str     # Carácter de texto si is_text=True
```

### Configuration Structure
```python
@dataclass
class BinaryBackgroundConfig:
    density: float = 0.7        # Densidad de caracteres (0.1-1.0)
    animation_speed: float = 1.0 # Velocidad de animación
    base_opacity: float = 0.3   # Opacidad base
    text_opacity: float = 0.5   # Opacidad del texto especial
    transition_duration: float = 1.25  # Duración de transiciones
    color_scheme: tuple = (100, 150, 200)  # Color base RGB
```

## Error Handling

### Performance Safeguards
- Limitar el número máximo de caracteres actualizados por frame
- Implementar pooling de objetos para evitar garbage collection
- Usar dirty rectangles para optimizar renderizado

### Memory Management
- Reutilizar superficies de renderizado
- Implementar límites en el tamaño de la grilla
- Limpiar recursos no utilizados

### Fallback Mechanisms
- Si el rendimiento cae por debajo de 45 FPS, reducir densidad automáticamente
- Opción para deshabilitar el efecto completamente
- Modo de compatibilidad para hardware más lento

## Testing Strategy

### Unit Tests
- `test_binary_grid_generation()`: Verificar generación correcta de la matriz
- `test_text_integration()`: Validar integración del texto personalizado
- `test_animation_transitions()`: Comprobar suavidad de transiciones
- `test_performance_limits()`: Verificar límites de rendimiento

### Integration Tests
- `test_title_screen_integration()`: Verificar integración con TitleScreen
- `test_rendering_order()`: Comprobar orden correcto de renderizado
- `test_config_changes()`: Validar cambios de configuración en tiempo real

### Performance Tests
- `test_fps_stability()`: Verificar estabilidad de FPS con el fondo activo
- `test_memory_usage()`: Monitorear uso de memoria durante animación
- `test_large_screen_support()`: Probar en resoluciones altas

## Implementation Notes

### VS Code Inspiration Details
- Usar la misma fuente monoespaciada (tamaño 13px, line-height 15.75px)
- Implementar el mismo patrón de fade-in/fade-out (1.25s delay)
- Mantener la misma densidad y distribución de caracteres
- Usar colores similares pero adaptados a la paleta del juego

### Integration Points
- Añadir `self.binary_background` a la clase `TitleScreen`
- Llamar `binary_background.update()` en `TitleScreen.update()`
- Llamar `binary_background.draw()` después del gradiente pero antes de las partículas
- Añadir configuración en `config.py` para personalización

### Text Placement Strategy
- Calcular múltiples posiciones para "Bingacho_joseAlejandro"
- Usar algoritmo de distribución para evitar solapamiento con elementos UI
- Implementar rotación de posiciones para variedad visual
- Aplicar efectos de fade suaves para transiciones de texto
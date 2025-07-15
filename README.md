# Bingacho

Juego de bingo con audio genial y animaciones geniales.

## Descripción

Bingacho es un juego de bingo para PC que incluye:
- Animación de pelotas cayendo con los números del bingo
- Tablero con los 90 números disponibles
- Audio para cada número cuando es seleccionado
- Interfaz amigable con botones de inicio y bingo

## Requisitos

- Python 3.7 o superior
- Pygame
- Pydub (para manejo de audio)

## Instalación

1. Clona este repositorio:
```
git clone https://github.com/skillparty/Bingacho.git
cd Bingacho
```

2. Instala las dependencias:
```
pip install -r requirements.txt
```

3. Ejecuta el juego:
```
python main.py
```

## Cómo jugar

1. Haz clic en el botón "Iniciar" para comenzar el juego
2. Las pelotas caerán una a una mostrando los números del bingo
3. Cuando todos los números que necesites hayan salido, haz clic en "¡BINGO!"
4. Los números ganadores se iluminarán en el tablero

## Estructura del proyecto

- `main.py`: Archivo principal del juego
- `assets/`: Carpeta con imágenes y otros recursos
- `audios/`: Archivos de audio para cada número

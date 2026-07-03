#!/bin/bash
# Navegar al directorio del script para evitar problemas de rutas
cd "$(dirname "$0")"

# Verificar si existe el entorno virtual y ejecutar con él
if [ -d ".venv" ]; then
    echo "🎮 Iniciando Bingacho con el entorno virtual..."
    ./.venv/bin/python main.py
else
    echo "⚠️ No se encontró la carpeta .venv. Intentando ejecutar con el Python del sistema..."
    python3 main.py
fi

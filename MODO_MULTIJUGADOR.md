# Modo Multijugador - Bingacho

## Descripción

El juego Bingacho ahora incluye un modo multijugador que permite jugar en red local usando WebSockets. El sistema soporta tres modos de juego:

1. **Modo Local**: Juego tradicional en solitario
2. **Modo Servidor (Host)**: Controlas el sorteo y los demás se conectan a ti
3. **Modo Cliente (Jugador)**: Te conectas a una partida existente con tu propia cartilla

## Instalación

Antes de usar el modo multijugador, instala las dependencias:

```bash
pip install -r requirements.txt
```

Esto instalará:
- `pygame==2.6.1`
- `websockets==12.0`

## Cómo Jugar

### 1. Modo Local (Sin Red)

1. Ejecuta el juego: `python main.py`
2. En la pantalla de título, selecciona "INICIAR JUEGO"
3. En la selección de modo, elige "MODO LOCAL"
4. Juega normalmente con el tablero de 90 números

### 2. Modo Servidor (Host)

**Como servidor, controlas el sorteo de números.**

1. Ejecuta el juego: `python main.py`
2. En la pantalla de título, selecciona "INICIAR JUEGO"
3. En la selección de modo, elige "CREAR PARTIDA (SERVIDOR)"
4. Ingresa tu nickname (ej: "Host")
5. Presiona "INICIAR"
6. **Importante**: Anota la IP que aparece en pantalla (ej: `192.168.1.100`)
7. Comparte esta IP con los demás jugadores
8. Cuando estés listo, presiona el botón "INICIAR JUEGO" para sortear números
9. Cada vez que presiones "SIGUIENTE NÚMERO", todos los clientes recibirán el número

**Lo que verás:**
- Tablero de 90 números (9x10)
- Historial de números sorteados
- Número actual grande
- Información del servidor en la parte superior (IP y número de clientes conectados)

### 3. Modo Cliente (Jugador)

**Como cliente, recibes los números y marcas tu cartilla.**

1. Ejecuta el juego en tu computadora: `python main.py`
2. En la pantalla de título, selecciona "INICIAR JUEGO"
3. En la selección de modo, elige "UNIRSE A PARTIDA"
4. Ingresa tu nickname (ej: "Jugador1")
5. Ingresa la IP del servidor que te compartió el host (ej: `192.168.1.100`)
6. Presiona "INICIAR"
7. Espera a que el servidor comience a sortear números
8. Tu cartilla se marcará automáticamente cuando salgan tus números

**Lo que verás:**
- Tu cartilla personal (3 filas x 9 columnas)
- Tablero de 90 números (sincronizado con el servidor)
- Historial de números sorteados
- Número actual grande
- Estado de conexión en la parte superior

## Características del Modo Multijugador

### Cartillas Aleatorias
- Cada cliente recibe una cartilla única generada aleatoriamente
- Formato estilo bingo español: 3 filas x 9 columnas
- Cada fila tiene 5 números y 4 espacios vacíos
- Los números están distribuidos por rangos de 10 (columna 1: 1-10, columna 2: 11-20, etc.)

### Sincronización Automática
- Los números sorteados se sincronizan instantáneamente con todos los clientes
- Las cartillas se marcan automáticamente
- Detección automática de LÍNEA (fila completa)
- Detección automática de BINGO (cartilla completa)

### Información en Pantalla

**Modo Servidor:**
```
Servidor: [Nickname] | IP: [IP Local] | Clientes: [Número]
```

**Modo Cliente:**
```
Conectado: [Nickname] | Jugadores: [Total]
```

## Requisitos de Red

- **Todos los dispositivos deben estar en la misma red local** (Wi-Fi o Ethernet)
- Puerto usado: **8765** (debe estar abierto en el firewall)
- El servidor debe permitir conexiones entrantes en este puerto

### Verificar Conectividad

Si tienes problemas de conexión:

1. **En el servidor (Host):**
   - Verifica que el firewall no bloquee Python
   - Anota la IP local que muestra el juego
   - En macOS: `ifconfig | grep "inet " | grep -v 127.0.0.1`
   - En Windows: `ipconfig`

2. **En los clientes:**
   - Asegúrate de estar en la misma red Wi-Fi
   - Prueba hacer ping al servidor: `ping [IP_DEL_SERVIDOR]`
   - Si el ping funciona, el juego debería conectar

## Controles

### Modo Local
- **INICIAR JUEGO / SIGUIENTE NÚMERO**: Sortea el primer/siguiente número
- **ESPACIO**: Sortea siguiente número (atajo rápido de teclado) ⌨️
- **REINICIAR**: Reinicia la partida
- **BINGO**: Muestra animación de victoria
- **ESC**: Salir del juego

### Modo Servidor
- **INICIAR JUEGO / SIGUIENTE NÚMERO**: Sortea el primer/siguiente número
- **ESPACIO**: Sortea siguiente número (atajo rápido de teclado) ⌨️
- **REINICIAR**: Reinicia la partida (limpia tablero y cartillas de clientes)
- **BINGO**: Muestra animación de victoria
- **ESC**: Salir del juego

### Modo Cliente
- **REINICIAR**: Limpia tu cartilla (se sincronizará con el servidor)
- **BINGO**: Muestra animación de victoria
- **ESC**: Salir del juego

**Nota**: En modo cliente, NO puedes sortear números con ESPACIO. Solo el servidor controla el sorteo.

## Arquitectura Técnica

### Módulos Creados

1. **`bingo_card.py`**: Generador de cartillas aleatorias
2. **`multiplayer_server.py`**: Servidor WebSocket
3. **`multiplayer_client.py`**: Cliente WebSocket
4. **`multiplayer_manager.py`**: Gestor de modos multijugador
5. **`mode_selection.py`**: Pantalla de selección de modo
6. **`bingo_card_renderer.py`**: Renderizador de cartillas en pygame

### Protocolo de Mensajes

El servidor y los clientes se comunican usando JSON sobre WebSockets:

**Mensajes del Cliente al Servidor:**
```json
{"type": "register", "nickname": "Jugador1"}
{"type": "ping"}
```

**Mensajes del Servidor a los Clientes:**
```json
{"type": "game_state", "game_started": true, "drawn_numbers": [5, 23, 67], "current_number": 67}
{"type": "new_number", "number": 42, "drawn_numbers": [5, 23, 42, 67]}
{"type": "game_started"}
{"type": "game_reset"}
{"type": "player_joined", "nickname": "Jugador2", "total_players": 3}
{"type": "player_left", "nickname": "Jugador1", "total_players": 2}
```

## Solución de Problemas

### Error: "No se pudo conectar al servidor"
- Verifica que el servidor esté ejecutándose
- Comprueba que la IP sea correcta
- Asegúrate de estar en la misma red
- Verifica el firewall

### Error: "Error iniciando servidor"
- El puerto 8765 puede estar en uso
- Intenta reiniciar el juego
- Verifica permisos de red

### La cartilla no se marca automáticamente
- Verifica la conexión en la parte superior de la pantalla
- El número debe estar en tu cartilla para marcarse
- Si dice "Desconectado", intenta reiniciar el cliente

### Los números no se sincronizan
- Solo el servidor puede sortear números
- Los clientes deben esperar a que el servidor sortee
- Verifica el estado de conexión

## Ejemplos de Uso

### Ejemplo 1: Juego en Casa

1. **Host (Laptop):**
   - Inicia como servidor
   - Nickname: "Casa"
   - IP mostrada: `192.168.1.100`

2. **Jugadores (Tablets/Computadoras):**
   - Se conectan como clientes
   - Nicknames: "Mamá", "Papá", "Hijo"
   - IP: `192.168.1.100`

3. **Juego:**
   - El host sortea números con el botón "SIGUIENTE NÚMERO"
   - Cada jugador ve su cartilla marcarse automáticamente
   - Cuando alguien completa una línea, aparece "¡LÍNEA!"
   - Cuando alguien completa toda la cartilla, aparece "¡¡¡BINGO!!!"

### Ejemplo 2: Juego en Oficina

1. **Servidor (Computadora Principal):**
   - Conectada a la red de oficina
   - IP: `10.0.0.50`

2. **Clientes (5 computadoras):**
   - Todas conectadas a la misma red
   - Se conectan a `10.0.0.50`

## Notas Importantes

- ⚠️ **Modo solo para servidor:** En modo servidor, SOLO se muestra el tablero de 90 números, sin cartilla personal
- ⚠️ **Sin base de datos:** Los nicknames son temporales y solo existen durante la sesión
- ⚠️ **Cartillas únicas:** Cada cliente genera su propia cartilla al conectarse
- ⚠️ **Sincronización en tiempo real:** Los números se envían instantáneamente a todos los clientes
- ⚠️ **Desconexión:** Si un cliente se desconecta, su cartilla se pierde (deberá reconectarse con una nueva)

## Futuras Mejoras (Opcionales)

- Permitir múltiples cartillas por jugador
- Chat entre jugadores
- Guardado de estadísticas
- Modo torneo
- Sonidos de notificación cuando alguien hace LÍNEA o BINGO
- Opción de velocidad automática de sorteo

---

**¡Disfruta jugando Bingacho en modo multijugador!** 🎉

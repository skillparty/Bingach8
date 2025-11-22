# Modo Espectador - Bingacho

El modo espectador permite que dispositivos adicionales (celulares, tablets, computadoras) visualicen y escuchen el juego en tiempo real desde cualquier lugar dentro de la misma red local.

## ¿Qué es el Modo Espectador?

Los espectadores pueden:
- ✅ **Ver el tablero del juego en tiempo real** (se actualiza cada ~0.6 segundos)
- ✅ **Escuchar los números cantados** con el audio sincronizado
- ❌ **NO pueden** controlar el juego (solo el host puede sortear números)

## Requisitos

- Todos los dispositivos deben estar conectados a la **misma red WiFi/LAN**
- El host debe ejecutar el juego en **modo Servidor**
- Los espectadores necesitan:
  - **Opción 1 (Móviles/Tablets):** Navegador web moderno (Chrome, Safari, Firefox)
  - **Opción 2 (Computadoras):** Python 3 con pygame instalado

## Instrucciones Paso a Paso

### 1. Iniciar el Host (Servidor)

1. En la computadora que será el **host**, ejecuta:
   ```bash
   python3 main.py
   ```

2. En la pantalla de selección de modo, elige **"Servidor (Host)"**

3. El servidor mostrará información importante en la consola:
   ```
   ============================================================
   Servidor Bingacho iniciado
   ============================================================
   IP Local: 192.168.1.100
   Puerto: 8765
   Los clientes deben conectarse a: ws://192.168.1.100:8765
   ============================================================

   ============================================================
   Servidor Web para espectadores iniciado
   ============================================================
   Abre en tu celular/tablet: http://192.168.1.100:8080
   ============================================================
   ```

4. **Anota la IP local** (ejemplo: `192.168.1.100`) - la necesitarás para conectar espectadores

### 2. Conectar Espectadores desde Móviles/Tablets

#### Método Web (Recomendado para móviles)

1. En tu celular/tablet, abre el **navegador web**

2. Escribe la URL que apareció en la consola del servidor:
   ```
   http://192.168.1.100:8080
   ```
   *(Reemplaza `192.168.1.100` con la IP que apareció en tu consola)*

3. Verás la pantalla **"Bingacho Espectador"**

4. Toca el botón **"Conectar"**

5. ¡Listo! Ahora verás el tablero del host y escucharás los números cantados

**Nota:** En la primera conexión, el navegador puede pedir permiso para reproducir audio automáticamente. Acepta para escuchar los números.

### 3. Conectar Espectadores desde Computadoras (Python)

Si prefieres usar una computadora como espectador:

1. Asegúrate de tener Python 3 y pygame instalados:
   ```bash
   pip3 install pygame websockets
   ```

2. Ejecuta el cliente espectador:
   ```bash
   python3 spectator_client.py
   ```

3. Cuando te lo pida, ingresa la URL del servidor:
   ```
   ws://192.168.1.100:8765
   ```

4. Ingresa un nombre (opcional) o presiona Enter

5. Se abrirá una ventana mostrando el tablero del host

## Solución de Problemas

### No puedo conectar desde mi celular

1. **Verifica que ambos dispositivos estén en la misma red WiFi**
   - Host y celular deben estar en la misma red
   - Revisa la configuración de WiFi de ambos dispositivos

2. **Verifica la IP del servidor**
   - La IP mostrada en la consola debe coincidir con la que usas en el celular
   - Prueba hacer ping desde el celular a esa IP

3. **Desactiva temporalmente el firewall** (solo para probar)
   - En macOS: Preferencias del Sistema > Seguridad y privacidad > Cortafuegos
   - En Windows: Panel de control > Firewall de Windows

4. **Verifica que los puertos estén disponibles**
   - Puerto 8765 (WebSocket)
   - Puerto 8080 (HTTP)

### El audio no se reproduce

1. **En navegadores móviles:**
   - Asegúrate de tocar el botón "Conectar" (requerido para habilitar audio)
   - Verifica que el volumen del dispositivo no esté en silencio
   - Revisa que el navegador tenga permiso para reproducir audio

2. **El navegador bloqueó la reproducción automática:**
   - Toca la pantalla una vez después de conectar
   - Recarga la página y vuelve a conectar

### La imagen se ve lenta o con lag

Esto es normal. El modo espectador envía frames cada ~0.6 segundos para no saturar la red. Si necesitas mejor calidad:

- Reduce el intervalo en `multiplayer_manager.py` línea con `set_server_screen(screen, interval=0.6)`
- Cambia `interval=0.6` a `interval=0.3` para más fps (usa más ancho de banda)

### Error "Connection refused" o "No se pudo conectar"

1. Verifica que el **host haya iniciado correctamente** el modo servidor
2. Comprueba que la **IP sea correcta**
3. Asegúrate de estar usando el **protocolo correcto**:
   - Navegador web: `http://IP:8080`
   - Cliente Python: `ws://IP:8765`

## Características Técnicas

### Arquitectura

```
┌──────────────┐
│     HOST     │ (Ejecuta main.py en modo Servidor)
│  (Servidor)  │
└──────┬───────┘
       │
       ├─── Puerto 8765 (WebSocket) ──┐
       │                               │
       └─── Puerto 8080 (HTTP) ────┐  │
                                    │  │
       ┌────────────────────────────┘  │
       │                               │
       ▼                               ▼
┌─────────────┐               ┌─────────────┐
│  ESPECTADOR │               │  ESPECTADOR │
│  (Navegador)│               │   (Python)  │
└─────────────┘               └─────────────┘
```

### Datos Transmitidos

1. **Frames de pantalla**: PNG codificado en base64, enviado cada ~0.6s
2. **Audio de números**: WAV codificado en base64, enviado cuando se sortea un número
3. **Estado del juego**: JSON con números sorteados, jugadores conectados, etc.

### Consumo de Ancho de Banda (estimado)

- **Por espectador web:** ~50-150 KB/s (depende de la resolución y frecuencia)
- **Audio por número:** ~100-200 KB por número cantado
- **Total estimado:** ~1-2 MB/minuto por espectador

## Preguntas Frecuentes

**¿Cuántos espectadores pueden conectarse?**
No hay límite técnico, pero el rendimiento depende de tu red. En redes domésticas típicas, 5-10 espectadores funcionan sin problemas.

**¿Funciona fuera de mi casa?**
No directamente. Necesitas configurar port forwarding en tu router o usar servicios como ngrok. El modo espectador está diseñado para uso en red local.

**¿Los espectadores pueden hacer trampa?**
Los espectadores solo ven lo que el host ve. No pueden controlar el juego ni sortear números.

**¿Puedo usar esto para transmitir por streaming?**
Sí, pero este sistema es básico. Para streaming profesional considera usar OBS + YouTube/Twitch.

## Soporte

Si encuentras problemas, revisa:
1. Que ambos dispositivos estén en la misma red
2. Que el firewall permita las conexiones
3. Que los puertos 8765 y 8080 estén disponibles

Para más información técnica, consulta el código en:
- `multiplayer_server.py` - Servidor WebSocket
- `multiplayer_manager.py` - Gestor de streaming
- `spectator_client.py` - Cliente Python
- `web/index.html` - Cliente web para móviles

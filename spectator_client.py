"""
Cliente espectador para conectarse al servidor y recibir la vista y audio del host.
Usa WebSockets para registrarse con role 'spectator' y muestra frames en una ventana pygame.
"""

import asyncio
import websockets
import json
import base64
import tempfile
import threading
import pygame
import os

class SpectatorClient:
    def __init__(self, server_url, nickname="spectator"):
        self.server_url = server_url
        self.nickname = nickname
        self.websocket = None
        self.loop = None
        self.thread = None
        self.connected = False
        self.running = False
        self.screen = None
        self.clock = None
        self.frame_surface = None

    async def connect_async(self):
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            # Enviar registro con role spectator
            register_message = {"type": "register", "nickname": self.nickname, "role": "spectator"}
            await self.websocket.send(json.dumps(register_message))
            print(f"Conectado al servidor como espectador {self.nickname}")
            await self.listen_messages()
        except Exception as e:
            print(f"Error conectando como espectador: {e}")
            self.connected = False

    async def listen_messages(self):
        try:
            async for message in self.websocket:
                # Mensaje puede ser JSON string
                try:
                    data = json.loads(message)
                except Exception:
                    # No es JSON string; ignorar
                    continue

                msg_type = data.get('type')
                if msg_type == 'spectator_frame':
                    await self.handle_frame_message(data)
                elif msg_type == 'spectator_audio':
                    await self.handle_audio_message(data)
                elif msg_type == 'game_state':
                    # Opcional: mostrar estado
                    pass
                elif msg_type == 'new_number':
                    # Opcional: mostrar número actual
                    pass

        except websockets.exceptions.ConnectionClosed:
            print("Conexión cerrada por el servidor")
            self.connected = False
        except Exception as e:
            print(f"Error en listen_messages: {e}")
            self.connected = False

    async def handle_frame_message(self, data):
        fmt = data.get('format')
        b64 = data.get('data')
        if not b64:
            return
        try:
            b = base64.b64decode(b64)
            # Guardar temporal y cargar con pygame
            with tempfile.NamedTemporaryFile(suffix='.'+fmt, delete=False) as tmp:
                tmp.write(b)
                tmp_path = tmp.name

            img = pygame.image.load(tmp_path)
            # Convertir al formato de pantalla
            self.frame_surface = pygame.transform.scale(img, (pygame.display.get_surface().get_size()))
            try:
                os.remove(tmp_path)
            except Exception:
                pass
        except Exception as e:
            print(f"Error procesando frame: {e}")

    async def handle_audio_message(self, data):
        fmt = data.get('format')
        b64 = data.get('data')
        if not b64:
            return
        try:
            b = base64.b64decode(b64)
            # Guardar temporal y reproducir con mixer
            with tempfile.NamedTemporaryFile(suffix='.'+fmt, delete=False) as tmp:
                tmp.write(b)
                tmp_path = tmp.name
            try:
                sound = pygame.mixer.Sound(tmp_path)
                sound.play()
            except Exception as e:
                print(f"Error reproduciendo audio temporal: {e}")
            # Optionally remove file after some time
        except Exception as e:
            print(f"Error procesando audio: {e}")

    def start(self):
        # Inicializar pygame ventana para mostrar frames
        pygame.init()
        pygame.mixer.init()
        info = pygame.display.Info()
        # Crear ventana con tamaño del config si disponible, otherwise use current display
        try:
            import config as cfg
            width, height = cfg.WIDTH, cfg.HEIGHT
        except Exception:
            width, height = info.current_w, info.current_h

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Bingacho - Espectador')
        self.clock = pygame.time.Clock()
        self.running = True

        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.connect_async())

        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()

        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                # Dibujar último frame si existe
                if self.frame_surface:
                    self.screen.blit(self.frame_surface, (0,0))
                else:
                    # Mostrar mensaje esperando frame
                    self.screen.fill((30,30,30))
                    font = pygame.font.SysFont(None, 36)
                    text = font.render('Esperando vista del host...', True, (200,200,200))
                    self.screen.blit(text, (20,20))

                pygame.display.flip()
                self.clock.tick(30)
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            try:
                if self.websocket:
                    asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)
            except Exception:
                pass
            pygame.quit()


if __name__ == '__main__':
    server_url = input('URL del servidor (ej: ws://192.168.1.100:8765): ')
    nickname = input('Tu nombre (opcional): ') or 'spectator'
    client = SpectatorClient(server_url, nickname)
    client.start()

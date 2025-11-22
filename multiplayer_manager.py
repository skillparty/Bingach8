"""
Gestor de modos multijugador
Coordina servidor, cliente y renderizado de cartillas
"""

import threading
import asyncio
import json
import base64
import tempfile
import time
import os
import queue
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiplayer_server import BingachoServer, get_server_instance
from multiplayer_client import BingachoClient, create_client, get_client_instance
from bingo_card import BingoCard, generate_unique_cards
from bingo_card_renderer import BingoCardRenderer

class MultiplayerManager:
    """Gestiona el modo multijugador del juego"""
    
    def __init__(self):
        self.mode = None  # "server", "client", None
        self.server = None
        self.client = None
        self.server_thread = None
        self.http_server = None
        self.http_thread = None
        self.http_port = 8080 # Puerto por defecto
        self.player_card = None  # Cartilla del jugador (solo en modo cliente)
        self.card_renderer = None  # Renderizador de la cartilla
        self.nickname = ""
        self.server_ip = ""
        self.is_active = False
        
        # Variables para streaming
        self._frame_queue = None
        self._streamer_thread = None
        self._last_frame_time = 0
        self._stream_interval = 0.05
        
    def start_server_mode(self, nickname, port=8765):
        """
        Inicia el modo servidor
        
        Args:
            nickname: Nickname del host
            port: Puerto del servidor
            
        Returns:
            True si se inició correctamente, False si hubo error
        """
        try:
            # Detener cualquier instancia previa
            self.stop()
            
            self.mode = "server"
            self.nickname = nickname
            self.server = get_server_instance()
            self.server.port = port
            
            # Iniciar servidor en un thread separado
            def run_server():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(self.server.start())
                except Exception as e:
                    print(f"Error en loop del servidor: {e}")
                finally:
                    loop.close()
            
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()

            # Esperar un momento para verificar si el servidor arrancó
            time.sleep(1.0)
            if not getattr(self.server, 'server', None):
                print("ADVERTENCIA: El servidor WS parece no haber arrancado correctamente (posible puerto en uso)")
                # No retornamos False aquí porque puede tardar un poco más, pero avisamos

            # Iniciar servidor HTTP para servir el cliente web
            self._start_http_server(port=8080)

            # If the caller provided a screen later via set_server_screen, a streamer thread
            # will be started from set_server_screen. This keeps start_server_mode minimal.
            
            self.is_active = True
            print(f"Modo servidor iniciado como '{nickname}' en puerto {port}")
            return True
            
        except Exception as e:
            print(f"Error iniciando servidor: {e}")
            return False
    
    def start_client_mode(self, nickname, server_ip, port=8765, screen=None, position=(50, 50)):
        """
        Inicia el modo cliente
        
        Args:
            nickname: Nickname del jugador
            server_ip: IP del servidor
            port: Puerto del servidor
            screen: Superficie de pygame para renderizar la cartilla
            position: Posición donde dibujar la cartilla
            
        Returns:
            True si se conectó correctamente, False si hubo error
        """
        try:
            self.mode = "client"
            self.nickname = nickname
            self.server_ip = server_ip
            
            # Crear URL del servidor
            server_url = f"ws://{server_ip}:{port}"
            
            # Crear cliente
            self.client = create_client(server_url, nickname)
            self.client.start_connection_thread()
            
            # Generar cartilla para el jugador
            self.player_card = BingoCard(card_id=nickname)
            
            # Crear renderizador si se proporcionó screen
            if screen:
                self.card_renderer = BingoCardRenderer(screen, self.player_card, position)
            
            self.is_active = True
            print(f"Modo cliente iniciado como '{nickname}', conectando a {server_url}")
            return True
            
        except Exception as e:
            print(f"Error iniciando cliente: {e}")
            return False
    
    def stop(self):
        """Detiene el modo multijugador actual"""
        if self.mode == "server" and self.server:
            # Detener servidor HTTP
            if self.http_server:
                try:
                    self.http_server.shutdown()
                    print("Servidor HTTP detenido")
                except:
                    pass
            
            # Detener servidor WebSocket
            if self.server:
                try:
                    if hasattr(self.server, 'loop') and self.server.loop and self.server.loop.is_running():
                        future = asyncio.run_coroutine_threadsafe(self.server.stop(), self.server.loop)
                        try:
                            future.result(timeout=2)
                        except:
                            pass
                except Exception as e:
                    print(f"Error deteniendo servidor WS: {e}")
            
            print("Servidor detenido")
            
        elif self.mode == "client" and self.client:
            # Desconectar cliente
            if self.client.loop:
                try:
                    asyncio.run_coroutine_threadsafe(
                        self.client.disconnect_async(),
                        self.client.loop
                    )
                except:
                    pass
            print("Cliente desconectado")
        
        self.mode = None
        self.is_active = False
    
    def send_number_to_clients(self, number):
        """
        Envía un número sorteado a todos los clientes (solo en modo servidor)
        
        Args:
            number: Número sorteado
        """
        if self.mode == "server" and self.server:
            # Ejecutar en el loop del servidor (si está disponible)
            if hasattr(self.server, 'loop') and self.server.loop:
                try:
                    async def send():
                        await self.server.handle_new_number(number)
                    asyncio.run_coroutine_threadsafe(send(), self.server.loop)
                except Exception as e:
                    print(f"Error enviando número a clientes: {e}")
            else:
                print("Advertencia: loop del servidor no disponible para enviar número")
    
    def send_game_start(self):
        """Envía señal de inicio de juego a los clientes (solo en modo servidor)"""
        if self.mode == "server" and self.server:
            try:
                async def send():
                    await self.server.handle_game_start()
                if hasattr(self.server, 'loop') and self.server.loop:
                    asyncio.run_coroutine_threadsafe(send(), self.server.loop)
            except Exception as e:
                print(f"Error enviando inicio de juego: {e}")
    
    def send_game_reset(self):
        """Envía señal de reinicio de juego a los clientes (solo en modo servidor)"""
        if self.mode == "server" and self.server:
            try:
                async def send():
                    await self.server.handle_game_reset()
                if hasattr(self.server, 'loop') and self.server.loop:
                    asyncio.run_coroutine_threadsafe(send(), self.server.loop)
            except Exception as e:
                print(f"Error enviando reinicio de juego: {e}")

    def set_server_screen(self, screen, interval=0.05):
        """
        Configura el streaming de pantalla.
        Nota: Ya no inicia un hilo que lee la pantalla directamente.
        El hilo principal debe llamar a broadcast_screen() periódicamente.
        """
        if not self.server:
            print("Servidor no inicializado: no se puede asociar la pantalla")
            return False

        self._stream_interval = interval
        self.start_streamer()
        print("Sistema de streaming configurado")
        return True

    def start_streamer(self):
        """Inicia el hilo que procesa y envía los frames desde la cola"""
        if self._streamer_thread and self._streamer_thread.is_alive():
            return

        self._frame_queue = queue.Queue(maxsize=2)
        
        def streamer_worker():
            frame_count = 0
            while self.mode == 'server':
                try:
                    # Bloquea hasta que haya un frame (timeout para poder salir si se detiene el servidor)
                    frame_surface = self._frame_queue.get(timeout=1.0)
                    
                    try:
                        import pygame as _pygame
                        
                        # Escalar imagen para mejorar rendimiento (ancho objetivo: 800px)
                        target_width = 800
                        current_w = frame_surface.get_width()
                        current_h = frame_surface.get_height()
                        
                        if current_w > target_width:
                            ratio = target_width / current_w
                            target_height = int(current_h * ratio)
                            # Escalar en el worker thread es seguro porque frame_surface es una copia
                            frame_surface = _pygame.transform.scale(frame_surface, (target_width, target_height))

                        # Guardar a JPG
                        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                            tmp_path = tmp.name
                            try:
                                _pygame.image.save(frame_surface, tmp_path)
                            except Exception as e:
                                print(f"Error guardando frame: {e}")
                                self._frame_queue.task_done()
                                continue

                        # Leer y enviar
                        with open(tmp_path, 'rb') as f:
                            b = f.read()
                        try:
                            os.remove(tmp_path)
                        except Exception:
                            pass

                        payload = {
                            'type': 'spectator_frame',
                            'format': 'jpg',
                            'data': base64.b64encode(b).decode('ascii')
                        }

                        if hasattr(self.server, 'loop') and self.server.loop:
                            async def send():
                                await self.server.broadcast_message_filtered(payload, role_filter='spectator')
                            asyncio.run_coroutine_threadsafe(send(), self.server.loop)
                            
                            frame_count += 1
                            if frame_count % 100 == 0:
                                print(f"Streamer: {frame_count} frames enviados")
                                
                    except Exception as e:
                        print(f"Error procesando frame: {e}")
                    finally:
                        self._frame_queue.task_done()
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error en worker streamer: {e}")

        self._streamer_thread = threading.Thread(target=streamer_worker, daemon=True)
        self._streamer_thread.start()

    def broadcast_screen(self, screen):
        """
        Captura y encola la pantalla actual. 
        DEBE llamarse desde el hilo principal (bucle de juego).
        """
        if not self.is_server_mode() or not self._streamer_thread:
            return

        current_time = time.time()
        if current_time - self._last_frame_time < self._stream_interval:
            return

        self._last_frame_time = current_time
        
        try:
            # Copia segura en el hilo principal
            # Usamos copy() para crear una superficie independiente que el worker pueda usar
            frame_copy = screen.copy()
            
            # Intentar poner en la cola, si está llena descartamos para no bloquear el juego
            try:
                self._frame_queue.put_nowait(frame_copy)
            except queue.Full:
                pass
        except Exception as e:
            print(f"Error capturando pantalla: {e}")

    def _start_http_server(self, port=8080):
        """Inicia un servidor HTTP simple para servir el cliente web"""
        try:
            import os
            
            # Cambiar al directorio web para servir archivos
            web_dir = os.path.join(os.path.dirname(__file__), 'web')
            manager_instance = self
            
            class CustomHandler(SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=web_dir, **kwargs)
                
                def log_message(self, format, *args):
                    # Suprimir logs HTTP para no saturar consola
                    pass

                def do_GET(self):
                    if self.path == '/config.json':
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        # Añadir headers para evitar caché
                        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
                        self.end_headers()
                        
                        # Obtener el puerto WS actual del servidor
                        ws_port = manager_instance.server.port if manager_instance.server else 8765
                        
                        response = json.dumps({"ws_port": ws_port})
                        self.wfile.write(response.encode('utf-8'))
                    else:
                        super().do_GET()
            
            def run_http():
                # Intentar varios puertos si el 8080 está ocupado
                current_port = port
                max_attempts = 10
                
                for i in range(max_attempts):
                    try:
                        self.http_server = HTTPServer(('0.0.0.0', current_port), CustomHandler)
                        self.http_port = current_port  # Guardar el puerto real
                        
                        local_ip = self.server.get_local_ip() if self.server else 'localhost'
                        print(f"\n{'='*60}")
                        print(f"Servidor Web para espectadores iniciado")
                        print(f"{'='*60}")
                        print(f"Abre en tu celular/tablet: http://{local_ip}:{current_port}")
                        print(f"{'='*60}\n")
                        
                        self.http_server.serve_forever()
                        break
                    except OSError as e:
                        if e.errno == 48: # Address already in use
                            print(f"Puerto HTTP {current_port} ocupado, probando siguiente...")
                            current_port += 1
                        else:
                            raise e
            
            self.http_thread = threading.Thread(target=run_http, daemon=True)
            self.http_thread.start()
            
        except Exception as e:
            print(f"Error iniciando servidor HTTP: {e}")
    
    def update(self):
        """Actualiza el estado del multiplayer (procesa mensajes del cliente)"""
        if self.mode == "client" and self.client:
            # Procesar mensajes recibidos
            messages = self.client.get_messages()
            
            for msg in messages:
                msg_type = msg.get("type")
                
                if msg_type == "new_number":
                    # Nuevo número sorteado, marcar en la cartilla
                    number = msg["number"]
                    if self.player_card:
                        was_marked = self.player_card.mark_number(number)
                        if was_marked:
                            print(f"¡Número {number} marcado en tu cartilla!")
                            
                            # Verificar si hay línea o bingo
                            if self.player_card.check_bingo():
                                print("¡¡¡BINGO!!!")
                            elif self.player_card.check_line():
                                print("¡LÍNEA!")
                
                elif msg_type == "game_reset":
                    # Reiniciar cartilla
                    if self.player_card:
                        self.player_card.marked.clear()
                        print("Juego reiniciado, cartilla limpiada")
    
    def draw_card(self, screen):
        """Dibuja la cartilla del jugador (solo en modo cliente)"""
        if self.mode == "client" and self.card_renderer:
            self.card_renderer.draw(show_marked=True, highlight_current=True)
            
            # Mostrar estadísticas
            stats_y = self.card_renderer.position[1] + self.card_renderer.card_height + 10
            self.card_renderer.draw_stats((self.card_renderer.position[0], stats_y))
    
    def get_connection_status(self):
        """
        Obtiene el estado de la conexión
        
        Returns:
            Diccionario con información del estado
        """
        if self.mode == "server":
            local_ip = self.server.get_local_ip() if self.server else "N/A"
            return {
                "mode": "server",
                "active": self.is_active,
                "nickname": self.nickname,
                "connected_clients": len(self.server.clients) if self.server else 0,
                "ip": local_ip,
                "http_url": f"http://{local_ip}:{self.http_port}" if self.http_server else "Iniciando..."
            }
        elif self.mode == "client":
            return {
                "mode": "client",
                "active": self.is_active,
                "nickname": self.nickname,
                "connected": self.client.is_connected() if self.client else False,
                "server_ip": self.server_ip,
                "game_started": self.client.game_started if self.client else False,
                "total_players": self.client.total_players if self.client else 0
            }
        else:
            return {
                "mode": None,
                "active": False
            }
    
    def is_server_mode(self):
        """Verifica si está en modo servidor"""
        return self.mode == "server"
    
    def is_client_mode(self):
        """Verifica si está en modo cliente"""
        return self.mode == "client"
    
    def is_local_mode(self):
        """Verifica si está en modo local (no multijugador)"""
        return self.mode is None


# Instancia global del gestor
_multiplayer_manager = None

def get_multiplayer_manager():
    """Obtiene la instancia global del gestor multijugador"""
    global _multiplayer_manager
    if _multiplayer_manager is None:
        _multiplayer_manager = MultiplayerManager()
    return _multiplayer_manager

def reset_multiplayer_manager():
    """Reinicia el gestor multijugador"""
    global _multiplayer_manager
    if _multiplayer_manager:
        _multiplayer_manager.stop()
    _multiplayer_manager = None

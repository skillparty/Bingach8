"""
Gestor de modos multijugador
Coordina servidor, cliente y renderizado de cartillas
"""

import threading
import asyncio
import json
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
        self.player_card = None  # Cartilla del jugador (solo en modo cliente)
        self.card_renderer = None  # Renderizador de la cartilla
        self.nickname = ""
        self.server_ip = ""
        self.is_active = False
        
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
            self.mode = "server"
            self.nickname = nickname
            self.server = get_server_instance()
            self.server.port = port
            
            # Iniciar servidor en un thread separado
            def run_server():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.server.start())
            
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            
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
            # Detener servidor
            if self.server_thread and self.server_thread.is_alive():
                # El servidor se detendrá cuando termine el programa
                pass
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
            # Ejecutar en el loop del servidor
            if self.server_thread and self.server_thread.is_alive():
                try:
                    # Crear una coroutine para enviar el número
                    async def send():
                        await self.server.handle_new_number(number)
                    
                    # Obtener el loop del servidor y ejecutar
                    # Como el servidor está en otro thread, necesitamos hacer esto de forma thread-safe
                    asyncio.run_coroutine_threadsafe(send(), asyncio.get_event_loop())
                except Exception as e:
                    print(f"Error enviando número a clientes: {e}")
    
    def send_game_start(self):
        """Envía señal de inicio de juego a los clientes (solo en modo servidor)"""
        if self.mode == "server" and self.server:
            try:
                async def send():
                    await self.server.handle_game_start()
                
                asyncio.run_coroutine_threadsafe(send(), asyncio.get_event_loop())
            except Exception as e:
                print(f"Error enviando inicio de juego: {e}")
    
    def send_game_reset(self):
        """Envía señal de reinicio de juego a los clientes (solo en modo servidor)"""
        if self.mode == "server" and self.server:
            try:
                async def send():
                    await self.server.handle_game_reset()
                
                asyncio.run_coroutine_threadsafe(send(), asyncio.get_event_loop())
            except Exception as e:
                print(f"Error enviando reinicio de juego: {e}")
    
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
            return {
                "mode": "server",
                "active": self.is_active,
                "nickname": self.nickname,
                "connected_clients": len(self.server.clients) if self.server else 0,
                "ip": self.server.get_local_ip() if self.server else "N/A"
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

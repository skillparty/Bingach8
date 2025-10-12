"""
Cliente WebSocket para el modo multijugador de Bingacho
El cliente se conecta al servidor, recibe números y gestiona la cartilla
"""

import asyncio
import websockets
import json
import threading
from queue import Queue

class BingachoClient:
    """Cliente para conectarse a partidas multijugador de Bingacho"""
    
    def __init__(self, server_url, nickname):
        """
        Inicializa el cliente
        
        Args:
            server_url: URL del servidor WebSocket (ej: ws://192.168.1.100:8765)
            nickname: Nickname del jugador
        """
        self.server_url = server_url
        self.nickname = nickname
        self.websocket = None
        self.connected = False
        self.message_queue = Queue()  # Cola para mensajes recibidos
        self.loop = None
        self.thread = None
        
        # Estado del juego
        self.game_started = False
        self.drawn_numbers = []
        self.current_number = None
        self.total_players = 0
    
    async def connect_async(self):
        """Conecta al servidor de forma asíncrona"""
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            
            # Enviar mensaje de registro
            register_message = {
                "type": "register",
                "nickname": self.nickname
            }
            await self.websocket.send(json.dumps(register_message))
            
            print(f"Conectado al servidor como {self.nickname}")
            
            # Iniciar escucha de mensajes
            await self.listen_messages()
            
        except Exception as e:
            print(f"Error conectando al servidor: {e}")
            self.connected = False
    
    async def listen_messages(self):
        """Escucha mensajes del servidor"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                
                # Poner el mensaje en la cola para procesarlo en el thread principal
                self.message_queue.put(data)
                
                # Procesar mensaje en el thread async
                await self.handle_message(data)
                
        except websockets.exceptions.ConnectionClosed:
            print("Conexión cerrada por el servidor")
            self.connected = False
        except Exception as e:
            print(f"Error recibiendo mensaje: {e}")
            self.connected = False
    
    async def handle_message(self, data):
        """
        Procesa un mensaje del servidor
        
        Args:
            data: Diccionario con los datos del mensaje
        """
        msg_type = data.get("type")
        
        if msg_type == "game_state":
            # Estado inicial del juego
            self.game_started = data["game_started"]
            self.drawn_numbers = data["drawn_numbers"]
            self.current_number = data["current_number"]
            self.total_players = data["total_players"]
            print(f"Estado del juego recibido: {len(self.drawn_numbers)} números sorteados")
            
        elif msg_type == "new_number":
            # Nuevo número sorteado
            self.current_number = data["number"]
            self.drawn_numbers = data["drawn_numbers"]
            print(f"Nuevo número: {self.current_number}")
            
        elif msg_type == "game_started":
            # Juego iniciado
            self.game_started = True
            print("Juego iniciado")
            
        elif msg_type == "game_reset":
            # Juego reiniciado
            self.game_started = False
            self.drawn_numbers = []
            self.current_number = None
            print("Juego reiniciado")
            
        elif msg_type == "player_joined":
            # Nuevo jugador
            self.total_players = data["total_players"]
            print(f"Jugador {data['nickname']} se unió ({self.total_players} jugadores)")
            
        elif msg_type == "player_left":
            # Jugador se fue
            self.total_players = data["total_players"]
            print(f"Jugador {data['nickname']} se fue ({self.total_players} jugadores)")
    
    async def send_message_async(self, message):
        """
        Envía un mensaje al servidor
        
        Args:
            message: Diccionario con el mensaje
        """
        if self.connected and self.websocket:
            try:
                await self.websocket.send(json.dumps(message))
            except Exception as e:
                print(f"Error enviando mensaje: {e}")
    
    async def disconnect_async(self):
        """Desconecta del servidor"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            print("Desconectado del servidor")
    
    def start_connection_thread(self):
        """Inicia el cliente en un thread separado"""
        def run_async_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.connect_async())
        
        self.thread = threading.Thread(target=run_async_loop, daemon=True)
        self.thread.start()
    
    def get_messages(self):
        """
        Obtiene todos los mensajes pendientes de la cola
        
        Returns:
            Lista de mensajes
        """
        messages = []
        while not self.message_queue.empty():
            messages.append(self.message_queue.get())
        return messages
    
    def is_connected(self):
        """Verifica si está conectado"""
        return self.connected
    
    def get_game_state(self):
        """
        Obtiene el estado actual del juego
        
        Returns:
            Diccionario con el estado del juego
        """
        return {
            "game_started": self.game_started,
            "drawn_numbers": self.drawn_numbers,
            "current_number": self.current_number,
            "total_players": self.total_players
        }


# Variable global para el cliente
_client_instance = None

def get_client_instance():
    """Obtiene la instancia singleton del cliente"""
    global _client_instance
    return _client_instance

def create_client(server_url, nickname):
    """
    Crea una nueva instancia del cliente
    
    Args:
        server_url: URL del servidor
        nickname: Nickname del jugador
        
    Returns:
        Instancia del cliente
    """
    global _client_instance
    _client_instance = BingachoClient(server_url, nickname)
    return _client_instance

def disconnect_client():
    """Desconecta el cliente actual"""
    global _client_instance
    if _client_instance:
        if _client_instance.loop:
            asyncio.run_coroutine_threadsafe(
                _client_instance.disconnect_async(),
                _client_instance.loop
            )
        _client_instance = None


if __name__ == "__main__":
    # Test del cliente
    import time
    
    print("=== Test del cliente ===")
    server_url = input("URL del servidor (ej: ws://192.168.1.100:8765): ")
    nickname = input("Tu nickname: ")
    
    client = create_client(server_url, nickname)
    client.start_connection_thread()
    
    print("\nEsperando conexión...")
    time.sleep(2)
    
    if client.is_connected():
        print("Conectado exitosamente")
        print("\nEscuchando mensajes... (Ctrl+C para salir)")
        
        try:
            while True:
                messages = client.get_messages()
                for msg in messages:
                    print(f"Mensaje: {msg}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDesconectando...")
            disconnect_client()
    else:
        print("No se pudo conectar al servidor")

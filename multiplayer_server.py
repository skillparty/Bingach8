"""
Servidor WebSocket para el modo multijugador de Bingacho
El servidor gestiona la partida, distribuye números y sincroniza con los clientes
"""

import asyncio
import websockets
import json
import socket
from datetime import datetime

class BingachoServer:
    """Servidor para gestionar partidas multijugador de Bingacho"""
    
    def __init__(self, host='0.0.0.0', port=8765):
        """
        Inicializa el servidor
        
        Args:
            host: Dirección IP del servidor (0.0.0.0 para todas las interfaces)
            port: Puerto del servidor
        """
        self.host = host
        self.port = port
        self.clients = {}  # {websocket: {"nickname": str, "connected_at": datetime}}
        self.drawn_numbers = []  # Números sorteados en orden
        self.current_number = None  # Número actual
        self.game_started = False
        self.server = None
        
    def get_local_ip(self):
        """Obtiene la IP local del servidor"""
        try:
            # Crear un socket y conectarse a una dirección externa
            # No se envía nada, solo se usa para obtener la IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "localhost"
    
    async def register_client(self, websocket, nickname):
        """
        Registra un nuevo cliente
        
        Args:
            websocket: Conexión WebSocket del cliente
            nickname: Nickname del cliente
        """
        self.clients[websocket] = {
            "nickname": nickname,
            "connected_at": datetime.now()
        }
        
        print(f"Cliente conectado: {nickname} ({len(self.clients)} clientes totales)")
        
        # Enviar estado actual del juego al nuevo cliente
        await self.send_game_state(websocket)
        
        # Notificar a todos los clientes sobre el nuevo jugador
        await self.broadcast_message({
            "type": "player_joined",
            "nickname": nickname,
            "total_players": len(self.clients)
        })
    
    async def unregister_client(self, websocket):
        """
        Desregistra un cliente
        
        Args:
            websocket: Conexión WebSocket del cliente
        """
        if websocket in self.clients:
            nickname = self.clients[websocket]["nickname"]
            del self.clients[websocket]
            print(f"Cliente desconectado: {nickname} ({len(self.clients)} clientes restantes)")
            
            # Notificar a todos los clientes
            await self.broadcast_message({
                "type": "player_left",
                "nickname": nickname,
                "total_players": len(self.clients)
            })
    
    async def send_game_state(self, websocket):
        """
        Envía el estado actual del juego a un cliente específico
        
        Args:
            websocket: Conexión WebSocket del cliente
        """
        state = {
            "type": "game_state",
            "game_started": self.game_started,
            "drawn_numbers": self.drawn_numbers,
            "current_number": self.current_number,
            "total_players": len(self.clients)
        }
        await websocket.send(json.dumps(state))
    
    async def broadcast_message(self, message, exclude=None):
        """
        Envía un mensaje a todos los clientes conectados
        
        Args:
            message: Diccionario con el mensaje a enviar
            exclude: WebSocket a excluir (opcional)
        """
        if self.clients:
            message_json = json.dumps(message)
            # Enviar a todos los clientes excepto el excluido
            websockets_to_send = [
                ws for ws in self.clients.keys() 
                if ws != exclude
            ]
            
            # Usar gather para enviar a todos simultáneamente
            if websockets_to_send:
                await asyncio.gather(
                    *[ws.send(message_json) for ws in websockets_to_send],
                    return_exceptions=True
                )
    
    async def handle_new_number(self, number):
        """
        Maneja un nuevo número sorteado
        
        Args:
            number: Número sorteado
        """
        self.current_number = number
        if number not in self.drawn_numbers:
            self.drawn_numbers.append(number)
        
        # Broadcast a todos los clientes
        await self.broadcast_message({
            "type": "new_number",
            "number": number,
            "drawn_numbers": self.drawn_numbers
        })
        
        print(f"Número sorteado: {number}")
    
    async def handle_game_start(self):
        """Maneja el inicio del juego"""
        self.game_started = True
        await self.broadcast_message({
            "type": "game_started"
        })
        print("Juego iniciado")
    
    async def handle_game_reset(self):
        """Maneja el reinicio del juego"""
        self.game_started = False
        self.drawn_numbers = []
        self.current_number = None
        
        await self.broadcast_message({
            "type": "game_reset"
        })
        print("Juego reiniciado")
    
    async def handle_client(self, websocket, path):
        """
        Maneja la conexión de un cliente
        
        Args:
            websocket: Conexión WebSocket
            path: Ruta de la conexión
        """
        try:
            # Esperar mensaje de registro del cliente
            async for message in websocket:
                data = json.loads(message)
                
                # Primer mensaje debe ser el registro
                if websocket not in self.clients:
                    if data["type"] == "register":
                        await self.register_client(websocket, data["nickname"])
                    continue
                
                # Manejar diferentes tipos de mensajes
                msg_type = data.get("type")
                
                if msg_type == "new_number":
                    await self.handle_new_number(data["number"])
                elif msg_type == "game_start":
                    await self.handle_game_start()
                elif msg_type == "game_reset":
                    await self.handle_game_reset()
                elif msg_type == "ping":
                    # Responder con pong
                    await websocket.send(json.dumps({"type": "pong"}))
                
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Error en cliente: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def start(self):
        """Inicia el servidor"""
        try:
            self.server = await websockets.serve(
                self.handle_client,
                self.host,
                self.port
            )
            
            local_ip = self.get_local_ip()
            print(f"\n{'='*60}")
            print(f"Servidor Bingacho iniciado")
            print(f"{'='*60}")
            print(f"IP Local: {local_ip}")
            print(f"Puerto: {self.port}")
            print(f"Los clientes deben conectarse a: ws://{local_ip}:{self.port}")
            print(f"{'='*60}\n")
            
            # Mantener el servidor corriendo
            await asyncio.Future()  # Run forever
            
        except Exception as e:
            print(f"Error iniciando servidor: {e}")
    
    async def stop(self):
        """Detiene el servidor"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("Servidor detenido")


# Variable global para el servidor
_server_instance = None

def get_server_instance():
    """Obtiene la instancia singleton del servidor"""
    global _server_instance
    if _server_instance is None:
        _server_instance = BingachoServer()
    return _server_instance


async def start_server_async(port=8765):
    """
    Inicia el servidor de forma asíncrona
    
    Args:
        port: Puerto del servidor
    """
    server = get_server_instance()
    server.port = port
    await server.start()


def run_server(port=8765):
    """
    Inicia el servidor en un nuevo event loop
    
    Args:
        port: Puerto del servidor
    """
    asyncio.run(start_server_async(port))


if __name__ == "__main__":
    # Test del servidor
    print("Iniciando servidor de prueba...")
    run_server()

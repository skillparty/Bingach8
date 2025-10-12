# Guía Rápida de Instalación y Uso - Bingacho Multijugador

## 🚀 Instalación Rápida

### Paso 1: Instalar Dependencias

```bash
cd /Users/alejandrorollano/Bingacho
pip install -r requirements.txt
```

### Paso 2: Verificar Instalación

```bash
python test_multiplayer.py
```

Deberías ver algo como:
```
RESUMEN DE TESTS
====================================================
Cartillas de Bingo........................ ✅ PASADO
Servidor................................... ✅ PASADO
Cliente.................................... ✅ PASADO
Gestor..................................... ✅ PASADO
Selector de Modo........................... ✅ PASADO
Renderizador............................... ✅ PASADO

RESULTADO FINAL: 6/6 tests pasados
====================================================

🎉 ¡Todos los tests pasaron! El sistema está listo.
```

### Paso 3: Iniciar el Juego

```bash
python main.py
```

## 🎮 Uso Rápido

### Opción 1: Jugar Solo (Modo Local)

1. Ejecuta `python main.py`
2. Click en "INICIAR JUEGO" en la pantalla de título
3. Selecciona "MODO LOCAL"
4. ¡A jugar!

### Opción 2: Jugar en Red - TÚ COMO HOST

**En tu laptop (servidor):**

1. Ejecuta `python main.py`
2. Click en "INICIAR JUEGO"
3. Selecciona "CREAR PARTIDA (SERVIDOR)"
4. Ingresa tu nombre (ej: "Alejandro")
5. Click en "INICIAR"
6. **IMPORTANTE:** Anota la IP que aparece en pantalla
   - Ejemplo: `Servidor: Alejandro | IP: 192.168.1.100 | Clientes: 0`
7. Comparte esta IP con los demás jugadores
8. Cuando todos estén conectados, presiona "INICIAR JUEGO"
9. Sortea números con el botón "SIGUIENTE NÚMERO"

**En las computadoras de los demás (clientes):**

1. Ejecuta `python main.py`
2. Click en "INICIAR JUEGO"
3. Selecciona "UNIRSE A PARTIDA"
4. Ingresa su nombre (ej: "Jose", "Maria", etc.)
5. Ingresa la IP del servidor: `192.168.1.100`
6. Click en "INICIAR"
7. ¡Listo! Verán su cartilla y el tablero
8. Los números se marcarán automáticamente

## 📱 Ejemplo de Uso en Casa

### Escenario: Familia de 4 personas

**Setup:**
- 1 Laptop (Host/Servidor) - Alejandro
- 3 Tablets/Laptops (Clientes) - Jose, Maria, Pedro
- Todos conectados al mismo Wi-Fi

**Paso a paso:**

1. **Alejandro (Host):**
   ```
   1. Abre el juego en su laptop
   2. Modo: "CREAR PARTIDA (SERVIDOR)"
   3. Nickname: "Alejandro"
   4. Ve en pantalla: IP: 192.168.1.100
   5. Les dice a todos: "Conéctense a 192.168.1.100"
   ```

2. **Jose (Cliente 1):**
   ```
   1. Abre el juego en su tablet
   2. Modo: "UNIRSE A PARTIDA"
   3. Nickname: "Jose"
   4. IP: 192.168.1.100
   5. Ve su cartilla generada automáticamente
   ```

3. **Maria (Cliente 2):**
   ```
   1. Abre el juego en su laptop
   2. Modo: "UNIRSE A PARTIDA"
   3. Nickname: "Maria"
   4. IP: 192.168.1.100
   5. Ve su cartilla generada automáticamente
   ```

4. **Pedro (Cliente 3):**
   ```
   1. Abre el juego en su tablet
   2. Modo: "UNIRSE A PARTIDA"
   3. Nickname: "Pedro"
   4. IP: 192.168.1.100
   5. Ve su cartilla generada automáticamente
   ```

5. **Alejandro (Host) ve en pantalla:**
   ```
   Servidor: Alejandro | IP: 192.168.1.100 | Clientes: 3
   ```

6. **Alejandro presiona "INICIAR JUEGO" y empieza a sortear números**

7. **Todos los clientes:**
   - Ven el tablero actualizarse
   - Sus cartillas se marcan automáticamente
   - Cuando hacen línea, ven "¡LÍNEA!"
   - Cuando hacen bingo, ven "¡¡¡BINGO!!!"

## 🔧 Solución de Problemas Comunes

### "No se pudo conectar al servidor"

**Soluciones:**
1. Verifica que todos estén en la misma red Wi-Fi
2. Verifica que la IP sea correcta
3. En el servidor, verifica el firewall:
   ```bash
   # macOS: Permitir conexiones entrantes para Python
   # Ve a Preferencias del Sistema > Seguridad > Firewall
   ```

### "Error iniciando servidor"

**Soluciones:**
1. Cierra otras instancias del juego
2. El puerto 8765 puede estar en uso
3. Reinicia tu computadora

### La cartilla no se marca

**Soluciones:**
1. Verifica que estés conectado (arriba dice "Conectado")
2. El número debe estar en tu cartilla
3. Si dice "Desconectado", cierra y vuelve a conectar

## 📚 Archivos Importantes

- **`main.py`**: Archivo principal del juego
- **`MODO_MULTIJUGADOR.md`**: Manual completo
- **`IMPLEMENTACION_MULTIJUGADOR.md`**: Detalles técnicos
- **`test_multiplayer.py`**: Tests de verificación
- **`requirements.txt`**: Dependencias

## 🎯 Controles del Juego

### Modo Local y Modo Servidor (Host)
- **Click en "INICIAR JUEGO"**: Sortea primer número
- **Click en "SIGUIENTE NÚMERO"**: Sortea siguiente número
- **ESPACIO**: Sortea siguiente número (atajo de teclado rápido) ⌨️
- **Click en "REINICIAR"**: Reinicia la partida
- **ESC**: Salir del juego

### Modo Cliente (Jugador)
- **Click en "BINGO"**: Muestra animación (decorativo)
- **ESC**: Salir del juego
- *Los números se marcan automáticamente*
- *No puedes sortear números con ESPACIO (solo el servidor)*

## ⚡ Tips Rápidos

1. **Conectividad:**
   - Todos deben estar en la MISMA red Wi-Fi
   - Anota bien la IP del servidor
   - La IP suele ser 192.168.1.XXX o 10.0.0.XXX

2. **Para el Host:**
   - Espera a que todos se conecten antes de iniciar
   - Puedes ver cuántos clientes están conectados arriba
   - Sortea a tu ritmo con "SIGUIENTE NÚMERO"

3. **Para los Clientes:**
   - Tu cartilla es única y aleatoria
   - No puedes sortear números (solo el host)
   - Puedes ver todo sincronizado en tiempo real

## 🎨 Interfaz

### Vista del Servidor (Host)
```
┌─────────────────────────────────────────────────────┐
│ Servidor: Alejandro | IP: 192.168.1.100 | Clientes: 3│
├─────────────────────────────────────────────────────┤
│                                                      │
│  [NÚMERO ACTUAL]    [TABLERO 90 NÚM]   [HISTORIAL] │
│                                                      │
│  [INICIAR] [SIGUIENTE]        [REINICIAR]  [BINGO] │
└─────────────────────────────────────────────────────┘
```

### Vista del Cliente (Jugador)
```
┌─────────────────────────────────────────────────────┐
│ Conectado: Jose | Jugadores: 4                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  [TU CARTILLA]  [TABLERO]           [HISTORIAL]    │
│                                                      │
│  Marcados: 8/15                                     │
│  [BINGO]                                            │
└─────────────────────────────────────────────────────┘
```

## 🆘 Soporte

Si tienes problemas:

1. **Verifica que los tests pasen:**
   ```bash
   python test_multiplayer.py
   ```

2. **Revisa los documentos:**
   - `MODO_MULTIJUGADOR.md` - Manual completo
   - `IMPLEMENTACION_MULTIJUGADOR.md` - Detalles técnicos

3. **Verifica tu red:**
   ```bash
   # En el servidor, obtén tu IP:
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Desde un cliente, prueba conectividad:
   ping [IP_DEL_SERVIDOR]
   ```

---

## ✅ Checklist de Inicio Rápido

- [ ] Instalé las dependencias: `pip install -r requirements.txt`
- [ ] Corrí los tests: `python test_multiplayer.py`
- [ ] Todos los tests pasaron (6/6)
- [ ] Todos los dispositivos están en la misma red Wi-Fi
- [ ] El servidor está corriendo y veo la IP
- [ ] Los clientes se conectaron exitosamente
- [ ] ¡Estoy listo para jugar!

---

**¡Disfruta tu juego de Bingacho multijugador! 🎉**

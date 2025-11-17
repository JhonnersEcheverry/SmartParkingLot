# 🚗 Simulador de Parqueadero Inteligente

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OS](https://img.shields.io/badge/OS-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com)

> Demostración educativa de conceptos de Sistemas Operativos: concurrencia, semáforos, locks y threads implementados en Python con interfaz gráfica Tkinter.

---

## 📋 Descripción

El **Simulador de Parqueadero Inteligente** es una aplicación educativa que modela vehículos (threads) compitiendo por espacios limitados de estacionamiento (recursos compartidos). El sistema utiliza primitivas de sincronización del módulo `threading` de Python para demostrar cómo un Sistema Operativo gestiona procesos concurrentes.

### Analogía con Sistemas Operativos

| Concepto de Parqueadero | Concepto de SO |
|------------------------|----------------|
| 🚗 Vehículo | Proceso/Thread |
| 🅿️ Espacio de parqueo | Recurso compartido (CPU, memoria) |
| 🚦 Semáforo del parqueadero | Gestor de recursos del SO |
| ⏸️ Vehículo bloqueado (lleno) | Proceso en estado BLOQUEADO |
| ▶️ Vehículo estacionado | Proceso en estado RUNNING |
| 🔒 Lock del contador | Región crítica protegida |

---

## ✨ Características Principales

- **Concurrencia real**: Múltiples threads ejecutándose simultáneamente
- **Sincronización con semáforos**: Control de capacidad máxima del parqueadero
- **Exclusión mutua con locks**: Protección de sección crítica
- **Coordinación con eventos**: Shutdown ordenado de threads
- **Interfaz gráfica intuitiva**: Visualización en tiempo real del estado del sistema
- **Registro de eventos**: Log timestamped de todas las acciones
- **Estadísticas en vivo**: Métricas de vehículos creados, completados y esperando
- **Control interactivo**: Iniciar, detener, agregar vehículos y resetear simulación

---

## 🎬 Demo

```
┌─────────────────────────────────────────────────────────┐
│  Simulador de Parqueadero Inteligente                  │
│  Demostración de Conceptos de SO: Semáforos y Locks    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📊 Estadísticas en Tiempo Real                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Total: 8 │  │ Compl: 3 │  │ Esper: 2 │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                         │
│  🅿️ Estado del Parqueadero                              │
│  [#1 OCUPADO] [#2 OCUPADO] [#3 LIBRE] [#4 LIBRE] ...  │
│                                                         │
│  📜 Registro de Eventos                                 │
│  [14:23:45] Vehículo-1 ingresó al parqueadero         │
│  [14:23:47] Vehículo-3 esperando espacio...           │
│  [14:23:50] Vehículo-2 salió del parqueadero          │
│                                                         │
│  [Iniciar] [Agregar Vehículo] [Detener] [Reiniciar]   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Requisitos

- **Python 3.13+** (funciona con Python 3.8+)
- **Tkinter** (generalmente incluido con Python)
- **Módulos estándar**: `threading`, `queue`, `random`, `time`, `csv`

### Verificar instalación de Tkinter

```bash
# Linux/WSL
python3 -m tkinter

# Windows
python -m tkinter
```

Si no está instalado:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (con Homebrew)
brew install python-tk
```

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/SmartParkingLot.git
cd SmartParkingLot
```

### 2. Crear entorno virtual (recomendado)

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. No se requieren dependencias externas

El proyecto utiliza únicamente la biblioteca estándar de Python.

---

## 📖 Uso

### Ejecutar la aplicación

```bash
# Asegúrate de estar en el directorio raíz del proyecto
python src/main.py
```

### Controles de la interfaz

1. **Iniciar Simulación**: Crea 8 vehículos iniciales que compiten por 5 espacios
2. **Agregar Vehículo**: Añade un vehículo adicional durante la simulación
3. **Detener**: Finaliza todos los threads de forma ordenada
4. **Reiniciar**: Limpia el estado y reinicia la simulación

### Ciclo de vida de un vehículo

1. **Creación**: El vehículo (thread) se crea e inicia
2. **Espera inicial**: Tiempo aleatorio (2-5 seg) antes de intentar entrar
3. **Solicitud de entrada**: Intenta adquirir el semáforo
   - Si hay espacio → Entra y estaciona
   - Si está lleno → Espera en estado bloqueado
4. **Estacionamiento**: Permanece 4-8 segundos (aleatorio)
5. **Salida**: Libera el semáforo y termina el thread

---

## 📁 Estructura del Proyecto

```
SmartParkingLot/
│
├── src/
│   ├── main.py              # Orquestador principal (ParkingSimulator)
│   ├── parking_lot.py       # Recurso compartido con semáforo y lock
│   ├── vehicle.py           # Thread que representa un vehículo
│   ├── gui.py               # Interfaz gráfica Tkinter
│   ├── logger.py            # Sistema de logging CSV
│   └── config.py            # Configuración centralizada
│
├── README.md                # Este archivo
├── event_log.csv            # Log de eventos (generado automáticamente)
└── venv/                    # Entorno virtual (no versionado)
```

### Descripción de componentes

#### `src/main.py` - ParkingSimulator
- Gestiona el ciclo de vida de los threads
- Maneja la cola de eventos (`queue.Queue`)
- Coordina shutdown con `threading.Event`
- Actualiza la GUI periódicamente (cada 200ms)

#### `src/parking_lot.py` - ParkingLot
- **Semáforo**: Limita capacidad máxima (`threading.Semaphore`)
- **Lock**: Protege la variable `occupied` (`threading.Lock`)
- Métodos: `try_enter()`, `exit()`, `get_occupied_count()`

#### `src/vehicle.py` - Vehicle
- Hereda de `threading.Thread`
- Ejecuta el ciclo de vida completo (espera → intento → estacionamiento → salida)
- Publica eventos a la cola para actualizar la GUI

#### `src/gui.py` - ParkingLotGUI
- Visualización del estado del parqueadero (canvas con rectángulos)
- Panel de estadísticas en tiempo real
- Log de eventos con timestamps
- Botones de control

#### `src/config.py` - Configuración
```python
CAPACIDAD = 5                 # Número de espacios del parqueadero
VEHICULOS_INICIALES = 8       # Vehículos al iniciar
TIEMPO_MIN_ESPERA = 2         # Espera antes de intentar entrar
TIEMPO_MAX_ESPERA = 5
TIEMPO_MIN_ESTACIONADO = 4    # Tiempo estacionado
TIEMPO_MAX_ESTACIONADO = 8
REFRESCO_UI = 200             # Frecuencia de actualización GUI (ms)
```

---

## 🧠 Conceptos Técnicos Implementados

### 1. Threading (Concurrencia)

Cada vehículo es un thread independiente:

```python
class Vehicle(threading.Thread):
    def run(self):
        while not self.stop_event.is_set():
            if self.parking_lot.try_enter(self.name, timeout=2):
                time.sleep(random.uniform(4, 8))  # Simular estacionamiento
                self.parking_lot.exit(self.name)
                break
```

### 2. Semáforo (Control de recursos)

Limita el número máximo de threads concurrentes:

```python
self.semaphore = threading.Semaphore(capacidad)

# Vehículo intenta entrar
if self.semaphore.acquire(timeout=2):  # Bloquea si está lleno
    # Espacio adquirido exitosamente
    ...
    self.semaphore.release()  # Liberar al salir
```

**Analogía con SO**: El planificador del SO limita cuántos procesos pueden usar la CPU simultáneamente.

### 3. Lock (Exclusión mutua)

Protege la sección crítica al modificar variables compartidas:

```python
self.lock = threading.Lock()

with self.lock:  # Solo un thread a la vez
    self.occupied += 1
```

**Sin lock**: Condición de carrera → contador inconsistente
**Con lock**: Operación atómica → consistencia garantizada

### 4. Event (Coordinación de threads)

Señal compartida para shutdown ordenado:

```python
self.stop_event = threading.Event()

# Detener todos los threads
self.stop_event.set()

# En el thread del vehículo
while not self.stop_event.is_set():
    # Lógica...
```

### 5. Queue (Comunicación thread-safe)

Canal de comunicación entre threads y GUI:

```python
self.event_queue = queue.Queue()

# En thread del vehículo
self.event_queue.put(f"{self.name} ingresó al parqueadero")

# En thread principal (GUI)
while not self.event_queue.empty():
    event = self.event_queue.get()
    self.gui.log_event(event)
```

---

## ⚙️ Configuración

### Modificar parámetros de la simulación

Edita `src/config.py` para ajustar el comportamiento:

```python
# Ejemplo: Parqueadero más grande y vehículos más rápidos
CAPACIDAD = 10                # Aumentar a 10 espacios
VEHICULOS_INICIALES = 15      # Más vehículos
TIEMPO_MIN_ESTACIONADO = 2    # Menos tiempo estacionado
TIEMPO_MAX_ESTACIONADO = 4
```

### Semilla aleatoria

El archivo `main.py` usa `random.seed(42)` para reproducibilidad. Comenta esta línea para comportamiento aleatorio:

```python
if __name__ == "__main__":
    # random.seed(42)  # Comentar para aleatoriedad real
    root = tk.Tk()
    app = ParkingSimulator(root)
    root.mainloop()
```

---

## 🎓 Casos de Uso Educativos

### Experimentos sugeridos

1. **Deadlock simulation**: Modificar el código para crear un deadlock intencional
2. **Prioridades**: Implementar un sistema de prioridad para vehículos (ej: ambulancias)
3. **Starvation**: Observar si algunos vehículos nunca obtienen espacio (ajustar capacidad a 1)
4. **Fairness**: Implementar una cola FIFO para garantizar justicia
5. **Métricas de rendimiento**: Calcular tiempo promedio de espera

### Preguntas de análisis

- ¿Qué sucede si `CAPACIDAD = 1` y `VEHICULOS_INICIALES = 10`?
- ¿Por qué es necesario usar `timeout` en `semaphore.acquire()`?
- ¿Qué pasaría si eliminamos el lock del contador `occupied`?
- ¿Cómo se compara esto con algoritmos de planificación de CPU (FCFS, Round Robin)?

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

### Lineamientos

- Mantén el código educativo y legible
- Agrega comentarios explicativos en español
- Sigue el estilo existente (PEP 8)
- Documenta nuevas características en el README

---

## 🐛 Problemas Conocidos

- **GUI lenta con 50+ vehículos**: Tkinter tiene limitaciones de rendimiento
- **WSL**: Requiere servidor X (como VcXsrv) para mostrar ventanas
- **macOS**: Posibles problemas con threading en versiones antiguas de Python

### Soluciones

```bash
# WSL: Configurar DISPLAY
export DISPLAY=:0

# Si Tkinter no funciona, reinstalar Python con tk
sudo apt-get install --reinstall python3-tk
```

---

**¡Feliz aprendizaje de Sistemas Operativos!** 🎓✨

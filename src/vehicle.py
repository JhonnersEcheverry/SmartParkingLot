import threading
import time
import random
from config import TIEMPO_MIN_ESPERA, TIEMPO_MAX_ESPERA, TIEMPO_MIN_ESTACIONADO, TIEMPO_MAX_ESTACIONADO

class Vehicle(threading.Thread):
    """
    Clase que representa un vehículo (proceso).
    Cada vehículo es un hilo que compite por un recurso finito (espacio de parqueo).
    """

    def __init__(self, vehicle_id, parking_lot, event_queue, stop_event):
        super().__init__(name=f"Vehículo-{vehicle_id}")
        self.vehicle_id = vehicle_id
        self.parking_lot = parking_lot
        self.event_queue = event_queue
        self.stop_event = stop_event

    def run(self):
        """Ciclo de vida del hilo (proceso)."""
        # MEJORADO: Usar constantes de config.py en lugar de valores hardcoded
        # Ahora si quieres cambiar el tiempo, solo editas config.py
        time.sleep(random.uniform(TIEMPO_MIN_ESPERA, TIEMPO_MAX_ESPERA))

        while not self.stop_event.is_set():
            try:
                # Usar el método try_enter() en lugar de acceder directamente al semáforo

                if self.parking_lot.try_enter(self.name, timeout=2):
                    # Logramos entrar al parqueadero
                    self.event_queue.put(f"{self.name} ingresó al parqueadero.")

                    # Simular tiempo estacionado (usando constantes de config)
                    time.sleep(random.uniform(TIEMPO_MIN_ESTACIONADO, TIEMPO_MAX_ESTACIONADO))

                    # Usar el método exit() en lugar de acceder directamente
                    self.parking_lot.exit(self.name)
                    self.event_queue.put(f"{self.name} salió del parqueadero.")
                    break  # Terminamos el ciclo - este vehículo completó su tarea
                else:
                    # No había espacio disponible - seguimos esperando
                    self.event_queue.put(f"{self.name} esperando espacio...")

            # Capturar solo excepciones específicas, no todas
            except (RuntimeError, ValueError) as e:
                # RuntimeError: problemas con threading
                # ValueError: problemas con semaphore
                self.event_queue.put(f"Error en {self.name}: {e}")
                break

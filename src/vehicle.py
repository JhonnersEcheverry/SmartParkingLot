import threading
import time
import random

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
        time.sleep(random.uniform(2, 5))  # Simula tiempo antes de intentar entrar

        while not self.stop_event.is_set():
            try:
                # Intentar adquirir un espacio (semáforo)
                if self.parking_lot.semaphore.acquire(timeout=2):
                    with self.parking_lot.lock:  # Exclusión mutua
                        self.parking_lot.occupied += 1
                        self.event_queue.put(f"{self.name} ingresó al parqueadero.")
                    # Simula tiempo estacionado
                    time.sleep(random.uniform(4, 8))
                    with self.parking_lot.lock:
                        self.parking_lot.occupied -= 1
                        self.event_queue.put(f"{self.name} salió del parqueadero.")
                    self.parking_lot.semaphore.release()
                    break
                else:
                    # Si no hay cupos, queda bloqueado (esperando)
                    self.event_queue.put(f"{self.name} esperando espacio...")
            except Exception as e:
                self.event_queue.put(f"Error en {self.name}: {e}")
                break

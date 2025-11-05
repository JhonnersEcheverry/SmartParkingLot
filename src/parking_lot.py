import threading

class ParkingLot:
    """
    Clase que representa el recurso compartido (parqueadero).
    Controla concurrencia con semáforo y lock.
    """

    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.occupied = 0
        self.lock = threading.Lock()
        self.semaphore = threading.Semaphore(capacidad)

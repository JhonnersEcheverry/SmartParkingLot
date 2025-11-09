import threading

class ParkingLot:
    """
    Clase que representa el recurso compartido (parqueadero).
    Controla concurrencia con semáforo y lock.

    Tiene métodos propios para entrada/salida para esconder los detalles internos
    """

    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.occupied = 0
        # NOTA: Estos son "privados" (conceptualmente) - no acceder directamente
        self.lock = threading.Lock()
        self.semaphore = threading.Semaphore(capacidad)

    def try_enter(self, vehicle_name, timeout=2):
        """
        Intenta que un vehículo entre al parqueadero.

        Parámetros:
        - vehicle_name: Nombre del vehículo (para logging)
        - timeout: Segundos a esperar si está lleno

        Retorna:
        - True si logró entrar
        - False si está lleno y no pudo entrar
        """

        # Intentar adquirir el semáforo (limita cuántos pueden entrar)
        if self.semaphore.acquire(timeout=timeout):
            # Adquirimos el lock para modificar 'occupied' de forma segura
            with self.lock:
                self.occupied += 1
            return True  # ✅ Logró entrar
        else:
            return False  # ❌ No había espacio

    def exit(self, vehicle_name):
        """
        Un vehículo sale del parqueadero.

        Parámetros:
        - vehicle_name: Nombre del vehículo (para logging futuro)
        """

        # Adquirir lock para modificar 'occupied' de forma segura
        with self.lock:
            self.occupied -= 1
        # Liberar el semáforo (permite que otro vehículo entre)
        self.semaphore.release()

    def get_occupied_count(self):
        """
        Obtiene el número de espacios ocupados de forma segura.

        Retorna:
        - int: Cantidad de espacios ocupados actualmente

        """
        # Por ahora, leer un int es atómico en Python, pero es buena práctica
        # usar un método en lugar de acceso directo
        return self.occupied

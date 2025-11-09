import tkinter as tk
import threading
import queue
import random
import time
from config import CAPACIDAD, VEHICULOS_INICIALES, REFRESCO_UI
from parking_lot import ParkingLot
from vehicle import Vehicle
from gui import ParkingLotGUI
from logger import log_to_csv

class ParkingSimulator:
    def __init__(self, root):
        self.root = root
        self.event_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.parking_lot = ParkingLot(CAPACIDAD)
        self.vehicles = []

        # Variables para rastrear estadísticas
        # Estas variables guardan información sobre lo que pasa en la simulación
        self.total_vehicles_created = 0    # Contador: cuántos vehículos hemos creado en total
        self.successful_parks = 0          # Contador: cuántos vehículos lograron estacionarse
        self.vehicles_exited = 0           # NUEVO: cuántos vehículos salieron completamente
        self.waiting_vehicles = set()      # CORREGIDO: Set de vehículos únicos esperando (evita duplicados)

        self.gui = ParkingLotGUI(root, self.start_simulation, self.add_vehicle, self.stop_simulation, self.reset_simulation)
        self.gui.init_spaces(CAPACIDAD)
        self.root.after(REFRESCO_UI, self.update_ui)

    def start_simulation(self):
        # Verificar si ya hay una simulación en curso
        active_vehicles = sum(1 for v in self.vehicles if v.is_alive())
        if active_vehicles > 0:
            self.gui.log_event("⚠️ Ya hay una simulación en curso")
            return

        self.stop_event.clear()
        for i in range(VEHICULOS_INICIALES):
            v = Vehicle(i + 1, self.parking_lot, self.event_queue, self.stop_event)
            self.vehicles.append(v)
            v.start()

            # Incrementar contador cada vez que creamos un vehículo
            self.total_vehicles_created += 1

            time.sleep(0.5)
        self.gui.log_event("🚦 Simulación iniciada")

    def add_vehicle(self):
        v = Vehicle(len(self.vehicles) + 1, self.parking_lot, self.event_queue, self.stop_event)
        self.vehicles.append(v)
        v.start()

        # Incrementar contador cuando agregamos un vehículo manualmente
        self.total_vehicles_created += 1

        self.gui.log_event(f"Nuevo vehículo agregado: {v.name}")

    def stop_simulation(self):
        self.stop_event.set()
        self.gui.log_event("Simulación detenida")

    def reset_simulation(self):
        # PASO 1: Señalar a todos los hilos que deben detenerse
        self.stop_event.set()
        self.gui.log_event("⏳ Deteniendo hilos...")

        # PASO 2: Esperar a que TODOS los hilos terminen correctamente
        # Esto se llama "thread cleanup" o "limpieza de hilos"
        # Sin esto, los hilos viejos podrían seguir ejecutándose y causar problemas
        for vehicle in self.vehicles:
            if vehicle.is_alive():  # ¿El hilo todavía está corriendo?
                vehicle.join(timeout=3)  # Esperar máximo 3 segundos a que termine
                # join() = "espérame, no sigas hasta que yo termine"

        # PASO 3: Ahora sí es seguro resetear todo
        self.parking_lot = ParkingLot(CAPACIDAD)
        self.vehicles.clear()

        # Resetear todas las estadísticas a cero
        self.total_vehicles_created = 0
        self.successful_parks = 0
        self.vehicles_exited = 0
        self.waiting_vehicles = set()  # Limpiar el set

        # Limpiar interfaz
        self.gui.init_spaces(CAPACIDAD)
        self.gui.log_box.delete(0, tk.END)
        self.gui.log_event("Simulación reiniciada")

    def update_ui(self):
        """Actualiza visualmente los espacios y eventos."""
        while not self.event_queue.empty():
            event = self.event_queue.get()
            self.gui.log_event(event)
            log_to_csv("event_log.csv", event)

            # Analizar cada evento para actualizar estadísticas
            # Extraer el nombre del vehículo del evento
            vehicle_name = event.split()[0] if event else ""  # Ejemplo: "Vehículo-1" de "Vehículo-1 ingresó..."

            if "ingresó al parqueadero" in event:
                # Un vehículo logró estacionarse exitosamente
                self.successful_parks += 1
                # Remover del set de esperando (si estaba ahí)
                self.waiting_vehicles.discard(vehicle_name)

            elif "esperando espacio" in event:
                # Agregar vehículo al set de esperando (set evita duplicados automáticamente)
                # Si el mismo vehículo espera 10 veces, solo cuenta como 1
                self.waiting_vehicles.add(vehicle_name)

            elif "salió del parqueadero" in event:
                # Un vehículo completó su ciclo (entró y salió)
                self.vehicles_exited += 1
                # Asegurar que no esté en el set de esperando
                self.waiting_vehicles.discard(vehicle_name)

        # Usar el método get_occupied_count() en lugar de acceso directo
        # Esto respeta la encapsulación de la clase ParkingLot
        self.gui.update_spaces(self.parking_lot.get_occupied_count(), CAPACIDAD)

        # Actualizar el panel de estadísticas
        # Llamamos al nuevo método de la GUI para mostrar los números actualizados
        self.gui.update_statistics(
            self.total_vehicles_created,
            self.vehicles_exited,  # Cambiado: mostrar salidas en lugar de estacionados
            len(self.waiting_vehicles)  # Tamaño del set = vehículos únicos esperando
        )

        # Detener automáticamente cuando todos los vehículos terminen
        # Verificar si todos los hilos han terminado (vehículos completaron su ciclo)
        if self.vehicles and not self.stop_event.is_set():
            # Contar cuántos vehículos siguen activos
            active_vehicles = sum(1 for v in self.vehicles if v.is_alive())

            # Si no hay vehículos activos, la simulación terminó naturalmente
            if active_vehicles == 0:
                self.gui.log_event("✅ Simulación completada - Todos los vehículos finalizaron")
                self.stop_event.set()  # Marcar como detenida
                return  # No seguir actualizando

        # Llamar esta función de nuevo después de REFRESCO_UI milisegundos
        self.root.after(REFRESCO_UI, self.update_ui)

if __name__ == "__main__":
    random.seed(42)
    root = tk.Tk()
    app = ParkingSimulator(root)
    root.mainloop()

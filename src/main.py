import tkinter as tk
import threading
import queue
import random
import time
from config import *
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
        self.gui = ParkingLotGUI(root, self.start_simulation, self.add_vehicle, self.stop_simulation, self.reset_simulation)
        self.gui.init_spaces(CAPACIDAD)
        self.root.after(REFRESCO_UI, self.update_ui)

    def start_simulation(self):
        self.stop_event.clear()
        for i in range(VEHICULOS_INICIALES):
            v = Vehicle(i + 1, self.parking_lot, self.event_queue, self.stop_event)
            self.vehicles.append(v)
            v.start()
            time.sleep(0.5)
        self.gui.log_event("Simulación iniciada 🚦")

    def add_vehicle(self):
        v = Vehicle(len(self.vehicles) + 1, self.parking_lot, self.event_queue, self.stop_event)
        self.vehicles.append(v)
        v.start()
        self.gui.log_event(f"Nuevo vehículo agregado: {v.name}")

    def stop_simulation(self):
        self.stop_event.set()
        self.gui.log_event("Simulación detenida 🛑")

    def reset_simulation(self):
        self.stop_event.set()
        self.parking_lot = ParkingLot(CAPACIDAD)
        self.vehicles.clear()
        self.gui.init_spaces(CAPACIDAD)
        self.gui.log_box.delete(0, tk.END)
        self.gui.log_event("Simulación reiniciada 🔁")

    def update_ui(self):
        """Actualiza visualmente los espacios y eventos."""
        while not self.event_queue.empty():
            event = self.event_queue.get()
            self.gui.log_event(event)
            log_to_csv("event_log.csv", event)
        self.gui.update_spaces(self.parking_lot.occupied, CAPACIDAD)
        self.root.after(REFRESCO_UI, self.update_ui)

if __name__ == "__main__":
    random.seed(42)
    root = tk.Tk()
    app = ParkingSimulator(root)
    root.mainloop()

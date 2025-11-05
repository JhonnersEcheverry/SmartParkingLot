import tkinter as tk
from tkinter import ttk

class ParkingLotGUI:
    def __init__(self, root, start_callback, add_vehicle_callback, stop_callback, reset_callback):
        self.root = root
        self.root.title("Simulador de Parqueadero Inteligente")
        self.root.geometry("800x600")

        self.status_label = tk.Label(root, text="Estado del sistema operativo (simulado)", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # Canvas de parqueadero
        self.canvas = tk.Canvas(root, width=700, height=250)
        self.canvas.pack()
        self.spaces = []

        # Lista de eventos
        self.log_box = tk.Listbox(root, height=10, width=100)
        self.log_box.pack(pady=10)

        # Botones de control
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Iniciar Simulación", command=start_callback, width=20).grid(row=0, column=0, padx=10)
        tk.Button(frame, text="Agregar Vehículo", command=add_vehicle_callback, width=20).grid(row=0, column=1, padx=10)
        tk.Button(frame, text="Detener", command=stop_callback, width=20).grid(row=0, column=2, padx=10)
        tk.Button(frame, text="Reiniciar", command=reset_callback, width=20).grid(row=0, column=3, padx=10)

    def init_spaces(self, capacidad):
        """Dibuja los espacios de parqueo."""
        self.canvas.delete("all")
        self.spaces.clear()
        for i in range(capacidad):
            x0 = 60 + i * 130
            rect = self.canvas.create_rectangle(x0, 80, x0 + 100, 180, fill="lightgray")
            text = self.canvas.create_text(x0 + 50, 130, text=f"{i+1}")
            self.spaces.append((rect, text))

    def update_spaces(self, ocupados, capacidad):
        """Actualiza visualmente los espacios ocupados."""
        for i, (rect, text) in enumerate(self.spaces):
            if i < ocupados:
                self.canvas.itemconfig(rect, fill="green")
            else:
                self.canvas.itemconfig(rect, fill="lightgray")

    def log_event(self, message):
        """Muestra mensajes de eventos (cola)."""
        self.log_box.insert(tk.END, message)
        self.log_box.yview(tk.END)

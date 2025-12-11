# ejercicio2.py
# Versión visual sencilla usando Tkinter

import tkinter as tk
from tkinter import ttk
import math

from ejercicio1 import (
    Fragata, Corbeta, Submarino,
    Capitan, Flota
)


class AppFlota(tk.Tk):
    def __init__(self, flota):
        super().__init__()
        self.title("Simulador Naval - Tkinter")
        self.geometry("900x500")

        self.flota = flota
        self.activa = None
        self.pos = {}

        # Canvas
        self.canvas = tk.Canvas(self, bg="#0d1b2a")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Panel lateral
        panel = ttk.Frame(self, padding=10)
        panel.pack(side="right", fill="y")

        ttk.Label(panel, text="Plataforma activa:").pack(anchor="w")
        self.combo = ttk.Combobox(panel, state="readonly",
                                  values=[p.nombre for p in flota.plataformas])
        self.combo.pack(fill="x", pady=5)
        self.combo.bind("<<ComboboxSelected>>", self.cambiar_activa)

        ttk.Label(panel, text="Rumbo:").pack(anchor="w")
        self.var_r = tk.StringVar(value="0")
        ttk.Entry(panel, textvariable=self.var_r).pack(fill="x")

        ttk.Label(panel, text="Velocidad:").pack(anchor="w")
        self.var_v = tk.StringVar(value="0")
        ttk.Entry(panel, textvariable=self.var_v).pack(fill="x")

        ttk.Button(panel, text="Aplicar",
                   command=self.actualizar_mov).pack(fill="x", pady=8)
        ttk.Button(panel, text="Daño (20)",
                   command=self.daniar).pack(fill="x")

        self.lbl = ttk.Label(panel, text="", justify="left")
        self.lbl.pack(fill="x", pady=8)

        self.dibujar_inicial()
        self.cambiar_activa()
        self.loop()

    def dibujar_inicial(self):
        ancho = 700
        alto = 450
        n = len(self.flota.plataformas)
        paso = ancho / (n + 1)

        for i, p in enumerate(self.flota.plataformas, start=1):
            x = paso * i
            y = alto / 2
            rect = self.canvas.create_rectangle(
                x - 25, y - 10, x + 25, y + 10,
                fill="#1b6ca8"
            )
            txt = self.canvas.create_text(x, y - 18, text=p.nombre, fill="white")
            self.pos[p] = {"x": x, "y": y, "rect": rect, "txt": txt}

    def cambiar_activa(self, event=None):
        nombre = self.combo.get()
        for p in self.flota.plataformas:
            if p.nombre == nombre:
                self.activa = p
        self.actualizar_info()

    def actualizar_info(self):
        if not self.activa:
            self.lbl.config(text="")
            return
        p = self.activa
        txt = (
            f"{p.nombre} ({p.pais})\n"
            f"Rumbo: {p.rumbo}\n"
            f"Velocidad: {p.velocidad}\n"
            f"Integridad: {p.integridad}/100\n"
        )
        if p.capitan:
            txt += f"Capitán: {p.capitan.nombre}\n"
        self.lbl.config(text=txt)

    def actualizar_mov(self):
        if not self.activa:
            return
        try:
            rumbo = float(self.var_r.get())
            vel = float(self.var_v.get())
        except:
            return
        self.activa.navegar(rumbo, vel)
        self.actualizar_info()

    def daniar(self):
        if not self.activa:
            return
        self.activa.recibir_danio(20)
        self.actualizar_info()

    def loop(self):
        for p, d in self.pos.items():
            ang = math.radians(p.rumbo)
            dx = math.cos(ang) * p.velocidad * 0.1
            dy = math.sin(ang) * p.velocidad * 0.1

            d["x"] += dx
            d["y"] += dy

            self.canvas.coords(
                d["rect"], d["x"] - 25, d["y"] - 10, d["x"] + 25, d["y"] + 10
            )
            self.canvas.coords(d["txt"], d["x"], d["y"] - 18)

        self.after(50, self.loop)


# =====================
# EJECUCIÓN DEL GUI
# =====================

if __name__ == "__main__":
    # Crear capitanes y barcos igual que en el ejercicio 1
    c1 = Capitan("Ramírez", "Capitán de Fragata", 15)
    c2 = Capitan("López", "Capitán de Corbeta", 10)
    c3 = Capitan("Santos", "Capitán de Navío", 20)

    fragata = Fragata("F-101", "España", 146, 6000, 28, 16, 1, "AA")
    corbeta = Corbeta("C-21", "España", 90, 2500, 24, 8, 15)
    submarino = Submarino("S-80", "España", 80, 3000, 20, 300, "Diesel-Eléctrica", 6)

    c1.asumir_mando(fragata)
    c2.asumir_mando(corbeta)
    c3.asumir_mando(submarino)

    flota = Flota("Flota del Atlántico")
    flota.agregar(fragata)
    flota.agregar(corbeta)
    flota.agregar(submarino)

    app = AppFlota(flota)
    app.mainloop()

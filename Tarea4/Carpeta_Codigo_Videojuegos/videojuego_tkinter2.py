#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 2 - Tema 3
Tkinter + (opcional) pygame para audio
--------------------------------------
- Interfaz para gestionar barcos (clase Barco del ejercicio 1).
- Movimiento en Canvas según velocidad (km/h) y rumbo (grados).
- Selector de barco activo, creación de nuevos barcos y acciones:
  disparar, cambiar velocidad/rumbo, munición.
- Sonido de fondo y disparo con pygame si está disponible (fallback silencioso).

Inicio: SOLO 1 barco cargado (el resto los crea el usuario).
"""
from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk, messagebox

# ====================== MODELO ======================

class Barco:
    def __init__(self, nombre, posicionX, posicionY, velocidad, rumbo, numeroMunicion):
        self.nombre = nombre
        self.posicionX = float(posicionX)
        self.posicionY = float(posicionY)
        self.velocidad = float(velocidad)          # km/h (0..20)
        self.rumbo = int(rumbo)                    # 1..359
        self.numeroMunicion = int(numeroMunicion)  # >=0

    def __str__(self):
        return (f"{self.nombre} | Pos=({self.posicionX:.1f},{self.posicionY:.1f}) "
                f"Vel={self.velocidad:.1f} km/h Rumbo={self.rumbo}° Mun={self.numeroMunicion}")

    def disparar(self):
        if self.numeroMunicion > 0:
            self.numeroMunicion -= 1
            return True
        return False

    def setVelocidad(self, nuevaVelocidad):
        if 0 <= nuevaVelocidad <= 20:
            self.velocidad = float(nuevaVelocidad)
            return True
        return False

    def setRumbo(self, nuevoRumbo):
        if 1 <= nuevoRumbo <= 359:
            self.rumbo = int(nuevoRumbo)
            return True
        return False


# ====================== AUDIO (opc.) ======================

class Audio:
    def __init__(self):
        self.ok = False
        try:
            import pygame
            self.pg = pygame
            pygame.mixer.init()
            self.ok = True
        except Exception:
            self.pg = None
            self.ok = False

    def load_and_loop_bg(self):
        if not self.ok:
            return
        try:
            import numpy as np
            sr = 22050
            t = np.linspace(0, 1, sr, False)
            wave = (0.03 * np.sin(2*math.pi*264*t)).astype(np.float32)
            arr = (wave * 32767).astype(np.int16)
            sound = self.pg.sndarray.make_sound(arr)
            sound.play(loops=-1)
        except Exception:
            pass

    def play_cannon(self):
        if not self.ok:
            return
        try:
            import numpy as np
            sr = 22050
            dur = 0.25
            t = np.linspace(0, dur, int(sr*dur), False)
            wave = 0.9*np.exp(-8*t)*np.sin(2*math.pi*(300 - 240*t)*t)
            arr = (wave * 32767).astype('int16')
            sound = self.pg.sndarray.make_sound(arr)
            sound.play()
        except Exception:
            pass


# ====================== VISTA / CONTROL ======================

PIXELS_PER_KMH = 8   # escala: 1 km/h -> 8 px/s

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Batalla Naval - Gestión de Barcos (Tkinter + pygame opcional)")
        self.geometry("900x560")
        self.minsize(820, 520)

        self.audio = Audio()
        self.after(500, self.audio.load_and_loop_bg)

        self.barcos: list[Barco] = []
        self.activo: Barco | None = None
        self.canvas_items: dict[Barco, int] = {}

        self._build_ui()
        self._crear_demo()  # ahora solo 1 barco inicial

        self._tick()

    def _build_ui(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, bg="#0a2740", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(8,4), pady=8)

        panel = ttk.Frame(self, padding=8)
        panel.grid(row=0, column=1, sticky="nsew", padx=(4,8), pady=8)
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="Barco activo:").grid(row=0, column=0, sticky="w")
        self.cbo = ttk.Combobox(panel, state="readonly")
        self.cbo.grid(row=1, column=0, sticky="ew", pady=(0,8))
        self.cbo.bind("<<ComboboxSelected>>", self._on_select_barco)

        self.lbl_info = ttk.Label(panel, text="—", anchor="center")
        self.lbl_info.grid(row=2, column=0, sticky="ew", pady=(0,8))

        box = ttk.LabelFrame(panel, text="Controles")
        box.grid(row=3, column=0, sticky="ew", pady=6)
        for i in range(4):
            box.columnconfigure(i, weight=1)

        ttk.Button(box, text="Vel -", command=lambda: self._ajustar_vel(-1)).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(box, text="Vel +", command=lambda: self._ajustar_vel(+1)).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(box, text="Rumbo -15°", command=lambda: self._ajustar_rumbo(-15)).grid(row=0, column=2, sticky="ew", padx=2, pady=2)
        ttk.Button(box, text="Rumbo +15°", command=lambda: self._ajustar_rumbo(+15)).grid(row=0, column=3, sticky="ew", padx=2, pady=2)

        ttk.Button(box, text="Munición +1", command=lambda: self._ajustar_mun(+1)).grid(row=1, column=0, columnspan=2, sticky="ew", padx=2, pady=2)
        ttk.Button(box, text="Disparar", command=self._disparar).grid(row=1, column=2, columnspan=2, sticky="ew", padx=2, pady=2)

        ttk.Button(panel, text="Crear nuevo barco", command=self._dialogo_nuevo).grid(row=4, column=0, sticky="ew", pady=(10,4))

        ttk.Label(panel, text="Velocidad 0..20 km/h — Rumbo 1..359°\nWrap en bordes de mapa.").grid(row=5, column=0, sticky="ew", pady=6)

    def _crear_demo(self):
        # Solo un barco inicial
        self._add_barco(Barco("Titanic", 120, 160, 8, 90, 5))
        self._set_activo(self.barcos[0])

    def _add_barco(self, b: Barco):
        self.barcos.append(b)
        item = self.canvas.create_polygon(self._triangulo(b.posicionX, b.posicionY, b.rumbo),
                                          fill="#4dd0e1", outline="#b2ebf2", width=2)
        self.canvas_items[b] = item
        self._refrescar_selector()

    def _refrescar_selector(self):
        self.cbo["values"] = [b.nombre for b in self.barcos]
        if self.activo and self.activo in self.barcos:
            self.cbo.current(self.barcos.index(self.activo))

    def _set_activo(self, b: Barco | None):
        self.activo = b
        self.lbl_info.config(text="—" if not b else str(b))
        self._refrescar_selector()

    def _on_select_barco(self, _):
        idx = self.cbo.current()
        if 0 <= idx < len(self.barcos):
            self._set_activo(self.barcos[idx])

    @staticmethod
    def _triangulo(x: float, y: float, rumbo: int, tam: float = 18) -> list[float]:
        p1 = (tam, 0)
        p2 = (-tam*0.6, tam*0.6)
        p3 = (-tam*0.6, -tam*0.6)
        ang = math.radians(rumbo)
        cos_a, sin_a = math.cos(ang), math.sin(ang)

        def rot(px, py):
            rx = px * cos_a - py * sin_a
            ry = px * sin_a + py * cos_a
            return (x + rx, y + ry)

        a = rot(*p1); b = rot(*p2); c = rot(*p3)
        return [a[0], a[1], b[0], b[1], c[0], c[1]]

    def _ajustar_vel(self, delta: int):
        if not self.activo: return
        nv = max(0, min(20, self.activo.velocidad + delta))
        if self.activo.setVelocidad(nv):
            self._set_activo(self.activo)

    def _ajustar_rumbo(self, delta: int):
        if not self.activo: return
        nr = (self.activo.rumbo + delta) % 360
        if nr == 0: nr = 1
        if self.activo.setRumbo(nr):
            self._set_activo(self.activo)

    def _ajustar_mun(self, delta: int):
        if not self.activo: return
        self.activo.numeroMunicion = max(0, self.activo.numeroMunicion + delta)
        self._set_activo(self.activo)

    def _disparar(self):
        if not self.activo: return
        if self.activo.disparar():
            self.audio.play_cannon()
            self._set_activo(self.activo)
        else:
            messagebox.showwarning("Munición", f"{self.activo.nombre} no tiene munición.")

    def _dialogo_nuevo(self):
        win = tk.Toplevel(self)
        win.title("Nuevo barco")
        win.grab_set()
        for i in range(2):
            win.grid_columnconfigure(i, weight=1)

        etiquetas = ["Nombre", "Pos X", "Pos Y", "Velocidad (0..20)", "Rumbo (1..359)", "Munición"]
        vars_ = [tk.StringVar(value=v) for v in ["Barco", "100", "100", "5", "45", "3"]]
        for i, (lbl, var) in enumerate(zip(etiquetas, vars_), start=0):
            ttk.Label(win, text=lbl).grid(row=i, column=0, sticky="e", padx=6, pady=4)
            ttk.Entry(win, textvariable=var).grid(row=i, column=1, sticky="ew", padx=6, pady=4)

        def crear():
            try:
                b = Barco(vars_[0].get(), float(vars_[1].get()), float(vars_[2].get()),
                          float(vars_[3].get()), int(vars_[4].get()), int(vars_[5].get()))
                if not (0 <= b.velocidad <= 20): raise ValueError
                if not (1 <= b.rumbo <= 359): raise ValueError
            except Exception:
                messagebox.showerror("Datos inválidos", "Revisa los valores introducidos.")
                return
            self._add_barco(b)
            self._set_activo(b)
            win.destroy()

        ttk.Button(win, text="Crear", command=crear).grid(row=len(etiquetas), column=0, columnspan=2, sticky="ew", padx=6, pady=8)

    def _tick(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        for b in self.barcos:
            step = b.velocidad * PIXELS_PER_KMH / 30.0
            rad = math.radians(b.rumbo)
            b.posicionX += math.cos(rad) * step
            b.posicionY += math.sin(rad) * step

            if b.posicionX < 0: b.posicionX = w
            if b.posicionX > w: b.posicionX = 0
            if b.posicionY < 0: b.posicionY = h
            if b.posicionY > h: b.posicionY = 0

            self.canvas.coords(self.canvas_items[b], *self._triangulo(b.posicionX, b.posicionY, b.rumbo))

        if self.activo:
            self.lbl_info.config(text=str(self.activo))

        self.after(33, self._tick)


if __name__ == "__main__":
    App().mainloop()

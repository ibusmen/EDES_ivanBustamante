import math
import tkinter as tk
from tkinter import ttk, messagebox

# =========================================
#   CLASES DEL MODELO: Caja y Camion
# =========================================

class Caja:
    def __init__(self, codigo, peso_kg, descripcion_carga,
                 largo, ancho, altura):
        self.codigo = codigo
        self.peso_kg = peso_kg
        self.descripcion_carga = descripcion_carga
        self.largo = largo
        self.ancho = ancho
        self.altura = altura

    def __str__(self):
        return (f"Caja {self.codigo} - {self.descripcion_carga}\n"
                f"Peso: {self.peso_kg} kg\n"
                f"Dimensiones: {self.largo} x {self.ancho} x {self.altura} m")


class Camion:
    def __init__(self, matricula, conductor, capacidad_kg,
                 descripcion_carga, rumbo, velocidad,
                 pos_x=100, pos_y=100):
        self.matricula = matricula
        self.conductor = conductor
        self.capacidad_kg = capacidad_kg
        self.descripcion_carga = descripcion_carga
        self.rumbo = rumbo          # 1..359
        self.velocidad = velocidad  # entero
        self.cajas = []             # lista de objetos Caja

        # Para la representación gráfica
        self.pos_x = pos_x
        self.pos_y = pos_y

    def peso_total(self):
        total = 0.0
        for caja in self.cajas:
            total += caja.peso_kg
        return total

    def add_caja(self, caja):
        peso_con_nueva = self.peso_total() + caja.peso_kg
        if peso_con_nueva <= self.capacidad_kg:
            self.cajas.append(caja)
        else:
            print("No se puede añadir la caja: se supera la capacidad máxima.")

    def __str__(self):
        return (f"Camión {self.matricula}\n"
                f"Conductor: {self.conductor}\n"
                f"Descripción carga: {self.descripcion_carga}\n"
                f"Capacidad: {self.capacidad_kg} kg\n"
                f"Rumbo: {self.rumbo}°\n"
                f"Velocidad: {self.velocidad} km/h\n"
                f"Nº de cajas: {len(self.cajas)}\n"
                f"Peso total cargado: {self.peso_total()} kg")

    def setVelocidad(self, nueva_velocidad):
        self.velocidad = nueva_velocidad

    def setRumbo(self, nuevo_rumbo):
        if 1 <= nuevo_rumbo <= 359:
            self.rumbo = nuevo_rumbo
        else:
            print("Rumbo inválido, debe estar entre 1 y 359 grados.")

    def claxon(self):
        print("piiiiiii")


# =========================================
#   AUDIO OPCIONAL CON PYGAME
# =========================================

class Audio:
    def __init__(self, ruta_sonido="claxon.wav"):
        self.ok = False
        self.snd = None
        self.ruta = ruta_sonido
        try:
            import pygame
            self.pg = pygame
            pygame.mixer.init()
            try:
                self.snd = pygame.mixer.Sound(self.ruta)
                self.ok = True
            except Exception:
                self.snd = None
        except Exception:
            self.pg = None

    def play_claxon(self):
        if self.ok and self.snd is not None:
            self.snd.play()


# =========================================
#   INTERFAZ GRÁFICA CON TKINTER
# =========================================

PIXELS_POR_VELOCIDAD = 0.5   # Factor de escala para movimiento

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Camiones - Tkinter")
        self.geometry("900x550")
        self.minsize(800, 500)

        # Audio (si no hay pygame o no está el fichero, no peta)
        self.audio = Audio("claxon.wav")

        # Datos
        self.camiones = []
        self.camion_activo = None
        self.canvas_items = {}   # camion -> rectángulo del camión
        self.canvas_cajas = {}   # camion -> lista de rectángulos de cajas

        self._crear_interfaz()
        self._crear_camion_inicial()
        self._bucle_animacion()

    # -------------------------------
    #   Construcción de la interfaz
    # -------------------------------
    def _crear_interfaz(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        # Canvas (zona de “mapa”)
        self.canvas = tk.Canvas(self, bg="#e0f7fa", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=8)

        # Botón derecho del ratón -> claxon del camión activo
        self.canvas.bind("<Button-3>", self._claxon_evento)

        # Panel lateral derecho
        panel = ttk.Frame(self, padding=8)
        panel.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=8)
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="Camión activo:").grid(row=0, column=0, sticky="w")
        self.selector = ttk.Combobox(panel, state="readonly")
        self.selector.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.selector.bind("<<ComboboxSelected>>", self._seleccionar_camion)

        self.lbl_info = ttk.Label(panel, text="—", justify="left")
        self.lbl_info.grid(row=2, column=0, sticky="ew", pady=(0, 8))

        # Controles de velocidad y rumbo
        marco_controles = ttk.LabelFrame(panel, text="Controles")
        marco_controles.grid(row=3, column=0, sticky="ew", pady=6)
        for i in range(3):
            marco_controles.columnconfigure(i, weight=1)

        ttk.Button(marco_controles, text="Vel -",
                   command=lambda: self._cambiar_velocidad(-5)).grid(
            row=0, column=0, sticky="ew", padx=2, pady=2
        )
        ttk.Button(marco_controles, text="Vel +",
                   command=lambda: self._cambiar_velocidad(+5)).grid(
            row=0, column=1, sticky="ew", padx=2, pady=2
        )

        ttk.Button(marco_controles, text="Rumbo -15°",
                   command=lambda: self._cambiar_rumbo(-15)).grid(
            row=1, column=0, sticky="ew", padx=2, pady=2
        )
        ttk.Button(marco_controles, text="Rumbo +15°",
                   command=lambda: self._cambiar_rumbo(+15)).grid(
            row=1, column=1, sticky="ew", padx=2, pady=2
        )

        ttk.Button(marco_controles, text="Claxon",
                   command=self._claxon).grid(
            row=0, column=2, rowspan=2, sticky="nsew", padx=2, pady=2
        )

        # Controles de carga (cajas)
        marco_carga = ttk.LabelFrame(panel, text="Carga")
        marco_carga.grid(row=4, column=0, sticky="ew", pady=6)
        marco_carga.columnconfigure(0, weight=1)
        marco_carga.columnconfigure(1, weight=1)

        ttk.Button(marco_carga, text="Añadir caja",
                   command=self._dialogo_nueva_caja).grid(
            row=0, column=0, sticky="ew", padx=2, pady=2
        )
        ttk.Button(marco_carga, text="Mostrar info",
                   command=self._mostrar_info).grid(
            row=0, column=1, sticky="ew", padx=2, pady=2
        )

        # Crear nuevos camiones
        ttk.Button(panel, text="Crear nuevo camión",
                   command=self._dialogo_nuevo_camion).grid(
            row=5, column=0, sticky="ew", pady=(10, 4)
        )

        ttk.Label(panel,
                  text="Botón derecho en el mapa = claxon.\n"
                       "Velocidad y rumbo afectan al movimiento.",
                  justify="left").grid(row=6, column=0, sticky="ew", pady=4)

    # -------------------------------
    #   Camión inicial de ejemplo
    # -------------------------------
    def _crear_camion_inicial(self):
        cam = Camion(
            "1234ABC", "Iván", 2000.0,
            "Electrónica", rumbo=45, velocidad=40,
            pos_x=150, pos_y=150
        )
        self._add_camion(cam)
        self._set_camion_activo(cam)

    def _add_camion(self, camion):
        self.camiones.append(camion)

        x, y = camion.pos_x, camion.pos_y
        rect = self.canvas.create_rectangle(
            x - 20, y - 10, x + 20, y + 10,
            fill="#00796b", outline="#004d40", width=2
        )
        self.canvas_items[camion] = rect
        self.canvas_cajas[camion] = []   # lista de rectángulos de cajas

        self._actualizar_selector()

    def _actualizar_selector(self):
        valores = [c.matricula for c in self.camiones]
        self.selector["values"] = valores
        if self.camion_activo in self.camiones:
            idx = self.camiones.index(self.camion_activo)
            self.selector.current(idx)

    def _set_camion_activo(self, camion):
        self.camion_activo = camion
        if camion is None:
            self.lbl_info.config(text="—")
        else:
            self.lbl_info.config(text=str(camion))
        self._actualizar_selector()

    def _seleccionar_camion(self, event):
        idx = self.selector.current()
        if 0 <= idx < len(self.camiones):
            self._set_camion_activo(self.camiones[idx])

    # -------------------------------
    #   Controles de velocidad/rumbo
    # -------------------------------
    def _cambiar_velocidad(self, delta):
        if not self.camion_activo:
            return
        nueva = self.camion_activo.velocidad + delta
        if nueva < 0:
            nueva = 0
        self.camion_activo.setVelocidad(nueva)
        self.lbl_info.config(text=str(self.camion_activo))

    def _cambiar_rumbo(self, delta):
        if not self.camion_activo:
            return
        nuevo = (self.camion_activo.rumbo + delta) % 360
        if nuevo == 0:
            nuevo = 1
        self.camion_activo.setRumbo(nuevo)
        self.lbl_info.config(text=str(self.camion_activo))

    # -------------------------------
    #   Dibujar cajas sobre el camión
    # -------------------------------
    def _dibujar_cajas_camion(self, camion):
        # Borrar rectángulos antiguos
        for item in self.canvas_cajas.get(camion, []):
            self.canvas.delete(item)

        nueva_lista = []
        num_cajas = len(camion.cajas)

        for i in range(num_cajas):
            # Apilar las cajas por encima del camión
            x = camion.pos_x
            y = camion.pos_y - 15 - i * 12

            rect = self.canvas.create_rectangle(
                x - 10, y - 8, x + 10, y + 2,
                fill="#ffb300", outline="#ff6f00", width=1
            )
            nueva_lista.append(rect)

        self.canvas_cajas[camion] = nueva_lista

    # -------------------------------
    #   Gestión de cajas y carga
    # -------------------------------
    def _dialogo_nueva_caja(self):
        if not self.camion_activo:
            messagebox.showwarning("Sin camión", "Primero selecciona un camión.")
            return

        win = tk.Toplevel(self)
        win.title("Nueva caja")
        win.grab_set()
        for i in range(2):
            win.grid_columnconfigure(i, weight=1)

        etiquetas = ["Código", "Peso (kg)", "Descripción",
                     "Largo (m)", "Ancho (m)", "Altura (m)"]
        valores_defecto = ["C001", "100.0", "Carga genérica",
                           "1.0", "0.8", "0.6"]
        vars_ = []
        for i, (et, val) in enumerate(zip(etiquetas, valores_defecto)):
            ttk.Label(win, text=et).grid(row=i, column=0, sticky="e", padx=4, pady=4)
            v = tk.StringVar(value=val)
            vars_.append(v)
            ttk.Entry(win, textvariable=v).grid(row=i, column=1, sticky="ew", padx=4, pady=4)

        def crear():
            try:
                caja = Caja(
                    vars_[0].get(),
                    float(vars_[1].get()),
                    vars_[2].get(),
                    float(vars_[3].get()),
                    float(vars_[4].get()),
                    float(vars_[5].get())
                )
            except ValueError:
                messagebox.showerror("Error", "Revisa los datos de la caja.")
                return

            self.camion_activo.add_caja(caja)
            self._dibujar_cajas_camion(self.camion_activo)
            self.lbl_info.config(text=str(self.camion_activo))
            win.destroy()

        ttk.Button(win, text="Añadir", command=crear).grid(
            row=len(etiquetas), column=0, columnspan=2,
            sticky="ew", padx=4, pady=8
        )

    def _mostrar_info(self):
        if not self.camion_activo:
            messagebox.showinfo("Info", "No hay camión seleccionado.")
            return
        messagebox.showinfo("Información del camión", str(self.camion_activo))

    # -------------------------------
    #   Claxon (botón y ratón)
    # -------------------------------
    def _claxon(self):
        if not self.camion_activo:
            return
        self.camion_activo.claxon()
        self.audio.play_claxon()

    def _claxon_evento(self, event):
        # Click derecho en el canvas
        self._claxon()

    # -------------------------------
    #   Crear nuevos camiones
    # -------------------------------
    def _dialogo_nuevo_camion(self):
        win = tk.Toplevel(self)
        win.title("Nuevo camión")
        win.grab_set()
        for i in range(2):
            win.grid_columnconfigure(i, weight=1)

        etiquetas = ["Matrícula", "Conductor", "Capacidad kg",
                     "Descripción", "Rumbo (1-359)", "Velocidad"]
        valores_defecto = ["0000XXX", "Conductor", "3000.0",
                           "Carga", "90", "50"]
        vars_ = []
        for i, (et, val) in enumerate(zip(etiquetas, valores_defecto)):
            ttk.Label(win, text=et).grid(row=i, column=0, sticky="e", padx=4, pady=4)
            v = tk.StringVar(value=val)
            vars_.append(v)
            ttk.Entry(win, textvariable=v).grid(row=i, column=1, sticky="ew", padx=4, pady=4)

        def crear():
            try:
                matricula = vars_[0].get()
                conductor = vars_[1].get()
                capacidad = float(vars_[2].get())
                descr = vars_[3].get()
                rumbo = int(vars_[4].get())
                velocidad = int(vars_[5].get())
                if not (1 <= rumbo <= 359):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Revisa los datos del camión.")
                return

            nuevo = Camion(
                matricula, conductor, capacidad, descr,
                rumbo, velocidad,
                pos_x=200, pos_y=200
            )
            self._add_camion(nuevo)
            self._set_camion_activo(nuevo)
            win.destroy()

        ttk.Button(win, text="Crear", command=crear).grid(
            row=len(etiquetas), column=0, columnspan=2,
            sticky="ew", padx=4, pady=8
        )

    # -------------------------------
    #   Bucle de animación
    # -------------------------------
    def _bucle_animacion(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        for camion in self.camiones:
            # Movimiento en función de rumbo (grados) y velocidad (entero)
            ang = math.radians(camion.rumbo)
            dx = math.cos(ang) * camion.velocidad * PIXELS_POR_VELOCIDAD / 30.0
            dy = math.sin(ang) * camion.velocidad * PIXELS_POR_VELOCIDAD / 30.0

            camion.pos_x += dx
            camion.pos_y += dy

            # Wrap-around en bordes
            if camion.pos_x < 0:
                camion.pos_x = w
            elif camion.pos_x > w:
                camion.pos_x = 0

            if camion.pos_y < 0:
                camion.pos_y = h
            elif camion.pos_y > h:
                camion.pos_y = 0

            # Actualizar rectángulo del camión
            rect = self.canvas_items[camion]
            x, y = camion.pos_x, camion.pos_y
            self.canvas.coords(rect, x - 20, y - 10, x + 20, y + 10)

            # Actualizar cajas dibujadas encima
            cajas_items = self.canvas_cajas.get(camion, [])
            for i, item in enumerate(cajas_items):
                x_caja = camion.pos_x
                y_caja = camion.pos_y - 15 - i * 12
                self.canvas.coords(item, x_caja - 10, y_caja - 8,
                                            x_caja + 10, y_caja + 2)

        # Refrescar info del camión activo
        if self.camion_activo:
            self.lbl_info.config(text=str(self.camion_activo))

        # Repetir ~30 veces por segundo
        self.after(33, self._bucle_animacion)


# =========================================
#   PROGRAMA PRINCIPAL
# =========================================

if __name__ == "__main__":
    app = App()
    app.mainloop()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa con menú por tecla (sin escribir ni pulsar Enter) y GUI moderna (Tkinter).
Autor: Iván
"""

import os
import sys
from typing import List

# ======================= LÓGICA PURA =======================

def celsius_a_fahrenheit(celsius: float) -> float:
    return celsius * 9.0 / 5.0 + 32.0

def tabla_multiplicar(n: int, hasta: int = 10) -> list[str]:
    return [f"{n} x {i:>2} = {n * i}" for i in range(1, hasta + 1)]

# ======================= UTILIDADES CLI =======================

def leer_float(prompt: str) -> float:
    while True:
        dato = input(prompt).strip().replace(",", ".")
        try:
            return float(dato)
        except ValueError:
            print("❌ Introduce un número válido.")

def leer_int(prompt: str) -> int:
    while True:
        dato = input(prompt).strip()
        try:
            return int(dato)
        except ValueError:
            print("❌ Introduce un número entero válido.")

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def get_single_key() -> str | None:
    """Captura una tecla (sin Enter). Compatible con Windows, Linux y macOS."""
    try:
        if os.name == "nt":
            import msvcrt  # type: ignore
            ch = msvcrt.getch()
            if ch in (b"\x00", b"\xe0"):
                _ = msvcrt.getch()
                return None
            return ch.decode("utf-8")
        else:
            import termios, tty  # type: ignore
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            return ch
    except Exception:
        return None

def espera_tecla_valida(opciones: set[str]) -> str:
    """Espera hasta que se pulse una tecla válida (sin Enter)."""
    while True:
        key = get_single_key()
        if key is None:
            sel = input("Selecciona opción: ").strip()
            if sel in opciones:
                return sel
        elif key in opciones:
            print(key)  # eco visual mínimo
            return key

# ======================= MENÚ CLI =======================

def menu_cli() -> None:
    while True:
        clear_screen()
        print("=" * 60)
        print("            🧮 MENÚ PRINCIPAL - UTILIDADES PYTHON")
        print("=" * 60)
        print("  [1] Conversión de temperatura (°C → °F)")
        print("  [2] Tabla de multiplicar")
        print("  [3] Salir")
        print("  [4] Abrir interfaz gráfica (GUI)")
        print("=" * 60)

        opcion = espera_tecla_valida({"1", "2", "3", "4"})

        if opcion == "1":
            c = leer_float("\nIntroduce los °C: ")
            print(f"{c} °C = {celsius_a_fahrenheit(c):.2f} °F")
            input("\nPresiona Enter para volver al menú...")

        elif opcion == "2":
            n = leer_int("\nNúmero entero: ")
            print()
            for linea in tabla_multiplicar(n):
                print(linea)
            input("\nPresiona Enter para volver al menú...")

        elif opcion == "3":
            print("\n👋 Programa finalizado. ¡Hasta luego!")
            break

        elif opcion == "4":
            print("\n🪟 Abriendo interfaz gráfica...")
            try:
                lanzar_gui()
            except Exception as e:
                print(f"❌ Error al abrir la GUI: {e}")
                input("\nPresiona Enter para volver al menú...")

# ======================= GUI (TKINTER) =======================

def lanzar_gui() -> None:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog

    root = tk.Tk()
    root.title("Conversor y Tablas - Iván")
    root.geometry("560x420")
    root.configure(bg="#f7f9fc")

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    primary = "#0097A7"
    primary_dark = "#007C8A"
    bg_color = "#f7f9fc"
    text_color = "#1f1f1f"

    style.configure("TButton",
        font=("Segoe UI", 10, "bold"),
        padding=6,
        foreground="white",
        background=primary,
        borderwidth=0,
        relief="flat"
    )
    style.map("TButton",
        background=[("active", primary_dark)]
    )
    style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
    style.configure("TEntry", padding=4)

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Conversión ---
    tab1 = ttk.Frame(nb)
    nb.add(tab1, text="🌡️ Conversión de temperatura")

    marco1 = ttk.LabelFrame(tab1, text="Celsius → Fahrenheit")
    marco1.pack(fill="x", padx=20, pady=20)

    var_c = tk.StringVar()
    var_f = tk.StringVar()

    fila = ttk.Frame(marco1); fila.pack(fill="x", pady=6)
    ttk.Label(fila, text="Grados Celsius:").pack(side="left", padx=(5,5))
    ent_c = ttk.Entry(fila, textvariable=var_c, width=15)
    ent_c.pack(side="left", padx=5)
    ttk.Label(fila, text="Resultado (°F):").pack(side="left", padx=(20,5))
    ent_f = ttk.Entry(fila, textvariable=var_f, width=15, state="readonly")
    ent_f.pack(side="left")

    def convertir():
        try:
            c = float(var_c.get().replace(",", ".").strip())
            var_f.set(f"{celsius_a_fahrenheit(c):.2f}")
        except ValueError:
            messagebox.showerror("Entrada no válida", "Introduce un número válido para °C.")

    ttk.Button(marco1, text="Convertir", command=convertir).pack(pady=10)

    # --- Tabla ---
    tab2 = ttk.Frame(nb)
    nb.add(tab2, text="🧮 Tabla de multiplicar")

    marco2 = ttk.LabelFrame(tab2, text="Generar tabla de multiplicar")
    marco2.pack(fill="both", expand=True, padx=20, pady=20)

    var_n = tk.StringVar()
    var_hasta = tk.StringVar(value="10")

    fila_t = ttk.Frame(marco2); fila_t.pack(fill="x", pady=6)
    ttk.Label(fila_t, text="Número:").pack(side="left", padx=(5,5))
    ent_n = ttk.Entry(fila_t, textvariable=var_n, width=10)
    ent_n.pack(side="left", padx=5)
    ttk.Label(fila_t, text="Hasta:").pack(side="left", padx=(20,5))
    ent_h = ttk.Entry(fila_t, textvariable=var_hasta, width=10)
    ent_h.pack(side="left")

    caja = tk.Text(marco2, height=12, wrap="none", bg="white", fg=text_color, font=("Consolas", 10))
    caja.pack(fill="both", expand=True, pady=10)

    def generar():
        caja.delete("1.0", "end")
        try:
            n = int(var_n.get().strip())
            h = int(var_hasta.get().strip())
            for linea in tabla_multiplicar(n, h):
                caja.insert("end", linea + "\n")
        except ValueError:
            messagebox.showerror("Entrada no válida", "Introduce enteros válidos (n y hasta).")

    def copiar():
        texto = caja.get("1.0", "end").strip()
        if texto:
            root.clipboard_clear()
            root.clipboard_append(texto)
            messagebox.showinfo("Copiado", "Tabla copiada al portapapeles.")
        else:
            messagebox.showwarning("Vacío", "No hay tabla generada.")

    def guardar():
        texto = caja.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Vacío", "No hay contenido que guardar.")
            return
        ruta = filedialog.asksaveasfilename(
            title="Guardar tabla",
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")],
            initialfile=f"tabla_{var_n.get() or 'n'}_hasta_{var_hasta.get()}.txt",
        )
        if ruta:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(texto + "\n")
            messagebox.showinfo("Guardado", "Archivo guardado correctamente.")

    barra = ttk.Frame(marco2); barra.pack(fill="x", pady=(5,0))
    ttk.Button(barra, text="Generar", command=generar).pack(side="left", padx=5)
    ttk.Button(barra, text="Copiar", command=copiar).pack(side="left", padx=5)
    ttk.Button(barra, text="Guardar .txt", command=guardar).pack(side="left", padx=5)

    root.mainloop()

# ======================= MAIN =======================

def main(argv: List[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--gui" in argv:
        lanzar_gui()
    else:
        menu_cli()

if __name__ == "__main__":
    main()

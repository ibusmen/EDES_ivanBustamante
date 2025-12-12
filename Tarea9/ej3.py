import tkinter as tk


class Objeto:
    def __init__(self, nombre, x, y, vx, vy):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def avanzar(self):
        self.x += self.vx
        self.y += self.vy


class Planeta(Objeto):
    pass


class Satelite(Objeto):
    pass


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Espacial")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack(side=tk.LEFT)

        self.info = tk.Text(root, width=30)
        self.info.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.objetos = [
            Planeta("Tierra", 200, 200, 0, 0),
            Satelite("Satélite", 250, 200, -0.5, 0.3)
        ]

        self.items = {}
        self.dibujar()

        self.btn = tk.Button(root, text="Avanzar tiempo", command=self.avanzar)
        self.btn.pack(side=tk.BOTTOM)

    def dibujar(self):
        self.canvas.delete("all")
        for o in self.objetos:
            if isinstance(o, Planeta):
                r = 15
                item = self.canvas.create_oval(o.x - r, o.y - r, o.x + r, o.y + r, fill="blue")
            else:
                r = 6
                item = self.canvas.create_oval(o.x - r, o.y - r, o.x + r, o.y + r, fill="yellow")

            self.items[item] = o
            self.canvas.tag_bind(item, "<Button-1>", self.mostrar_info)

    def avanzar(self):
        for o in self.objetos:
            o.avanzar()
        self.dibujar()

    def mostrar_info(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        obj = self.items[item]
        self.info.delete("1.0", tk.END)
        self.info.insert(tk.END, f"{obj.nombre}\nPosición: {obj.x}, {obj.y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

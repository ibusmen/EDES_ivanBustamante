class Barco:
    def __init__(self, nombre, posicionX, posicionY, velocidad, rumbo, numeroMunicion):
        self.nombre = nombre
        self.posicionX = posicionX
        self.posicionY = posicionY
        self.velocidad = velocidad
        self.rumbo = rumbo
        self.numeroMunicion = numeroMunicion

    def __str__(self):
        return (f"Nombre: {self.nombre}\n"
                f"Posición: ({self.posicionX}, {self.posicionY})\n"
                f"Velocidad: {self.velocidad} km/h\n"
                f"Rumbo: {self.rumbo}°\n"
                f"Munición restante: {self.numeroMunicion}")

    def disparar(self):
        if self.numeroMunicion > 0:
            self.numeroMunicion -= 1
            print(f"{self.nombre} ha disparado. Munición restante: {self.numeroMunicion}")
        else:
            print(f"{self.nombre} no tiene munición para disparar.")

    def setVelocidad(self, nuevaVelocidad):
        if 0 <= nuevaVelocidad <= 20:
            self.velocidad = nuevaVelocidad
            print(f"{self.nombre} ahora navega a {self.velocidad} km/h.")
        else:
            print("La velocidad debe estar entre 0 y 20 km/h.")

    def setRumbo(self, nuevoRumbo):
        if 1 <= nuevoRumbo <= 359:
            self.rumbo = nuevoRumbo
            print(f"{self.nombre} cambió su rumbo a {self.rumbo}°.")
        else:
            print("El rumbo debe estar entre 1 y 359 grados.")


# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    barco1 = Barco("Titanic", 10, 25, 15, 90, 5)
    barco2 = Barco("Poseidón", 5, 10, 12, 180, 3)
    barco3 = Barco("Nautilus", 0, 0, 8, 270, 2)

    barcos = [barco1, barco2, barco3]

    for b in barcos:
        print("\n--- Información inicial del barco ---")
        print(b)

        # Probar métodos
        b.disparar()
        b.setVelocidad(b.velocidad + 2)
        b.setRumbo(b.rumbo + 15)

        print("\n--- Información después de los cambios ---")
        print(b)
        print("-----------------------------------------")

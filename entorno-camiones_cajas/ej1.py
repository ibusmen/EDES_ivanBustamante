class Caja:
    def __init__(self, codigo, peso_kg, descripcion_carga, largo, ancho, altura):
        self.codigo = codigo
        self.peso_kg = peso_kg
        self.descripcion_carga = descripcion_carga
        self.largo = largo
        self.ancho = ancho
        self.altura = altura

    def __str__(self):
        return (f"Caja {self.codigo} - {self.descripcion_carga}\n", f"Peso: {self.peso_kg} kg\n", f"Dimensiones: {self.largo} x {self.ancho} x {self.altura} m")

class Camion:
    def __init__(self, matricula, conductor, capacidad_kg,
                 descripcion_carga, rumbo, velocidad):
        self.matricula = matricula
        self.conductor = conductor
        self.capacidad_kg = capacidad_kg
        self.descripcion_carga = descripcion_carga
        self.rumbo = rumbo
        self.velocidad = velocidad
        self.cajas = []

    def peso_total(self):
        total = 0
        for caja in self.cajas:
            total = total + caja.peso_kg
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


if __name__ == "__main__":
    caja1 = Caja("C001", 100.0, "Electrónica", 1.0, 0.8, 0.5)
    caja2 = Caja("C002", 250.0, "Ropa", 1.2, 0.9, 0.6)
    caja3 = Caja("C003", 500.0, "Herramientas", 1.5, 1.0, 0.7)

    camion = Camion("1234-ABC", "Iván", 1000.0,
                    "Carga variada", 90, 80)

    print("Estado inicial del camión:")
    print(camion)

    print("\nAñadiendo cajas...")
    camion.add_caja(caja1)
    camion.add_caja(caja2)
    camion.add_caja(caja3)

    print("\nEstado después de cargar cajas:")
    print(camion)

    print("\nProbando claxon y cambios de rumbo/velocidad:")
    camion.claxon()
    camion.setVelocidad(95)
    camion.setRumbo(120)
    print(camion)
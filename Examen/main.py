# CLASE PADRE
class Alojamiento:
    def __init__(self, codigo, direccion, ciudad, precio_por_noche, espacio_principal):
        # Atributos comunes a todos los vehículos
        self.codigo = codigo
        self.direccion = direccion
        self.ciudad = ciudad
        self.precio_por_noche = precio_por_noche
        self.espacio_principal = Espacio()
    
    def __str__(self):
        texto = f"{self.codigo}\n"
        texto += f"  Dirección: {self.direccion}\n  {self.ciudad}\n"
        return texto

# Herencia Apartamente de Alojamiento
class Apartamento(Alojamiento):
    def __init__(self, codigo, direccion, ciudad, precio_por_noche, espacio_principal, numero_planta, ascensor):
        # Llamamos al constructor del padre con super()
        super().__init__(codigo, direccion, ciudad, precio_por_noche, espacio_principal)
        self.numero_planta = numero_planta
        self.ascensor = ascensor

    def __str__(self):
        # Usamos el __str__ de Alojamiento y añadimos datos propios
        texto = super().__str__()
        texto += f"  Tipo: Apartamento\n"
        texto += f"  numero_planta: {self.numero_planta}\n"
        texto += f"  ascensor: {self.ascensor}\n"

        return texto

# Herencia Casa Rural de Alojamiento
class CasaRural(Alojamiento):
    def __init__(self, codigo, direccion, ciudad, precio_por_noche, espacio_principal, metros_jardin, chimenea):
        # Llamamos al constructor del padre con super()
        super().__init__(codigo, direccion, ciudad, precio_por_noche, espacio_principal)
        self.metros_jardin = metros_jardin
        self.chimenea = chimenea

    def __str__(self):
        # Usamos el __str__ de Alojamiento y añadimos datos propios
        texto = super().__str__()
        texto += f"  Tipo: Casa Rural\n"
        texto += f"  metros_jardin: {self.metros_jardin}\n"
        texto += f"  chimenea: {self.chimenea}\n"

        return texto

# Composición Espacio de Alojamiento
class Espacio:
    def __init__(self, nombre, metros_cuadrados, ventanas):
        # Atributos comunes a todos los vehículos
        self.metros_cuadrados = metros_cuadrados
        self.ventanas = ventanas
    
    def __str__(self):
        texto = f"{self.metros_cuadrados}\n"
        texto += f"  Tiene ventanas?: {self.ventanas}\n"
        return texto
    
class Cliente:
    def __init__(self, nombre, dni, telefono):
        self.nombre = nombre
        self.dni = dni
        self.telefono = telefono
        self.alojamiento = None  # asociación (no composición)

    def __str__(self):
        if self.alojamiento:
            return f"{self.nombre} alquila un {self.alojamiento.ciudad} {self.vehiculo.direccion}"
        else:
            return f"{self.nombre} sin alojamiento asignado"



class Agencia:
    def __init__(self, nombre, correo_contacto, ):
        self.nombre = nombre
        self.correo_contacto = correo_contacto
        self.alojamiento = []  # lista simple (agregación)

    def agregar_alojamiento(self, vehiculo):
        # AGREGACIÓN: guardamos la referencia al vehículo
        self.alojamiento.append(alojamiento)

    def __str__(self):
        texto = f"Agencia: {self.nombre}\n",  f"Correo de contacto: {self.correo_contacto}\n"
        texto += "Alojamientos almacenados:\n"
        for a in self.alojamiento:
            texto += "- " + a.__str__().replace("\n", "\n  ") + "\n"
        return texto

if __name__ == "__main__":
    apartamento1 = Apartamento("12313213", "San Federico", "San Fernando", "150€", "Salón", "Bajo", "Si")
class Objeto2D:
    def __init__(self, nombre, x, y, vx, vy):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def avanzar(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt


class CuerpoNatural(Objeto2D):
    def __init__(self, nombre, tipo, sistema, masa, x, y, vx, vy):
        super().__init__(nombre, x, y, vx, vy)
        self.tipo = tipo
        self.sistema = sistema
        self.masa = masa

    def info(self):
        return f"{self.nombre} ({self.tipo}) - Posición: ({self.x}, {self.y})"


class Planeta(CuerpoNatural):
    def __init__(self, nombre, sistema, masa, x, y, vx, vy, radio, max_satelites, atmosfera):
        super().__init__(nombre, "Planeta", sistema, masa, x, y, vx, vy)
        self.radio = radio
        self.max_satelites = max_satelites
        self.atmosfera = atmosfera


class SateliteNatural(CuerpoNatural):
    def __init__(self, nombre, sistema, masa, x, y, vx, vy, cuerpo_orbitado, distancia):
        super().__init__(nombre, "Satélite natural", sistema, masa, x, y, vx, vy)
        self.cuerpo_orbitado = cuerpo_orbitado
        self.distancia = distancia


class Cometa(CuerpoNatural):
    def __init__(self, nombre, sistema, masa, x, y, vx, vy, periodo, cola):
        super().__init__(nombre, "Cometa", sistema, masa, x, y, vx, vy)
        self.periodo = periodo
        self.cola = cola


class SistemaPropulsion:
    def __init__(self, combustible, cantidad, empuje):
        self.combustible = combustible
        self.cantidad = cantidad
        self.empuje = empuje

    def consumir(self, cantidad):
        self.cantidad = max(0, self.cantidad - cantidad)


class SistemaComunicaciones:
    def __init__(self, potencia, frecuencias, operativo=True):
        self.potencia = potencia
        self.frecuencias = frecuencias
        self.operativo = operativo

    def enviar(self, mensaje):
        if self.operativo:
            print("COMMS:", mensaje)
        else:
            print("COMMS: sistema no operativo")


class CentroControl:
    def __init__(self, nombre, pais, operadores):
        self.nombre = nombre
        self.pais = pais
        self.operadores = operadores

    def enviar_orden(self, estructura, orden):
        estructura.comunicaciones.enviar(
            f"{self.nombre} ordena: {orden}"
        )


class EstructuraArtificial(Objeto2D):
    def __init__(self, mision, agencia, pais, x, y, vx, vy, estado, propulsion, comunicaciones):
        super().__init__(mision, x, y, vx, vy)
        self.mision = mision
        self.agencia = agencia
        self.pais = pais
        self.estado = estado
        self.propulsion = propulsion
        self.comunicaciones = comunicaciones
        self.centro = None

    def asignar_centro(self, centro):
        self.centro = centro


class SateliteArtificial(EstructuraArtificial):
    def __init__(self, mision, agencia, pais, x, y, vx, vy, estado,
                 propulsion, comunicaciones, cuerpo, altura, funcion):
        super().__init__(mision, agencia, pais, x, y, vx, vy, estado, propulsion, comunicaciones)
        self.cuerpo = cuerpo
        self.altura = altura
        self.funcion = funcion


class Cohete(EstructuraArtificial):
    def __init__(self, mision, agencia, pais, x, y, vx, vy, estado,
                 propulsion, comunicaciones, empuje, carga):
        super().__init__(mision, agencia, pais, x, y, vx, vy, estado, propulsion, comunicaciones)
        self.empuje = empuje
        self.carga = carga
        self.lanzamientos = 0

    def lanzar(self):
        self.lanzamientos += 1
        self.propulsion.consumir(50)


class SistemaPlanetario:
    def __init__(self, nombre, estrella):
        self.nombre = nombre
        self.estrella = estrella
        self.cuerpos = []

    def agregar(self, cuerpo):
        self.cuerpos.append(cuerpo)


class Constelacion:
    def __init__(self, nombre, tipo_orbita):
        self.nombre = nombre
        self.tipo_orbita = tipo_orbita
        self.estructuras = []

    def agregar(self, estructura):
        self.estructuras.append(estructura)


if __name__ == "__main__":
    sistema = SistemaPlanetario("Sistema Solar", "Sol")

    tierra = Planeta("Tierra", "Sistema Solar", 5.97, 0, 0, 0, 0, 6371, 1, True)
    luna = SateliteNatural("Luna", "Sistema Solar", 0.07, 1, 0, 0, 0, "Tierra", 384400)
    sistema.agregar(tierra)
    sistema.agregar(luna)

    propulsion = SistemaPropulsion("Xenón", 100, 1.0)
    comunicaciones = SistemaComunicaciones(120, ["S", "X"])
    sat = SateliteArtificial("OBS-1", "ESA", "España", 10, 5, 0.1, 0,
                             "En lanzamiento", propulsion, comunicaciones,
                             "Tierra", 550, "Observación")

    centro = CentroControl("Centro San Fernando", "España", 10)
    sat.asignar_centro(centro)

    constelacion = Constelacion("Red Polar", "LEO")
    constelacion.agregar(sat)

    print("ESTADO INICIAL")
    print(tierra.info())
    print(luna.info())
    print("Satélite:", sat.estado)

    sat.avanzar(5)
    propulsion.consumir(20)
    sat.estado = "En órbita"
    centro.enviar_orden(sat, "Iniciar observación")

    print("\nESTADO FINAL")
    print("Satélite posición:", sat.x, sat.y)
    print("Combustible restante:", propulsion.cantidad)
    print("Estado:", sat.estado)

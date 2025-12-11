class SistemaArmas:
    def __init__(self, num_canones, num_misiles, num_torpedos):
        self.num_canones = num_canones
        self.num_misiles = num_misiles
        self.num_torpedos = num_torpedos


class SistemaSensores:
    def __init__(self, tiene_radar, tiene_sonar, rango_km):
        self.tiene_radar = tiene_radar
        self.tiene_sonar = tiene_sonar
        self.rango_deteccion_km = rango_km


class PlataformaNaval:
    def __init__(self, nombre, pais, eslora, desplazamiento, vel_max, armas, sensores):
        self.nombre = nombre
        self.pais = pais
        self.eslora = eslora
        self.desplazamiento = desplazamiento
        self.velocidad_maxima = vel_max

        self.rumbo = 0
        self.velocidad = 0
        self.integridad = 100

        # composición
        self.sistema_armas = armas
        self.sistema_sensores = sensores

        # asociación
        self.capitan = None

    def navegar(self, rumbo, velocidad):
        self.rumbo = rumbo
        self.velocidad = min(velocidad, self.velocidad_maxima)
        print(f"{self.nombre} navega a rumbo {rumbo}° a {self.velocidad} nudos.")

    def recibir_danio(self, puntos):
        self.integridad -= puntos
        if self.integridad < 0:
            self.integridad = 0
        print(f"{self.nombre} recibe {puntos} puntos de daño (integridad {self.integridad}).")

    def esta_operativa(self):
        return self.integridad > 0

    def detenerse(self):
        self.velocidad = 0

    def info(self):
        txt = f"{self.nombre} ({self.pais})\n"
        if self.capitan:
            txt += f"  Capitán: {self.capitan.nombre}\n"
        txt += f"  Integridad: {self.integridad}/100\n"
        txt += f"  Armas: Cañones={self.sistema_armas.num_canones}, "
        txt += f"Misiles={self.sistema_armas.num_misiles}, Torpedos={self.sistema_armas.num_torpedos}\n"
        txt += f"  Sensores: Radar={self.sistema_sensores.tiene_radar}, "
        txt += f"Sonar={self.sistema_sensores.tiene_sonar}\n"
        return txt


class Fragata(PlataformaNaval):
    def __init__(self, nombre, pais, eslora, desplazamiento, vel_max, misiles_aa, helis, rol):
        armas = SistemaArmas(1, misiles_aa, 4)
        sensores = SistemaSensores(True, True, 250)
        super().__init__(nombre, pais, eslora, desplazamiento, vel_max, armas, sensores)
        self.misiles_aa = misiles_aa
        self.helicopteros = helis
        self.rol = rol

    def despegar_helicoptero(self):
        if self.helicopteros > 0:
            self.helicopteros -= 1
            print(f"{self.nombre} despega un helicóptero. Restan {self.helicopteros}.")
        else:
            print(f"{self.nombre} no tiene helicópteros disponibles.")


class Corbeta(PlataformaNaval):
    def __init__(self, nombre, pais, eslora, desplazamiento, vel_max, misiles, autonomia):
        armas = SistemaArmas(1, misiles, 2)
        sensores = SistemaSensores(True, False, 180)
        super().__init__(nombre, pais, eslora, desplazamiento, vel_max, armas, sensores)
        self.misiles = misiles
        self.autonomia = autonomia


class Submarino(PlataformaNaval):
    def __init__(self, nombre, pais, eslora, desplazamiento, vel_max, prof_max, tipo_propulsion, tubos):
        armas = SistemaArmas(0, 0, tubos)
        sensores = SistemaSensores(False, True, 120)
        super().__init__(nombre, pais, eslora, desplazamiento, vel_max, armas, sensores)
        self.profundidad_maxima = prof_max
        self.profundidad_actual = 0
        self.tipo_propulsion = tipo_propulsion
        self.tubos = tubos

    def sumergirse(self, profundidad):
        if profundidad > self.profundidad_maxima:
            profundidad = self.profundidad_maxima
        self.profundidad_actual = profundidad
        print(f"{self.nombre} se sumerge a {profundidad} m.")


class Capitan:
    def __init__(self, nombre, rango, exp):
        self.nombre = nombre
        self.rango = rango
        self.experiencia = exp
        self.plataforma = None

    def asumir_mando(self, plataforma):
        self.plataforma = plataforma
        plataforma.capitan = self


class Flota:
    def __init__(self, nombre):
        self.nombre = nombre
        self.plataformas = []

    def agregar(self, p):
        if p not in self.plataformas:
            self.plataformas.append(p)

    def ordenar_ataque(self):
        print(f"\n[Flota {self.nombre}] ORDEN: Ataque general.")
        for p in self.plataformas:
            print(f"  - {p.nombre} entra en combate.")

    def mostrar_info(self):
        print(f"\n=== Flota {self.nombre} ===")
        for p in self.plataformas:
            print(p.info())

if __name__ == "__main__":
    # Capitanes
    c1 = Capitan("Ramírez", "Capitán de Fragata", 15)
    c2 = Capitan("López", "Capitán de Corbeta", 10)
    c3 = Capitan("Santos", "Capitán de Navío", 20)

    # Plataformas
    fragata = Fragata("F-101", "España", 146, 6000, 28, 16, 1, "AA")
    corbeta = Corbeta("C-21", "España", 90, 2500, 24, 8, 15)
    submarino = Submarino("S-80", "España", 80, 3000, 20, 300, "Diesel-Eléctrica", 6)

    # Asignar mandos
    c1.asumir_mando(fragata)
    c2.asumir_mando(corbeta)
    c3.asumir_mando(submarino)

    # Crear flota y añadir barcos
    flota = Flota("Flota del Atlántico")
    flota.agregar(fragata)
    flota.agregar(corbeta)
    flota.agregar(submarino)

    # Información inicial
    flota.mostrar_info()

    # Simulación
    flota.ordenar_ataque()
    fragata.navegar(90, 20)
    corbeta.recibir_danio(35)
    submarino.sumergirse(200)
    fragata.despegar_helicoptero()

    # Estado final
    print("\n== Estado final de las plataformas ==")
    for p in flota.plataformas:
        estado = "Operativa" if p.esta_operativa() else "Fuera de servicio"
        print(f"  {p.nombre} → {estado} (integridad {p.integridad})")

    print("\n== Resumen final de la flota ==")
    flota.mostrar_info()

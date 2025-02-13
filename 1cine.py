import datetime

class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

class Usuario(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)

    def hacer_reserva(self, funcion, asientos):
        reserva = Reserva(self, funcion, asientos)
        return reserva

    def acceder_a_promociones(self):
       
        pass

class Empleado(Persona):
    def __init__(self, nombre, rol):
        super().__init__(nombre)
        self.rol = rol

    def agregar_pelicula(self, titulo, duracion, clasificacion, genero):
        pelicula = Película(titulo, duracion, clasificacion, genero)
        return pelicula

    def agregar_funcion(self, pelicula, sala, horario):
        funcion = Funcion(pelicula, sala, horario)
        return funcion

    def agregar_promocion(self, nombre, descuento, pelicula=None):
        promocion = Promoción(nombre, descuento, pelicula)
        return promocion

class Espacio:
    def __init__(self, nombre):
        self.nombre = nombre

class Sala(Espacio):
    def __init__(self, nombre, tipo, capacidad):
        super().__init__(nombre)
        self.tipo = tipo
        self.capacidad = capacidad
        self.asientos_disponibles = list(range(1, capacidad + 1))  # Lista de asientos disponibles

    def mostrar_disponibilidad(self):
        print(f"Sala {self.nombre} ({self.tipo}):")
        print(f"Asientos disponibles: {self.asientos_disponibles}")

class ZonaComida(Espacio):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.productos = {}  # Diccionario para almacenar productos y precios

    def agregar_producto(self, producto, precio):
        self.productos[producto] = precio

class Película:
    def __init__(self, titulo, duracion, clasificacion, genero):
        self.titulo = titulo
        self.duracion = duracion
        self.clasificacion = clasificacion
        self.genero = genero

class Promoción:
    def __init__(self, nombre, descuento, pelicula=None):
        self.nombre = nombre
        self.descuento = descuento
        self.pelicula = pelicula  

class Reserva:
    def __init__(self, usuario, funcion, asientos):
        self.usuario = usuario
        self.funcion = funcion
        self.asientos = asientos
        self.promocion = None

    def aplicar_promocion(self, promocion):
        self.promocion = promocion

    def calcular_total(self):
        precio_base = 10  # Precio base por asiento 
        total = precio_base * len(self.asientos)
        if self.promocion:
            total *= (1 - self.promocion.descuento)
        return total

    def mostrar_asientos(self):
        print("Asientos reservados:", self.asientos)

class Funcion:
    def __init__(self, pelicula, sala, horario):
        self.pelicula = pelicula
        self.sala = sala
        self.horario = horario

    def mostrar_informacion(self):
        print(f"Película: {self.pelicula.titulo}")
        print(f"Sala: {self.sala.nombre} ({self.sala.tipo})")
        print(f"Horario: {self.horario}")

# Ejemplo de uso

# Crear personas
usuario1 = Usuario("Ana Pérez")
empleado1 = Empleado("Juan Rodríguez", "taquillero")

# Crear espacios
sala2D = Sala("Sala 1", "2D", 50)
sala3D = Sala("Sala 2", "3D", 30)
zona_comida = ZonaComida("Zona de Comida")

# Crear películas
pelicula1 = empleado1.agregar_pelicula("Oppenheimer", 180, "B", "Drama")
pelicula2 = empleado1.agregar_pelicula("Barbie", 114, "A", "Comedia")

# Crear funciones
funcion1 = empleado1.agregar_funcion(pelicula1, sala2D, datetime.datetime(2024, 3, 15, 18, 00))
funcion2 = empleado1.agregar_funcion(pelicula2, sala3D, datetime.datetime(2024, 3, 16, 20, 00))

# Crear promociones
promocion1 = empleado1.agregar_promocion("Descuento Estudiantes", 0.10)

# Mostrar disponibilidad de sala
sala2D.mostrar_disponibilidad()

# Usuario hace reserva
asientos_reservados = [5, 6, 7]
reserva1 = usuario1.hacer_reserva(funcion1, asientos_reservados)

# Mostrar asientos reservados
reserva1.mostrar_asientos()

# Aplicar promoción
reserva1.aplicar_promocion(promocion1)

# Calcular total
total = reserva1.calcular_total()
print(f"Total de la reserva: ${total}")

# Mostrar información de la función
funcion1.mostrar_informacion()
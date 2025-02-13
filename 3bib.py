import datetime

class Material:
    def __init__(self, titulo, isbn, disponible=True):
        self.titulo = titulo
        self.isbn = isbn
        self.disponible = disponible

class Libro(Material):
    def __init__(self, titulo, isbn, autor, genero, disponible=True):
        super().__init__(titulo, isbn, disponible)
        self.autor = autor
        self.genero = genero

class Revista(Material):
    def __init__(self, titulo, isbn, edicion, periodicidad, disponible=True):
        super().__init__(titulo, isbn, disponible)
        self.edicion = edicion
        self.periodicidad = periodicidad

class MaterialDigital(Material):
    def __init__(self, titulo, isbn, tipo_archivo, enlace_descarga, disponible=True):
        super().__init__(titulo, isbn, disponible)
        self.tipo_archivo = tipo_archivo
        self.enlace_descarga = enlace_descarga

class Persona:
    def __init__(self, nombre, identificacion):
        self.nombre = nombre
        self.identificacion = identificacion

class Usuario(Persona):
    def __init__(self, nombre, identificacion):
        super().__init__(nombre, identificacion)
        self.materiales_prestados = []
        self.penalizaciones = []

    def prestar_material(self, material):
        if material.disponible:
            self.materiales_prestados.append(material)
            material.disponible = False
            return True
        return False

    def devolver_material(self, material):
        if material in self.materiales_prestados:
            self.materiales_prestados.remove(material)
            material.disponible = True
            return True
        return False

    def agregar_penalizacion(self, penalizacion):
        self.penalizaciones.append(penalizacion)

class Bibliotecario(Persona):
    def __init__(self, nombre, identificacion):
        super().__init__(nombre, identificacion)

    def agregar_material(self, sucursal, material):
        sucursal.agregar_material(material)

    def gestionar_prestamo(self, usuario, material, fecha_devolucion):
        if usuario.prestar_material(material):
            prestamo = Prestamo(usuario, material, datetime.date.today(), fecha_devolucion)
            return prestamo
        return None

    def transferir_material(self, material, sucursal_origen, sucursal_destino):
        if material in sucursal_origen.catalogo:
            sucursal_origen.catalogo.remove(material)
            sucursal_destino.agregar_material(material)
            return True
        return False

class Sucursal:
    def __init__(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion
        self.catalogo = []

    def agregar_material(self, material):
        self.catalogo.append(material)

    def buscar_material(self, criterio):
        resultados = []
        for material in self.catalogo:
            if criterio.lower() in material.titulo.lower() or \
               (isinstance(material, Libro) and criterio.lower() in material.autor.lower()) or \
               (isinstance(material, Libro) and criterio.lower() in material.genero.lower()) or \
               (isinstance(material, Revista) and criterio.lower() in material.edicion.lower()):
                resultados.append(material)
        return resultados

class Prestamo:
    def __init__(self, usuario, material, fecha_prestamo, fecha_devolucion):
        self.usuario = usuario
        self.material = material
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.penalizacion = None

    def calcular_penalizacion(self):
        if datetime.date.today() > self.fecha_devolucion:
            dias_retraso = (datetime.date.today() - self.fecha_devolucion).days
            monto_penalizacion = dias_retraso * 10  # Ejemplo: 10 pesos por día de retraso
            self.penalizacion = Penalizacion(self.usuario, self, monto_penalizacion)
            self.usuario.agregar_penalizacion(self.penalizacion)
            return self.penalizacion
        return None

class Penalizacion:
    def __init__(self, usuario, prestamo, monto):
        self.usuario = usuario
        self.prestamo = prestamo
        self.monto = monto

class Catalogo:
    def __init__(self):
        self.sucursales = []

    def agregar_sucursal(self, sucursal):
        self.sucursales.append(sucursal)

    def buscar_material(self, criterio):
        resultados = []
        for sucursal in self.sucursales:
            resultados.extend(sucursal.buscar_material(criterio))
        return resultados

import datetime


# Ejemplo de uso

# Crear sucursales
sucursal1 = Sucursal("Sucursal Centro", "Calle 1 #1")
sucursal2 = Sucursal("Sucursal Norte", "Calle 2 #2")

# Crear catálogo y agregar sucursales
catalogo = Catalogo()
catalogo.agregar_sucursal(sucursal1)
catalogo.agregar_sucursal(sucursal2)

# Crear materiales
libro1 = Libro("Cien años de soledad", "978-0307957258", "Gabriel García Márquez", "Realismo mágico")
revista1 = Revista("National Geographic", "1234-5678", "Enero 2024", "Mensual")
material_digital1 = MaterialDigital("El Quijote", "978-0306817711", "PDF", "http://example.com/quijote.pdf")

# Agregar materiales a sucursales
bibliotecario1 = Bibliotecario("Ana Pérez", "12345678")
bibliotecario1.agregar_material(sucursal1, libro1)
bibliotecario1.agregar_material(sucursal1, revista1)
bibliotecario1.agregar_material(sucursal2, material_digital1)

# Buscar materiales y mostrar resultados
print("\nBúsqueda de materiales con 'soledad':")
resultados = catalogo.buscar_material("soledad")
for material in resultados:
    print(f"  - Título: {material.titulo}")
    print(f"    ISBN: {material.isbn}")
    if isinstance(material, Libro):
        print(f"    Autor: {material.autor}")
        print(f"    Género: {material.genero}")
    elif isinstance(material, Revista):
        print(f"    Edición: {material.edicion}")
        print(f"    Periodicidad: {material.periodicidad}")
    elif isinstance(material, MaterialDigital):
        print(f"    Tipo de archivo: {material.tipo_archivo}")
        print(f"    Enlace de descarga: {material.enlace_descarga}")
    print(f"    Disponible: {'Sí' if material.disponible else 'No'}")

# Prestar material
usuario1 = Usuario("Juan Rodríguez", "98765432")
fecha_devolucion = datetime.date.today() + datetime.timedelta(days=7)  # 7 días
prestamo = bibliotecario1.gestionar_prestamo(usuario1, libro1, fecha_devolucion)

if prestamo:
    print(f"\nSe prestó el libro '{libro1.titulo}' a {usuario1.nombre}.")
    print(f"  Fecha de devolución: {prestamo.fecha_devolucion}")
else:
    print(f"\nNo se pudo prestar el libro '{libro1.titulo}'.")

# Simular retraso y calcular penalización
# (Avanzar el tiempo para simular el retraso)
fecha_actual = datetime.date.today() + datetime.timedelta(days=10)  # Avanzar 10 días
prestamo.fecha_devolucion = prestamo.fecha_devolucion.replace(year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day -3) #Simula que entrego el libro 3 dias antes
if fecha_actual > prestamo.fecha_devolucion:
    prestamo.calcular_penalizacion()  

if prestamo.penalizacion:
    print(f"\nSe aplicó una penalización a {usuario1.nombre} por retraso en la devolución.")
    print(f"  Monto de la penalización: {prestamo.penalizacion.monto}")

# Transferir material
if bibliotecario1.transferir_material(material_digital1, sucursal2, sucursal1):
    print(f"\nSe transfirió el material digital '{material_digital1.titulo}' de {sucursal2.nombre} a {sucursal1.nombre}.")
else:
    print(f"\nNo se pudo transferir el material digital '{material_digital1.titulo}'.")

# Mostrar catálogo de sucursal1 después de la transferencia
print(f"\nCatálogo de {sucursal1.nombre} después de la transferencia:")
for material in sucursal1.catalogo:
    print(f"  - {material.titulo}")
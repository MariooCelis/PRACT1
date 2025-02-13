class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

class Cliente(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.historial_pedidos = []
        self.puntos_fidelidad = 0

    def realizar_pedido(self, pedido):
        self.historial_pedidos.append(pedido)
       

    def consultar_historial(self):
        for pedido in self.historial_pedidos:
            print(pedido)

class Empleado(Persona):
    def __init__(self, nombre, rol):
        super().__init__(nombre)
        self.rol = rol

class ProductoBase:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Bebida(ProductoBase):
    def __init__(self, nombre, precio, tamaño, tipo, opciones_personalizables):
        super().__init__(nombre, precio)
        self.tamaño = tamaño
        self.tipo = tipo
        self.opciones_personalizables = opciones_personalizables

class Postre(ProductoBase):
    def __init__(self, nombre, precio, es_vegano, es_sin_gluten):
        super().__init__(nombre, precio)
        self.es_vegano = es_vegano
        self.es_sin_gluten = es_sin_gluten

    def __str__(self):
        return f"{self.nombre} (Vegano: {self.es_vegano}, Sin Gluten: {self.es_sin_gluten})"

class Inventario:
    def __init__(self):
        self.ingredientes = {}  # Diccionario para almacenar ingredientes y cantidades

    def agregar_ingrediente(self, ingrediente, cantidad):
        self.ingredientes[ingrediente] = cantidad

    def verificar_stock(self, ingredientes_necesarios):
        for ingrediente, cantidad_necesaria in ingredientes_necesarios.items():
            if ingrediente not in self.ingredientes or self.ingredientes[ingrediente] < cantidad_necesaria:
                return False
        return True

    def actualizar_stock(self, ingredientes_utilizados):
        for ingrediente, cantidad_utilizada in ingredientes_utilizados.items():
            self.ingredientes[ingrediente] -= cantidad_utilizada

class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.productos = []
        self.estado = "pendiente"

    def agregar_producto(self, producto, opciones={}):
        self.productos.append({"producto": producto, "opciones": opciones})

    def calcular_total(self):
        total = 0
        for item in self.productos:
            producto = item["producto"]
            total += producto.precio
            
        return total

    def cambiar_estado(self, estado):
        self.estado = estado

    def __str__(self):
        pedido_str = f"Pedido de {self.cliente.nombre}:\n"
        for item in self.productos:
            producto = item["producto"]
            opciones = item["opciones"]
            pedido_str += f"- {producto.nombre} ({producto.tamaño if hasattr(producto, 'tamaño') else ''})"
            if opciones:
                pedido_str += " con " + ", ".join([f"{opcion} {valor}" for opcion, valor in opciones.items()])
            pedido_str += "\n"
        pedido_str += f"Total: ${self.calcular_total()}\n"
        pedido_str += f"Estado: {self.estado}"
        return pedido_str

class Promocion:
    def __init__(self, nombre, descuento, productos=[], clientes_frecuentes=True):
        self.nombre = nombre
        self.descuento = descuento
        self.productos = productos  # Lista de productos a los que aplica la promoción
        self.clientes_frecuentes = clientes_frecuentes  # Aplica solo a clientes frecuentes

    def aplicar_descuento(self, pedido):
        # Lógica para aplicar el descuento al pedido si cumple con las condiciones
        pass


# Ejemplo de uso

# Crear personas
cliente1 = Cliente("Ana Pérez")
empleado1 = Empleado("Juan Rodríguez", "mesero")

# Crear productos
cafe_con_leche = Bebida("Café con leche", 30, "Grande", "Caliente", {"leche": ["normal", "almendra", "soya"], "azúcar": ["no", "si"]})
pastel_chocolate = Postre("Pastel de chocolate", 50, False, True)

# Crear inventario
inventario = Inventario()
inventario.agregar_ingrediente("café", 100)
inventario.agregar_ingrediente("leche", 50)
inventario.agregar_ingrediente("almendra", 30)
inventario.agregar_ingrediente("azúcar", 80)
inventario.agregar_ingrediente("chocolate", 60)

# Crear pedido
pedido1 = Pedido(cliente1)

# Personalizar bebida
pedido1.agregar_producto(cafe_con_leche, {"leche": "almendra", "azúcar": "no"})
pedido1.agregar_producto(pastel_chocolate)

# Verificar inventario
ingredientes_necesarios = {"café": 1, "almendra": 1, "chocolate": 1}  # Ejemplo
if inventario.verificar_stock(ingredientes_necesarios):
    # Actualizar inventario
    inventario.actualizar_stock(ingredientes_necesarios)

    # Calcular total
    total = pedido1.calcular_total()
    print(f"Total del pedido: ${total}")

    # Cambiar estado del pedido
    pedido1.cambiar_estado("en preparación")

    # Mostrar pedido (solo una vez)
    print(pedido1)
else:
    print("No hay suficiente stock para preparar el pedido.")
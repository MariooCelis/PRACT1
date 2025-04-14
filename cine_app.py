import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class PlaceholderEntry(ttk.Entry):
    """Entry con texto de placeholder personalizado"""
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.default_fg = self['foreground']
        
        self.bind("<FocusIn>", self.clear_placeholder)
        self.bind("<FocusOut>", self.set_placeholder)
        
        self.set_placeholder()

    def clear_placeholder(self, event=None):
        if self['foreground'] == 'grey':
            self.delete(0, tk.END)
            self['foreground'] = self.default_fg

    def set_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self['foreground'] = 'grey'

class CineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CinePlus - Sistema de Gestión")
        self.root.geometry("1100x750")
        
        # Variables de estado
        self.peliculas = []
        self.salas = []
        self.funciones = []
        self.reservas = []
        self.usuario_actual = "Usuario Demo"  # Simulamos un usuario logeado
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestañas principales
        self.crear_pestana_cartelera()
        self.crear_pestana_mis_reservas()
        self.crear_pestana_administracion()
        
        # Cargar datos de ejemplo mejorados
        self.cargar_datos_ejemplo()
    
    def crear_pestana_cartelera(self):
        # Pestaña de cartelera para usuarios
        cartelera_frame = ttk.Frame(self.notebook)
        self.notebook.add(cartelera_frame, text="Cartelera")
        
        # Panel de búsqueda
        search_frame = ttk.Frame(cartelera_frame)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(search_frame, text="Buscar películas:", style='TLabel').pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.buscar_peliculas).pack(side='left', padx=5)
        
        # Filtros por género
        generos_frame = ttk.Frame(cartelera_frame)
        generos_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(generos_frame, text="Filtrar por género:", style='TLabel').pack(side='left', padx=5)
        
        self.genero_var = tk.StringVar(value="Todos")
        generos = ["Todos", "Ciencia ficción", "Fantasía", "Aventura", "Drama", "Comedia", "Acción"]
        
        for genero in generos:
            ttk.Radiobutton(generos_frame, text=genero, variable=self.genero_var, 
                          value=genero, style='TLabel').pack(side='left', padx=5)
        
        # Lista de películas con más detalles
        columns = ('Duración', 'Clasificación', 'Género', 'Director')
        self.peliculas_tree = ttk.Treeview(cartelera_frame, columns=columns, show='headings', height=8)
        
        self.peliculas_tree.heading('#0', text='Título')
        self.peliculas_tree.heading('Duración', text='Duración (min)')
        self.peliculas_tree.heading('Clasificación', text='Clasificación')
        self.peliculas_tree.heading('Género', text='Género')
        self.peliculas_tree.heading('Director', text='Director')
        
        self.peliculas_tree.column('#0', width=200)
        self.peliculas_tree.column('Duración', width=80, anchor='center')
        self.peliculas_tree.column('Clasificación', width=80, anchor='center')
        self.peliculas_tree.column('Género', width=120)
        self.peliculas_tree.column('Director', width=150)
        
        self.peliculas_tree.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Funciones disponibles
        funciones_frame = ttk.LabelFrame(cartelera_frame, text="Funciones Disponibles")
        funciones_frame.pack(fill='x', padx=10, pady=10)
        
        self.funciones_tree = ttk.Treeview(funciones_frame, columns=('Sala', 'Horario', 'Tipo'), show='headings', height=4)
        self.funciones_tree.heading('#0', text='Película')
        self.funciones_tree.heading('Sala', text='Sala')
        self.funciones_tree.heading('Horario', text='Horario')
        self.funciones_tree.heading('Tipo', text='Tipo Sala')
        
        self.funciones_tree.pack(fill='x', padx=5, pady=5)
        
        # Botones de acción
        btn_frame = ttk.Frame(cartelera_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Reservar", command=self.hacer_reserva).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ver Mis Reservas", command=self.ver_mis_reservas).pack(side='left', padx=5)
    
    def crear_pestana_mis_reservas(self):
        # Pestaña para ver reservas del usuario
        reservas_frame = ttk.Frame(self.notebook)
        self.notebook.add(reservas_frame, text="Mis Reservas")
        
        # Lista de reservas
        self.reservas_tree = ttk.Treeview(reservas_frame, columns=('Sala', 'Horario', 'Estado'), show='headings', height=10)
        
        self.reservas_tree.heading('#0', text='Película')
        self.reservas_tree.heading('Sala', text='Sala')
        self.reservas_tree.heading('Horario', text='Horario')
        self.reservas_tree.heading('Estado', text='Estado')
        
        self.reservas_tree.column('#0', width=200)
        self.reservas_tree.column('Sala', width=100, anchor='center')
        self.reservas_tree.column('Horario', width=150, anchor='center')
        self.reservas_tree.column('Estado', width=100, anchor='center')
        
        self.reservas_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botones de acción
        btn_frame = ttk.Frame(reservas_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_mis_reservas).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar Reserva", command=self.cancelar_reserva).pack(side='left', padx=5)
    
    def crear_pestana_administracion(self):
        # Pestaña para administración
        admin_frame = ttk.Frame(self.notebook)
        self.notebook.add(admin_frame, text="Administración")
        
        # Notebook para diferentes secciones
        admin_notebook = ttk.Notebook(admin_frame)
        admin_notebook.pack(fill='both', expand=True)
        
        # Pestaña Películas
        peliculas_frame = ttk.Frame(admin_notebook)
        admin_notebook.add(peliculas_frame, text="Películas")
        self.crear_formulario_peliculas(peliculas_frame)
        
        # Pestaña Salas
        salas_frame = ttk.Frame(admin_notebook)
        admin_notebook.add(salas_frame, text="Salas")
        self.crear_formulario_salas(salas_frame)
        
        # Pestaña Funciones
        funciones_frame = ttk.Frame(admin_notebook)
        admin_notebook.add(funciones_frame, text="Funciones")
        self.crear_formulario_funciones(funciones_frame)
    
    def crear_formulario_peliculas(self, frame):
        # Formulario para películas
        form = ttk.LabelFrame(frame, text="Agregar Película")
        form.pack(fill='x', padx=10, pady=10)
        
        # Campos del formulario
        ttk.Label(form, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.peli_titulo = ttk.Entry(form)
        self.peli_titulo.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form, text="Duración (min):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.peli_duracion = ttk.Entry(form)
        self.peli_duracion.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form, text="Clasificación:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.peli_clasificacion = ttk.Combobox(form, values=["A", "B", "B15", "C", "D"])
        self.peli_clasificacion.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form, text="Género:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.peli_genero = ttk.Combobox(form, values=["Ciencia ficción", "Fantasía", "Aventura", "Drama", "Comedia", "Acción"])
        self.peli_genero.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form, text="Director:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.peli_director = ttk.Entry(form)
        self.peli_director.grid(row=4, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Button(form, text="Agregar Película", command=self.agregar_pelicula).grid(row=5, columnspan=2, pady=10)
    
    def crear_formulario_salas(self, frame):
        # Formulario para salas
        form = ttk.LabelFrame(frame, text="Agregar Sala")
        form.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.sala_nombre = ttk.Entry(form)
        self.sala_nombre.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form, text="Tipo:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.sala_tipo = ttk.Combobox(form, values=["2D", "3D", "4DX", "VIP", "IMAX"])
        self.sala_tipo.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form, text="Capacidad:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.sala_capacidad = ttk.Entry(form)
        self.sala_capacidad.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Button(form, text="Agregar Sala", command=self.agregar_sala).grid(row=3, columnspan=2, pady=10)
    
    def crear_formulario_funciones(self, frame):
        # Formulario para funciones
        form = ttk.LabelFrame(frame, text="Agregar Función")
        form.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form, text="Película:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.func_pelicula = ttk.Combobox(form)
        self.func_pelicula.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form, text="Sala:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.func_sala = ttk.Combobox(form)
        self.func_sala.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form, text="Fecha y hora:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.func_fecha = PlaceholderEntry(form, placeholder="YYYY-MM-DD HH:MM")
        self.func_fecha.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Button(form, text="Agregar Función", command=self.agregar_funcion).grid(row=3, columnspan=2, pady=10)
    
    def cargar_datos_ejemplo(self):
        # Películas de ejemplo con sus géneros 
        self.peliculas = [
            {"titulo": "Star Wars: Episodio IV - Una nueva esperanza", "duracion": 121, "clasificacion": "A", 
             "genero": "Ciencia ficción", "director": "George Lucas"},
            {"titulo": "Harry Potter y la piedra filosofal", "duracion": 152, "clasificacion": "A", 
             "genero": "Fantasía", "director": "Chris Columbus"},
            {"titulo": "El Señor de los Anillos: La Comunidad del Anillo", "duracion": 178, "clasificacion": "B", 
             "genero": "Fantasía", "director": "Peter Jackson"},
            {"titulo": "Avengers: Endgame", "duracion": 181, "clasificacion": "B", 
             "genero": "Acción", "director": "Anthony y Joe Russo"},
            {"titulo": "Toy Story", "duracion": 81, "clasificacion": "A", 
             "genero": "Animación", "director": "John Lasseter"},
            {"titulo": "El Padrino", "duracion": 175, "clasificacion": "C", 
             "genero": "Drama", "director": "Francis Ford Coppola"},
            {"titulo": "Jurassic Park", "duracion": 127, "clasificacion": "A", 
             "genero": "Aventura", "director": "Steven Spielberg"},
            {"titulo": "Forrest Gump", "duracion": 142, "clasificacion": "B", 
             "genero": "Drama", "director": "Robert Zemeckis"}
        ]
        
        # Salas de ejemplo
        self.salas = [
            {"nombre": "Sala 1", "tipo": "3D", "capacidad": "120"},
            {"nombre": "Sala 2", "tipo": "4DX", "capacidad": "80"},
            {"nombre": "Sala 3", "tipo": "IMAX", "capacidad": "150"},
            {"nombre": "Sala 4", "tipo": "2D", "capacidad": "100"},
            {"nombre": "Sala VIP", "tipo": "VIP", "capacidad": "50"}
        ]
        
        # Funciones de ejemplo
        self.funciones = [
            {"pelicula": "Star Wars: Episodio IV - Una nueva esperanza", "sala": "Sala 1", 
             "horario": "2023-12-15 18:00", "tipo": "3D"},
            {"pelicula": "Harry Potter y la piedra filosofal", "sala": "Sala 3", 
             "horario": "2023-12-15 20:30", "tipo": "IMAX"},
            {"pelicula": "El Señor de los Anillos: La Comunidad del Anillo", "sala": "Sala 2", 
             "horario": "2023-12-16 17:00", "tipo": "4DX"},
            {"pelicula": "Avengers: Endgame", "sala": "Sala 1", 
             "horario": "2023-12-16 21:00", "tipo": "3D"},
            {"pelicula": "Toy Story", "sala": "Sala 4", 
             "horario": "2023-12-17 15:00", "tipo": "2D"},
            {"pelicula": "Jurassic Park", "sala": "Sala VIP", 
             "horario": "2023-12-17 19:30", "tipo": "VIP"}
        ]
        
        # Algunas reservas de ejemplo
        self.reservas = [
            {"usuario": self.usuario_actual, "pelicula": "Star Wars: Episodio IV - Una nueva esperanza", 
             "sala": "Sala 1", "horario": "2023-12-15 18:00", "estado": "Confirmada"},
            {"usuario": self.usuario_actual, "pelicula": "Harry Potter y la piedra filosofal", 
             "sala": "Sala 3", "horario": "2023-12-15 20:30", "estado": "Confirmada"}
        ]
        
        self.actualizar_listas()
        self.actualizar_mis_reservas()
    
    def actualizar_listas(self):
        
        self.peliculas_tree.delete(*self.peliculas_tree.get_children())
        for pelicula in self.peliculas:
            self.peliculas_tree.insert('', 'end', text=pelicula["titulo"], 
                                     values=(pelicula["duracion"], pelicula["clasificacion"], 
                                             pelicula["genero"], pelicula["director"]))
        
        
        self.func_pelicula['values'] = [p["titulo"] for p in self.peliculas]
        
        
        self.func_sala['values'] = [s["nombre"] for s in self.salas]
        
        
        self.funciones_tree.delete(*self.funciones_tree.get_children())
        for funcion in self.funciones:
            self.funciones_tree.insert('', 'end', text=funcion["pelicula"], 
                                     values=(funcion["sala"], funcion["horario"], funcion["tipo"]))
    
    def actualizar_mis_reservas(self):
        self.reservas_tree.delete(*self.reservas_tree.get_children())
        for reserva in self.reservas:
            if reserva["usuario"] == self.usuario_actual:
                self.reservas_tree.insert('', 'end', text=reserva["pelicula"], 
                                        values=(reserva["sala"], reserva["horario"], reserva["estado"]))
    
    def buscar_peliculas(self):
        termino = self.search_entry.get().lower()
        genero_seleccionado = self.genero_var.get()
        
        self.peliculas_tree.delete(*self.peliculas_tree.get_children())
        
        for pelicula in self.peliculas:
            cumple_termino = termino == "" or termino in pelicula["titulo"].lower() or termino in pelicula["director"].lower()
            cumple_genero = genero_seleccionado == "Todos" or genero_seleccionado == pelicula["genero"]
            
            if cumple_termino and cumple_genero:
                self.peliculas_tree.insert('', 'end', text=pelicula["titulo"], 
                                         values=(pelicula["duracion"], pelicula["clasificacion"], 
                                                 pelicula["genero"], pelicula["director"]))
    
    def agregar_pelicula(self):
        if not all([self.peli_titulo.get(), self.peli_duracion.get(), 
                   self.peli_clasificacion.get(), self.peli_genero.get(), self.peli_director.get()]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        nueva_pelicula = {
            "titulo": self.peli_titulo.get(),
            "duracion": self.peli_duracion.get(),
            "clasificacion": self.peli_clasificacion.get(),
            "genero": self.peli_genero.get(),
            "director": self.peli_director.get()
        }
        self.peliculas.append(nueva_pelicula)
        self.actualizar_listas()
        
        # Limpiar campos
        self.peli_titulo.delete(0, tk.END)
        self.peli_duracion.delete(0, tk.END)
        self.peli_clasificacion.set('')
        self.peli_genero.set('')
        self.peli_director.delete(0, tk.END)
        
        messagebox.showinfo("Éxito", "Película agregada correctamente")
    
    def agregar_sala(self):
        if not all([self.sala_nombre.get(), self.sala_tipo.get(), self.sala_capacidad.get()]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        nueva_sala = {
            "nombre": self.sala_nombre.get(),
            "tipo": self.sala_tipo.get(),
            "capacidad": self.sala_capacidad.get()
        }
        self.salas.append(nueva_sala)
        self.actualizar_listas()
        
        # Limpiar campos
        self.sala_nombre.delete(0, tk.END)
        self.sala_tipo.set('')
        self.sala_capacidad.delete(0, tk.END)
        
        messagebox.showinfo("Éxito", "Sala agregada correctamente")
    
    def agregar_funcion(self):
        if not all([self.func_pelicula.get(), self.func_sala.get(), self.func_fecha.get()]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Validar formato de fecha
        try:
            datetime.strptime(self.func_fecha.get(), "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD HH:MM")
            return
        
        # Obtener tipo de sala
        sala_seleccionada = next((s for s in self.salas if s["nombre"] == self.func_sala.get()), None)
        tipo_sala = sala_seleccionada["tipo"] if sala_seleccionada else "2D"
        
        nueva_funcion = {
            "pelicula": self.func_pelicula.get(),
            "sala": self.func_sala.get(),
            "horario": self.func_fecha.get(),
            "tipo": tipo_sala
        }
        self.funciones.append(nueva_funcion)
        self.actualizar_listas()
        
        # Limpiar campos
        self.func_pelicula.set('')
        self.func_sala.set('')
        self.func_fecha.delete(0, tk.END)
        self.func_fecha.set_placeholder()  # Restablecer el placeholder
        
        messagebox.showinfo("Éxito", "Función agregada correctamente")
    
    def hacer_reserva(self):
        seleccion = self.funciones_tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione una función para reservar")
            return
        
        funcion = self.funciones_tree.item(seleccion[0])
        
        nueva_reserva = {
            "usuario": self.usuario_actual,
            "pelicula": funcion['text'],
            "sala": funcion['values'][0],
            "horario": funcion['values'][1],
            "estado": "Confirmada"
        }
        
        self.reservas.append(nueva_reserva)
        self.actualizar_mis_reservas()
        
        messagebox.showinfo("Reserva Exitosa", 
                          f"Reserva confirmada para:\n"
                          f"Película: {funcion['text']}\n"
                          f"Sala: {funcion['values'][0]} ({funcion['values'][2]})\n"
                          f"Horario: {funcion['values'][1]}")
    
    def ver_mis_reservas(self):
        self.notebook.select(1)  # Cambiar a la pestaña de reservas
        self.actualizar_mis_reservas()
    
    def cancelar_reserva(self):
        seleccion = self.reservas_tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione una reserva para cancelar")
            return
        
        reserva = self.reservas_tree.item(seleccion[0])
        
        # Buscar y eliminar la reserva
        for i, r in enumerate(self.reservas):
            if (r["usuario"] == self.usuario_actual and 
                r["pelicula"] == reserva['text'] and 
                r["horario"] == reserva['values'][1]):
                del self.reservas[i]
                break
        
        self.actualizar_mis_reservas()
        messagebox.showinfo("Reserva Cancelada", "Su reserva ha sido cancelada exitosamente")

if __name__ == "__main__":
    root = tk.Tk()
    app = CineGUI(root)
    root.mainloop()

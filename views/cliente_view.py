from tkinter import ttk, StringVar, messagebox
from views.base_view import BaseView
from controllers.cliente_controller import ClienteController

class ClienteView(BaseView):
    def __init__(self, master=None):
        self.controller = ClienteController()
        super().__init__(master)

    def setup_ui(self):
        # Variables
        self.id_var = StringVar()
        self.cedula_var = StringVar()
        self.nombre_var = StringVar()
        self.telefono_var = StringVar()

        # Centrar contenido: crear un contenedor centrado
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        container = ttk.Frame(self.frame)
        container.grid(row=0, column=0, columnspan=2, pady=10)

        # Frame de datos
        data_frame = ttk.LabelFrame(container, text="Datos del Cliente", padding=12)
        data_frame.grid(row=0, column=0, padx=10, pady=5)
        # Hacer que la columna de inputs sea más ancha
        data_frame.columnconfigure(0, weight=0)
        data_frame.columnconfigure(1, weight=1)

        # Campos
        ttk.Label(data_frame, text="Cédula:").grid(row=0, column=0, sticky="w")
        cedula_entry = ttk.Entry(data_frame, textvariable=self.cedula_var)
        cedula_entry.grid(row=0, column=1, padx=5, pady=2)
        # Validación: solo números
        cedula_entry.bind('<KeyRelease>', lambda e: self.validar_solo_numeros(self.cedula_var))

        ttk.Label(data_frame, text="Nombre:").grid(row=1, column=0, sticky="w")
        nombre_entry = ttk.Entry(data_frame, textvariable=self.nombre_var)
        nombre_entry.grid(row=1, column=1, padx=5, pady=2)
        # Validación: solo letras y espacios, convertir a mayúsculas
        nombre_entry.bind('<KeyRelease>', lambda e: self.validar_solo_letras(self.nombre_var))

        ttk.Label(data_frame, text="Teléfono:").grid(row=2, column=0, sticky="w")
        telefono_entry = ttk.Entry(data_frame, textvariable=self.telefono_var)
        telefono_entry.grid(row=2, column=1, padx=5, pady=2)
        # Validación: solo números y algunos caracteres especiales
        telefono_entry.bind('<KeyRelease>', lambda e: self.validar_telefono(self.telefono_var))

        # Botones centrados
        button_frame = ttk.Frame(container)
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Guardar", command=self.save, style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Modificar", command=self.update, style='Info.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.delete, style='Danger.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_fields, style='Warning.TButton').grid(row=0, column=3, padx=5)

        # Frame de búsqueda
        search_frame = ttk.LabelFrame(container, text="Búsqueda", padding=10)
        search_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, padx=5)
        self.criterio_busqueda_var = StringVar(value="Cedula")
        criterio_combo = ttk.Combobox(search_frame, textvariable=self.criterio_busqueda_var, 
                                     values=["Cedula", "Nombre", "Telefono"], 
                                     state="readonly", width=10)
        criterio_combo.grid(row=0, column=1, padx=5)

        self.busqueda_var = StringVar()
        ttk.Entry(search_frame, textvariable=self.busqueda_var, width=30).grid(row=0, column=2, padx=5)

        ttk.Button(search_frame, text="Buscar", command=self.buscar_clientes, style='Info.TButton').grid(row=0, column=3, padx=5)
        ttk.Button(search_frame, text="Limpiar", command=self.limpiar_busqueda, style='Warning.TButton').grid(row=0, column=4, padx=5)

        # Tabla centrada
        table_wrap = ttk.Frame(container)
        table_wrap.grid(row=3, column=0, pady=10)
        self.tree = ttk.Treeview(table_wrap, columns=("Cedula", "Nombre", "Telefono"), show="headings", height=8)
        self.tree.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(table_wrap, orient='vertical', command=self.tree.yview)
        sb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=sb.set)

        # Configurar columnas
        self.tree.heading("Cedula", text="Cédula", anchor="center")
        self.tree.heading("Nombre", text="Nombre", anchor="center")
        self.tree.heading("Telefono", text="Teléfono", anchor="center")

        self.tree.column("Cedula", anchor="center")
        self.tree.column("Nombre", anchor="center")
        self.tree.column("Telefono", anchor="center")

        # Bind para selección
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Cargar datos
        self.load_data()

    def clear_fields(self):
        self.id_var.set("")
        self.cedula_var.set("")
        self.nombre_var.set("")
        self.telefono_var.set("")

    def load_data(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Cargar datos
        try:
            clientes = self.controller.get_all()
            for cliente in clientes:
                self.tree.insert("", "end", values=(
                    cliente.cedula,
                    cliente.nombre,
                    cliente.telefono
                ), tags=(str(cliente.id),))  # Guardar ID en tags para uso interno
        except Exception as e:
            self.show_error(f"Error al cargar datos: {str(e)}")

    def save(self):
        try:
            # Validaciones
            cedula = self.cedula_var.get().strip()
            nombre = self.nombre_var.get().strip()
            telefono = self.telefono_var.get().strip()
            
            if not cedula:
                self.show_warning("La cédula es obligatoria")
                return
            
            if not nombre:
                self.show_warning("El nombre es obligatorio")
                return
            
            if not telefono:
                self.show_warning("El teléfono es obligatorio")
                return
            
            if len(cedula) < 6:
                self.show_warning("La cédula debe tener al menos 6 dígitos")
                return
            
            if len(nombre) < 3:
                self.show_warning("El nombre debe tener al menos 3 caracteres")
                return
            
            if len(telefono) < 7:
                self.show_warning("El teléfono debe tener al menos 7 dígitos")
                return
            
            self.controller.create(
                cedula=cedula,
                nombre=nombre,
                telefono=telefono
            )
            self.show_info("Cliente guardado exitosamente")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            self.show_error(f"Error al guardar: {str(e)}")

    def update(self):
        try:
            if not self.id_var.get():
                self.show_warning("Seleccione un cliente para modificar")
                return

            # Validaciones
            cedula = self.cedula_var.get().strip()
            nombre = self.nombre_var.get().strip()
            telefono = self.telefono_var.get().strip()
            
            if not cedula:
                self.show_warning("La cédula es obligatoria")
                return
            
            if not nombre:
                self.show_warning("El nombre es obligatorio")
                return
            
            if not telefono:
                self.show_warning("El teléfono es obligatorio")
                return
            
            if len(cedula) < 6:
                self.show_warning("La cédula debe tener al menos 6 dígitos")
                return
            
            if len(nombre) < 3:
                self.show_warning("El nombre debe tener al menos 3 caracteres")
                return
            
            if len(telefono) < 7:
                self.show_warning("El teléfono debe tener al menos 7 dígitos")
                return

            self.controller.update(
                id=self.id_var.get(),
                cedula=cedula,
                nombre=nombre,
                telefono=telefono
            )
            self.show_info("Cliente actualizado exitosamente")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            self.show_error(f"Error al actualizar: {str(e)}")

    def delete(self):
        try:
            if not self.id_var.get():
                self.show_warning("Seleccione un cliente para eliminar")
                return

            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
                self.controller.delete(self.id_var.get())
                self.show_info("Cliente eliminado exitosamente")
                self.clear_fields()
                self.load_data()
        except Exception as e:
            self.show_error(f"Error al eliminar: {str(e)}")

    def buscar_clientes(self):
        """Buscar clientes según el criterio seleccionado"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            clientes = self.controller.get_all()
            busqueda = self.busqueda_var.get().upper()
            criterio = self.criterio_busqueda_var.get()

            for cliente in clientes:
                mostrar = False
                
                if criterio == "Cedula" and busqueda in cliente.cedula:
                    mostrar = True
                elif criterio == "Nombre" and busqueda in cliente.nombre.upper():
                    mostrar = True
                elif criterio == "Telefono" and busqueda in cliente.telefono:
                    mostrar = True

                if mostrar:
                    self.tree.insert("", "end", values=(
                        cliente.cedula,
                        cliente.nombre,
                        cliente.telefono
                    ), tags=(str(cliente.id),))
        except Exception as e:
            self.show_error(f"Error al buscar: {str(e)}")

    def limpiar_busqueda(self):
        """Limpiar búsqueda y mostrar todos los clientes"""
        self.busqueda_var.set("")
        self.load_data()

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        # Obtener ID del tag
        item_id = self.tree.item(selected[0])["tags"][0]
        values = self.tree.item(selected[0])["values"]
        
        self.id_var.set(item_id)
        self.cedula_var.set(values[0])
        self.nombre_var.set(values[1])
        self.telefono_var.set(values[2])
    
    def validar_solo_numeros(self, variable):
        """Permite solo numeros en un campo"""
        valor = variable.get()
        # Remover todo lo que no sea digito
        valor_limpio = ''.join(filter(str.isdigit, valor))
        if valor != valor_limpio:
            variable.set(valor_limpio)
    
    def validar_solo_letras(self, variable):
        """Permite solo letras y espacios, convierte a mayusculas"""
        valor = variable.get()
        # Permitir solo letras, espacios y algunos caracteres especiales del espanol
        valor_limpio = ''.join(c for c in valor if c.isalpha() or c.isspace())
        valor_limpio = valor_limpio.upper()
        if valor != valor_limpio:
            variable.set(valor_limpio)
    
    def validar_telefono(self, variable):
        """Permite numeros, espacios, guiones, parentesis y simbolo +"""
        valor = variable.get()
        # Permitir solo digitos, espacios, guiones, parentesis y +
        valor_limpio = ''.join(c for c in valor if c.isdigit() or c in ' -()+ ')
        if valor != valor_limpio:
            variable.set(valor_limpio)

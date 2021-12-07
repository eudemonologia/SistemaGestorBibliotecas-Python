from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from types import FunctionType
from typing import Dict
import controlador


def iniciar(nombre_usuario: str) -> None:
    # Crear la ventana principal
    ventana = componente_ventana(nombre_usuario)

    # Variables
    variables_libro = {
        "id_libro": IntVar(),
        "estado_libro": StringVar(),
        "titulo_libro": StringVar(),
        "autor_libro": StringVar(),
        "editorial_libro": StringVar(),
        "estante_libro": StringVar(),
    }
    listas = traer_listas()
    palabra_buscar = StringVar()

    # Frame de la tabla de libros
    frame_tabla = ttk.Frame(ventana)
    frame_tabla.pack(pady=10, padx=20)

    # Tabla de libros con scroll
    tabla_scroll = ttk.Scrollbar(frame_tabla)
    tabla_scroll.pack(side=RIGHT, fill=Y)
    tabla_libros = ttk.Treeview(
        frame_tabla, yscrollcommand=tabla_scroll.set, selectmode="extended", height=18)
    tabla_libros.pack()
    tabla_scroll.config(command=tabla_libros.yview)

    # Columnas de la tabla
    tabla_libros["columns"] = (
        "Id", "Estado", "Titulo", "Autor", "Editorial", "Estante")
    tabla_libros.column("#0", width=0, stretch=NO)
    tabla_libros.column("Id", anchor=CENTER, width=50)
    tabla_libros.column("Estado", anchor=CENTER, width=100)
    tabla_libros.column("Titulo", anchor=W, width=250)
    tabla_libros.column("Autor", anchor=CENTER, width=200)
    tabla_libros.column("Editorial", anchor=CENTER, width=200)
    tabla_libros.column("Estante", anchor=CENTER, width=200)

    # Encabezados de la tabla
    tabla_libros.heading("Id", text="Id", anchor=CENTER, command=lambda: ordenar_tabla(
        tabla_libros, "Id", True))
    tabla_libros.heading("Estado", text="Estado", anchor=CENTER, command=lambda: ordenar_tabla(
        tabla_libros, "Estado", False))
    tabla_libros.heading("Titulo", text="Titulo", anchor=CENTER, command=lambda: ordenar_tabla(
        tabla_libros, "Titulo", False))
    tabla_libros.heading("Autor", text="Autor", anchor=CENTER, command=lambda: ordenar_tabla(
        tabla_libros, "Autor", False))
    tabla_libros.heading("Editorial", text="Editorial", anchor=CENTER, command=lambda: ordenar_tabla(
        tabla_libros, "Editorial", False))
    tabla_libros.heading("Estante", text="Estante", anchor=CENTER, command=lambda: ordenar_tabla(
        tabla_libros, "Estante", False))

    # Sumar contenido a la tabla
    refrescar_contenido(tabla_libros)

    # Frame bucador de libros
    frame_buscar = ttk.LabelFrame(ventana, text="Busqueda")
    frame_buscar.pack(fill="x", expand="yes", pady=10, padx=20)

    # Entrada de buscar
    entrada_buscar = ttk.Entry(
        frame_buscar, textvariable=palabra_buscar)
    entrada_buscar.pack(fill="x", side=RIGHT, expand="yes",
                        pady=10, padx=10, ipady=2)
    entrada_buscar.bind("<Return>", lambda event: handle_btn_buscar(
        palabra_buscar, tabla_libros))

    # Boton de buscar
    componente_boton(frame_buscar, "Buscar",
                     lambda: handle_btn_buscar(palabra_buscar, tabla_libros))

    # Frame de ingreso de libros
    frame_ingreso = ttk.LabelFrame(ventana, text="Registro")
    frame_ingreso.grid_columnconfigure(0, weight=1)
    frame_ingreso.grid_columnconfigure(1, weight=2)
    frame_ingreso.grid_columnconfigure(2, weight=1)
    frame_ingreso.grid_columnconfigure(3, weight=2)
    frame_ingreso.grid_columnconfigure(4, weight=1)
    frame_ingreso.grid_columnconfigure(5, weight=2)
    frame_ingreso.grid_columnconfigure(6, weight=1)
    frame_ingreso.grid_columnconfigure(7, weight=2)

    # Campos de ingreso de libros
    componente_label_and_input(
        frame_ingreso, variables_libro["id_libro"], "Id: ", 0, 0, "readonly")

    componente_label(frame_ingreso, "Estado: ", 0, 2)
    componente_radiobutton(frame_ingreso, "Nuevo", "Nuevo",
                           variables_libro["estado_libro"], 0, 3)
    componente_radiobutton(frame_ingreso, "Leyendo", "Leyendo",
                           variables_libro["estado_libro"], 0, 4)
    componente_radiobutton(frame_ingreso, "Leído", "Leído",
                           variables_libro["estado_libro"], 0, 5)
    componente_radiobutton(frame_ingreso, "Perdido", "Perdido",
                           variables_libro["estado_libro"], 0, 6)

    componente_label_and_input(
        frame_ingreso, variables_libro["titulo_libro"], "Titulo: ", 1, 0)
    componente_label(frame_ingreso, "Autor: ", 1, 2)
    componente_combo(frame_ingreso, variables_libro["autor_libro"],
                     listas["autores"], 1, 3)
    componente_label(frame_ingreso, "Editorial: ", 1, 4)
    componente_combo(
        frame_ingreso, variables_libro["editorial_libro"], listas["editoriales"], 1, 5)
    componente_label(frame_ingreso, "Estante: ", 1, 6)
    componente_combo(
        frame_ingreso, variables_libro["estante_libro"], listas["estantes"], 1, 7)

    # Frame de botones
    frame_botones = ttk.LabelFrame(ventana, text="Botones")
    frame_botones.pack(fill="x", expand="yes", pady=10, padx=20)

    # Botones
    btn_nuevo = componente_boton(frame_botones, "Nuevo",
                                 lambda: handle_btn_nuevo(tabla_libros, frame_ingreso, frame_botones, btn_nuevo, btn_modificar, variables_libro))
    btn_modificar = componente_boton(frame_botones, "Modificar",
                                     lambda: handle_btn_modificar(tabla_libros, frame_ingreso, frame_botones, btn_nuevo, btn_modificar, variables_libro))
    componente_boton(frame_botones, "Eliminar",
                     lambda: handle_btn_eliminar(tabla_libros))
    componente_boton(frame_botones, "Exportar",
                     lambda: handle_btn_exportar(tabla_libros))
    componente_boton(frame_botones, "Importar",
                     lambda: handle_btn_importar(tabla_libros))
    componente_boton(frame_botones, "Refrescar",
                     lambda: refrescar_contenido(tabla_libros))

    mainloop()


"""
Componentes de la vista
"""


def componente_ventana(nombre_usuario: str) -> Tk:
    """
    Crea una ventana con el nombre del usuario
    """
    una_ventana = Tk()
    una_ventana.title("Biblioteca de " + nombre_usuario)
    una_ventana.resizable(0, 0)
    una_ventana.iconbitmap("./assets/icono.ico")
    return una_ventana


def componente_label_and_input(frame: LabelFrame, variable: Variable, texto: str, fila: int, columna: int, estado: str = "normal") -> None:
    """Crea un label y un input en un frame."""
    componente_label(frame, texto, fila, columna)
    componente_input(frame, variable, fila, columna + 1, estado)


def componente_label_and_combo(frame: LabelFrame, variable: Variable, lista: list, texto: str, fila: int, columna: int) -> None:
    """Crea un label y un combo en un frame."""
    componente_label(frame, texto, fila, columna)
    componente_combo(frame, variable, lista, fila, columna + 1,)


def componente_label(frame: LabelFrame, texto: str, fila: int, columna: int) -> Label:
    """Crea un label en un frame."""
    un_label = ttk.Label(frame, text=texto)
    un_label.grid(row=fila, column=columna, padx=10, pady=10, sticky=W)
    return un_label


def componente_input(frame: LabelFrame, variable: StringVar, fila: int, columna: int, estado: str = "normal") -> ttk.Entry:
    """Crea un input en un frame."""
    un_input = ttk.Entry(frame, textvariable=variable, state=estado)
    un_input.grid(row=fila, column=columna, padx=10, pady=10, sticky="we")
    return un_input


def componente_combo(frame: LabelFrame, variable: StringVar, lista: list, fila: int, columna: int) -> ttk.Combobox:
    """Crea un combo en un frame."""
    un_combo = ttk.Combobox(frame, textvariable=variable)
    un_combo['values'] = lista
    un_combo.bind("<KeyRelease>", lambda e: check_input_combo(
        un_combo, variable, lista))
    un_combo.grid(row=fila, column=columna, padx=10, pady=10, sticky="we")
    return un_combo


def componente_boton(frame: LabelFrame, texto: str, comando: FunctionType, lado: str = LEFT) -> ttk.Button:
    """Crea un boton en un frame."""
    un_boton = ttk.Button(frame, text=texto, command=comando)
    un_boton.pack(side=lado, pady=10, padx=10)
    return un_boton


def componente_radiobutton(frame: LabelFrame, texto: str, valor: str, variable: StringVar, fila: int, columna: int) -> None:
    """Crea un radiobutton en un frame."""
    un_radio = ttk.Radiobutton(
        frame, text=texto, value=valor, variable=variable)
    un_radio.grid(row=fila, column=columna, padx=10, pady=10)


"""
Acciones de la vista
"""


def traer_listas() -> Dict:
    """Trae las listas de autores, editoriales, estantes y libros."""
    libros = controlador.traer_libros()
    autores = sorted(list({e[3] for e in libros}))
    editoriales = sorted(list({e[4] for e in libros}))
    estantes = sorted(list({e[5] for e in libros}))
    return {
        "libros": libros,
        "autores": autores,
        "editoriales": editoriales,
        "estantes": estantes,
    }


def refrescar_contenido(tabla: ttk.Treeview) -> None:
    """Refrasca el contenido de la tabla."""
    lista_libros = controlador.traer_libros()
    tabla.delete(*tabla.get_children())
    for libro in lista_libros:
        tabla.insert("", END, values=libro)


def ordenar_tabla(tabla: ttk.Treeview, columna: str, reversa: bool) -> None:
    """Ordena la tabla por una columna."""
    nueva_lista = [(tabla.set(k, columna), k) for k in tabla.get_children()]
    nueva_lista.sort(reverse=reversa)
    for index, (val, k) in enumerate(nueva_lista):
        tabla.move(k, '', index)
    tabla.heading(columna, command=lambda: ordenar_tabla(
        tabla, columna, not reversa))


def check_input_combo(combo: ttk.Combobox, variable: StringVar, lista: list) -> None:
    """Verifica que el input del combo esté en la lista."""
    if variable.get() == "":
        combo['values'] = lista
    else:
        data = []
        for e in lista:
            if variable.get().lower() in e.lower():
                data.append(e)
        if len(data) == 0:
            combo['values'] = lista
        if len(data) > 0:
            combo['values'] = data


def handle_btn_buscar(palabra_buscar: StringVar, tabla: ttk.Treeview) -> None:
    """Busca un libro en la tabla."""
    tabla.delete(*tabla.get_children())
    lista_libros = controlador.buscar(palabra_buscar.get())
    if len(lista_libros) == 0:
        messagebox.showinfo("Error", "No se encontró nigún libro")
    else:
        for libro in lista_libros:
            tabla.insert("", END, values=libro)


def handle_btn_nuevo(tabla: ttk.Treeview, frame_mostrar: LabelFrame, frame_botones: LabelFrame, boton_principal: Button, boton_secundario: Button, variables: Dict) -> None:
    """Manejador del boton nuevo."""
    boton_principal.config(state="disabled")
    boton_secundario.config(state="disabled")
    btn_cancelar = componente_boton(frame_botones, "Cancelar", lambda: handle_btn_cancelar(
        frame_mostrar, boton_principal, boton_secundario, btn_guardar, btn_cancelar), RIGHT)
    btn_guardar = componente_boton(frame_botones, "Guardar", lambda: handle_btn_guardar_nuevo(
        tabla, frame_mostrar, variables, boton_principal, boton_secundario, btn_guardar, btn_cancelar), RIGHT)
    frame_mostrar.pack(fill="x", expand="yes", pady=10, padx=20)
    variables["id_libro"].set(controlador.id_ultimo_libro())
    variables["estado_libro"].set("Nuevo")
    variables["titulo_libro"].set("")
    variables["autor_libro"].set("")
    variables["editorial_libro"].set("")
    variables["estante_libro"].set("")


def handle_btn_guardar_nuevo(tabla: ttk.Treeview, frame_mostrar: LabelFrame, variables: dict, boton_principal: Button, boton_secundario: Button, boton_borrar_primero: Button, boton_borrar_segundo: Button) -> None:
    """Manejador del boton guardar nuevo."""
    if controlador.checkear_variables(variables):
        if messagebox.askyesno("Guardar", '¿Desea guardar el libro "{}" del autor {}?'.format(variables["titulo_libro"].get(), variables["autor_libro"].get())):
            boton_principal.config(state="normal")
            boton_secundario.config(state="normal")
            boton_borrar_primero.pack_forget()
            boton_borrar_segundo.pack_forget()
            frame_mostrar.pack_forget()
            if controlador.crear_libro(variables) == variables["id_libro"].get():
                messagebox.showinfo("Guardar", "Libro guardado")
                refrescar_contenido(tabla)
            else:
                messagebox.showerror(
                    "Guardar", "Error al guardar, libro ya existe.")
    else:
        messagebox.showerror("Error", "Debe completar todos los campos.")


def handle_btn_modificar(tabla: ttk.Treeview, frame_mostrar: LabelFrame, frame_botones: LabelFrame, boton_principal: Button, boton_secundario: Button, variables: Dict) -> None:
    """Manejador del boton modificar."""
    try:
        item = tabla.item(tabla.focus(), 'values')
        id_libro = item[0]
        estado_libro = item[1]
        titulo_libro = item[2]
        autor_libro = item[3]
        editorial_libro = item[4]
        estante_libro = item[5]
        if item:
            boton_principal.config(state="disabled")
            boton_secundario.config(state="disabled")
            btn_cancelar = componente_boton(frame_botones, "Cancelar", lambda: handle_btn_cancelar(
                frame_mostrar, boton_principal, boton_secundario, btn_guardar, btn_cancelar), RIGHT)
            btn_guardar = componente_boton(frame_botones, "Actualizar", lambda: hadle_btn_guardar_modificar(
                tabla, frame_mostrar, item, variables, boton_principal, boton_secundario, btn_guardar, btn_cancelar), RIGHT)
            frame_mostrar.pack(fill="x", expand="yes", pady=10, padx=20)
            variables["id_libro"].set(id_libro)
            variables["estado_libro"].set(estado_libro)
            variables["titulo_libro"].set(titulo_libro)
            variables["autor_libro"].set(autor_libro)
            variables["editorial_libro"].set(editorial_libro)
            variables["estante_libro"].set(estante_libro)
    except IndexError:
        messagebox.showerror("Error", "Seleccione un libro")


def hadle_btn_guardar_modificar(tabla: ttk.Treeview, frame_mostrar: LabelFrame, item: list, variables: dict, boton_principal: Button, boton_secundario: Button, boton_borrar_primero: Button, boton_borrar_segundo: Button) -> None:
    """Manejador del boton guardar modificar."""
    if controlador.checkear_variables(variables):
        if messagebox.askyesno("Modificar", '¿Desea modificar el libro "{}" del autor {}?'.format(item[2], item[3])):
            boton_principal.config(state="normal")
            boton_secundario.config(state="normal")
            boton_borrar_primero.pack_forget()
            boton_borrar_segundo.pack_forget()
            frame_mostrar.pack_forget()
            if controlador.actualizar_libro(variables):
                messagebox.showinfo("Modifica", "Libro modificado")
                refrescar_contenido(tabla)
    else:
        messagebox.showerror("Error", "Debe completar todos los campos.")


def handle_btn_cancelar(frame_mostrar: LabelFrame, boton_principal: Button, boton_secundario: Button, boton_borrar_primero: Button, boton_borrar_segundo: Button) -> None:
    """Manejador del boton cancelar."""
    if messagebox.askyesno("Cancelar", "¿Esta seguro que desea cancelar la operación?"):
        boton_principal.config(state="normal")
        boton_secundario.config(state="normal")
        boton_borrar_primero.pack_forget()
        boton_borrar_segundo.pack_forget()
        frame_mostrar.pack_forget()


def handle_btn_eliminar(tabla: ttk.Treeview) -> None:
    """
    Manejador del boton eliminar.
    """
    try:
        item = tabla.item(tabla.focus(), 'values')
        if messagebox.askyesno("Eliminar", '¿Desea eliminar el libro "{}" de {} ?'.format(item[1], item[2])):
            if controlador.eliminar_libro(item):
                messagebox.showinfo("Eliminar", "Libro eliminado")
                refrescar_contenido(tabla)
            else:
                messagebox.showerror("Error", "No se pudo eliminar el libro")
    except IndexError:
        messagebox.showerror("Eliminar", "Seleccione un libro")


def handle_btn_exportar(tabla: ttk.Treeview) -> None:
    """Manejador del boton exportar."""
    lista_exportar = [tabla.item(e, 'values')
                      for e in tabla.get_children()]
    if len(lista_exportar) > 0:
        file = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV", "*.csv")], title="Exportar libros")
        if file:
            if controlador.exportar_a_csv(lista_exportar, file):
                messagebox.showinfo("Exportar", "Libros exportados")
            else:
                messagebox.showerror("Exportar", "Error al exportar")
    else:
        messagebox.showerror("Error", "No hay datos para exportar")


def handle_btn_importar(tabla: ttk.Treeview) -> None:
    """Manejador del boton importar."""
    file = filedialog.askopenfilename(defaultextension=".csv",
                                      filetypes=[("CSV", "*.csv")], title="Importar libros")
    if file:
        if controlador.importar_de_csv(file):
            messagebox.showinfo("Importar", "Libros importados")
            refrescar_contenido(tabla)
        else:
            messagebox.showerror("Importar", "Error al importar")

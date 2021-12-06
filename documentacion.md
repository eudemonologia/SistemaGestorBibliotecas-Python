# Sistema Gestor de Bibliotecas

## Base de datos

Realizado en una sola tabla para una facil importación.

Contiene los siguientes campos:

- id (INT PRIMARY KEY): unico y característico del libro.
- estado (VARCHAR): situación del libro actualmente entre "Nuevo", "Leyendo", "Leído" y "Perdido".
- titulo (VARCHAR): titulo del libro.
- autor (VARCHAR): autor del libro.
- editorial (VARCHAR): editorial del libro.
- estante (VARCHAR): lugar dónde se encuentra posicionado el libro.

```
CREATE TABLE IF NOT EXISTS libros(id INTEGER NOT NULL PRIMARY KEY, estado VARCHAR(100), titulo VARCHAR(255), autor VARCHAR(255), editorial VARCHAR(255), estante VARCHAR(255))
```

## Iniciar programa

El programa se inicia en main.py, donde se hayan dos constantes configurables para el inicio del programa.

- DB_NAME: nombre y terminación de la base de datos (.sqlite de manera predeterminada)
- USER_NAME: nombre del usuario de la aplicación.

Ambas son pasadas por parametro al modelo y la vista para iniciar la base de datos y el GUI respectivamente.

```
DB_NAME = 'biblioteca.sqlite'
USER_NAME = 'Cristian Diego Góngora Pabón'
modelo.iniciar(DB_NAME)
vista.iniciar(USER_NAME)
```

## Modelo - Vista - Controlador

Separé la aplicación en tres archivos siguiendo el patrón de diseño modelo - vista - controlador.

### Modelo

Realiza todas las gestiones con la base de datos de la aplicación.

Su función "iniciar" crea tanto la BD como los tablas necesarias, además de setear la constante DB_PATH que será consultada por el resto de funciones.

```
global DB_PATH
DB_PATH = DB_PATH + nombre_db
con = sqlite3.connect(DB_PATH)
try:
    cursorObj = con.cursor()
    ursorObj.execute(
    "CREATE TABLE IF NOT EXISTS libros(id INTEGER NOT NULL PRIMARY KEY, estado VARCHAR(100), titulo VARCHAR(255), autor VARCHAR(255), editorial VARCHAR(255), estante VARCHAR(255))")
    con.commit()
except Error:
    print("Error al crear la tabla libros: \n", Error)
finally:
    con.close()
```

Las demás funciones no se distancian muchas del clásico CRUD, con excepción de "buscar_palabra_regex", que crea una función en la consulta que nos permita utilizar las expresiones regulares para buscar registros:

```
con.create_function('REGEXP', 2, lambda y, x: 1 if re.search(y, x) else 0)
```

Para realizar la consulta (enlazada al buscador del programa) utilizo el siguiente codigo:

```
cursorObj = con.cursor()
cursorObj.execute(
"SELECT \* FROM libros WHERE titulo REGEXP ? OR autor REGEXP ? OR editorial REGEXP ?", (palabra, palabra, palabra))
rows = cursorObj.fetchall()
return rows
```

### Vista

Es la parte más compleja de todo el programa en cuanto a su código (con 384 lineas).

Se inicializa con el parametro "nombre_usuario" que se pasa directamente al componente "ventana". Justamente este es un punto que intentó minimimizar la reutilización de código, la componetización de los elementos en la UI.

```
def componente_ventana(nombre_usuario: str) -> Tk:
    """Crea una ventana con el nombre del usuario."""
    una_ventana = Tk()
    una_ventana.title("Biblioteca de " + nombre_usuario)
    una_ventana.resizable(0, 0)
    una_ventana.iconbitmap("./assets/icono.ico")
    return una_ventana
```

El principal elemento de la interfaz es la tabla, desde la cual se permite modificar, eliminar y exportar los libros.

La misma toma los datos propocionados por el controlador a partir de una fución de "refrescar" que puede ser reutilizado en cada ocasión que estos sean modificados (como al guardar un registro o modificarlo).

```
def refrescar_contenido(tabla: ttk.Treeview) -> None:
    """Refrasca el contenido de la tabla."""
    lista_libros = controlador.traer_libros()
    tabla.delete(\*tabla.get_children())
    for libro in lista_libros:
        tabla.insert("", END, values=libro)
```

Otro punto a explicar es el manejador de los botones "Nuevo" y "Modificar", que aunque cuentan con diferencias, tienen un algoritmo similar, deshabilitando ambos los botones de registro y sumando dos nuevos "Guardar" y "Cancelar" para poder modificar los datos del libro.

```
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
```

### Controlador

Se coloca entre la vista y el modelo y realiza las fuciones lógicas de la aplicación.

Una de ellas es chekear que los campos cumplen con los requerimientos.

```
def revisar_estado(estado: str) -> bool:
    """Revisa que el estado sea válido"""
    regex_estado = re.compile('^Nuevo|Leyendo|Leído|Perdido$')
    return True if regex_estado.match(estado) else False
```

Otra es importar y exportar en CSV los registros de la tabla.

```
def exportar_a_csv(libros_exportar: list, file_direction) -> bool:
    """Exporta los libros a un archivo csv"""
    print(file_direction)
    try:
        with open(file_direction, "w", encoding='utf-8', newline="") as archivo:
            escritor = csv.writer(archivo)
            for libro in libros_exportar:
                if libro != []:
                    escritor.writerow(libro)
        return True
    except Exception as e:
        print(e)
        return False
```

Finalmente, otra función importante es la de buscar, que convierte la palabra pasada por la vista a una patrón de REGEX(que no tome en cuenta las tildes o las mayúsculas), y lo pasa al modelo para su consulta en la base de datos.

```
def buscar(palabra: str) -> list:
    """Busca los libros que contengan la palabra"""
    regex_palabra = "(?i)"
    for char in palabra:
        if char == "a" or char == "á":
            regex_palabra += "[aá]"
        elif char == "e" or char == "é":
            regex_palabra += "[eé]"
        elif char == "i" or char == "í":
            regex_palabra += "[ií]"
        elif char == "o" or char == "ó":
            regex_palabra += "[oó]"
        else:
            regex_palabra += char
    resultado = modelo.buscar_palabra_regex(regex_palabra)
    return resultado
```

## Conclusión

Una importante decisión de diseño fue permitir la importación y exportación de registros a través de CSV. Estó decantó en la utilización de una sola tabla en la base de datos y cimento un nuevo dinamismo en la movilidad de los registros.

Otra punto importante fue la utilización de expresiones regulares para la busqueda en la base de datos, esto permitió saltar las diferencias por tildes y mayusculas, lo cual permite un alcance mayor en la captabilidad de los registros.

##### Creado por [Cristian Diego Góngora Pabón](https://www.linkedin.com/in/cristiangongora/)

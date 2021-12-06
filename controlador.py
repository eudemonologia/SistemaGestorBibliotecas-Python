import re
import csv
from tkinter.constants import TRUE
import modelo


def id_ultimo_libro() -> int:
    """Devuelve el id del último libro registrado o 1 si no hay ninguno"""
    id = modelo.get_last_id_libros()[0][0]
    if id == None:
        return 1
    else:
        return id + 1


def traer_libros() -> list:
    """Devuelve una lista con todos los libros"""
    resultado = modelo.get_libros()
    return resultado


def crear_libro(variables: dict) -> int:
    """Crea un libro y devuelve el id"""
    estado = variables["estado_libro"].get()
    titulo = variables["titulo_libro"].get().title().strip()
    autor = variables["autor_libro"].get().title().strip()
    editorial = variables["editorial_libro"].get().title().strip()
    estante = variables["estante_libro"].get().title().strip()
    resultado = modelo.alta_libro(estado, titulo, autor, editorial, estante)
    return resultado


def actualizar_libro(variables: dict) -> None:
    """Actualiza un libro"""
    id = variables["id_libro"].get()
    estado = variables["estado_libro"].get()
    titulo = variables["titulo_libro"].get().title().strip()
    autor = variables["autor_libro"].get().title().strip()
    editorial = variables["editorial_libro"].get().title().strip()
    estante = variables["estante_libro"].get().title().strip()
    resultado = modelo.update_libro(
        id, estado, titulo, autor, editorial, estante)
    return resultado


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


def eliminar_libro(item) -> None:
    """Elimina un libro por su id"""
    resultado = modelo.delete_libro_by_id(item[0])
    return resultado


def revisar_id(id: int) -> bool:
    """Revisa que el id sea válido"""
    regex_id = re.compile('^[0-9]+$')
    return True if regex_id.match(str(id)) else False


def revisar_estado(estado: str) -> bool:
    """Revisa que el estado sea válido"""
    regex_estado = re.compile('^Nuevo|Leyendo|Leído|Perdido$')
    return True if regex_estado.match(estado) else False


def checkear_variables(variables: dict) -> bool:
    """Revisa que las variables sean válidas"""
    for key, value in variables.items():
        if key == "id_libro":
            if not revisar_id(value.get()):
                return False
        elif key == "estado_libro":
            if not revisar_estado(value.get()):
                return False
        else:
            if value.get() == "":
                return False
    return True


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


def importar_de_csv(file_direction) -> list:
    """Importa los libros de un archivo csv"""
    try:
        with open(file_direction, "r", encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            libros_importados = []
            for libro in lector:
                libros_importados.append(libro)
        for libro in libros_importados:
            modelo.alta_libro(libro[1], libro[2], libro[3], libro[4], libro[5])
        return True
    except Exception as e:
        print(e)
        return False

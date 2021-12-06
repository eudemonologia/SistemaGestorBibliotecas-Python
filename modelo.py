import re
import sqlite3
from sqlite3 import Error

DB_PATH = './bibliotecas/'

# Crear la base de datos


def conectar() -> sqlite3.Connection:
    """Se conecta a la base de datos y devuelve el objeto conexión"""
    try:
        con = sqlite3.connect(DB_PATH)
        return con
    except Error:
        print("Error al conectarse o crear a la base de datos: \n", Error)


def get_last_id_libros() -> int:
    """Devuelve el último id de la tabla libros"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT MAX(id) FROM libros")
        rows = cursorObj.fetchall()
        return rows
    except Error:
        print("Error al obtener el último id de los libros: \n", Error)
    finally:
        con.close()


def get_libros() -> list:
    """Devuelve todos los libros"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM libros")
        rows = cursorObj.fetchall()
        return rows
    except Error:
        print("Error al obtener los libros: \n", Error)
    finally:
        con.close()


def get_libro_by_id(id: int) -> tuple:
    """Devuelve un libro por su id"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM libros WHERE id = ?", (id,))
        rows = cursorObj.fetchone()
        return rows
    except Error:
        print("Error al obtener el libro: \n", Error)
    finally:
        con.close()


def get_libro_by_estado(estado: str) -> list:
    """Devuelve una lista de libros según su estado"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM libros WHERE estado = ?", (estado,))
        rows = cursorObj.fetchall()
        return rows
    except Error:
        print("Error al obtener los libros: \n", Error)
    finally:
        con.close()


def get_libros_by_autor(autor: str) -> list:
    """Devuelve una lista de libros según su autor"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT * FROM libros WHERE autor = ?", (autor,))
        rows = cursorObj.fetchall()
        return rows
    except Error:
        print("Error al obtener los libros: \n", Error)
    finally:
        con.close()


def get_libros_by_editorial(editorial: str) -> list:
    """Devuelve una lista de libros según su editorial"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT * FROM libros WHERE editorial = ?", (editorial,))
        rows = cursorObj.fetchall()
        return rows
    except Error:
        print("Error al obtener los libros: \n", Error)
    finally:
        con.close()


def get_libros_by_estante(estante: str) -> list:
    """Devuelve una lista de libros según su estante"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT * FROM libros WHERE estante = ?", (estante,))
        rows = cursorObj.fetchall()
        return rows
    except Error:
        print("Error al obtener los libros: \n", Error)
    finally:
        con.close()


def alta_libro(estado: str, titulo: str, autor: str, editorial: str, estante: str) -> int:
    """Agrega un libro a la base de datos si no existe"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT * FROM libros WHERE titulo = ? AND autor = ? AND editorial = ?", (titulo, autor, editorial))
        resultado = cursorObj.fetchone()
        if resultado is None:
            cursorObj.execute("INSERT INTO libros(estado, titulo, autor, editorial, estante) VALUES(?,?,?,?,?)",
                              (estado, titulo, autor, editorial, estante))
            con.commit()
            return cursorObj.lastrowid
        else:
            print("El libro ya existe")
            return resultado[0]
    except Error:
        print("Error al dar de alta el libro: \n", Error)
    finally:
        con.close()


def update_libro(id: int, estado: str, titulo: str, autor: str, editorial: str, estante: str) -> bool:
    """Actualiza un libro de la base de datos por su id"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute("UPDATE libros SET estado = ?, titulo = ?, autor = ?, editorial = ?, estante = ? WHERE id = ?",
                          (estado, titulo, autor, editorial, estante, id))
        con.commit()
        return True
    except Error:
        print("Error al actualizar el libro: \n", Error)
        return False
    finally:
        con.close()


def delete_libro_by_id(id: int) -> bool:
    """Elimina un libro de la base de datos por su id"""
    con = conectar()
    try:
        cursorObj = con.cursor()
        cursorObj.execute("DELETE FROM libros WHERE id = ?", (id,))
        con.commit()
        return True
    except Error:
        print("Error al eliminar el libro: \n", Error)
        return False
    finally:
        con.close()


def buscar_palabra_regex(palabra: str) -> list:
    """Busca un libro por su titulo, autor o editorial por REGEX"""
    con = conectar()
    con.create_function('REGEXP', 2, lambda y, x: 1 if re.search(y, x) else 0)
    try:
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT * FROM libros WHERE titulo REGEXP ? OR autor REGEXP ? OR editorial REGEXP ?", (palabra, palabra, palabra))
        rows = cursorObj.fetchall()
        return rows
    except Error:
        print("Error al buscar los libros: \n", Error)
    finally:
        con.close()


def iniciar(nombre_db) -> None:
    """Crea la base de datos segun el nombre pasado por parametro"""
    global DB_PATH
    DB_PATH = DB_PATH + nombre_db
    try:
        con = sqlite3.connect(DB_PATH)
        try:
            cursorObj = con.cursor()
            cursorObj.execute(
                "CREATE TABLE IF NOT EXISTS libros(id INTEGER NOT NULL PRIMARY KEY, estado VARCHAR(100), titulo VARCHAR(255), autor VARCHAR(255), editorial VARCHAR(255), estante VARCHAR(255))")
            con.commit()
        except Error:
            print("Error al crear la tabla libros: \n", Error)
        finally:
            con.close()
    except Error:
        print("Error al crear o conectarse a la base de datos: \n", Error)
    finally:
        print("Base de datos creada")

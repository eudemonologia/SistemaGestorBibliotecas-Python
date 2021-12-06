import vista
import modelo

if __name__ == '__main__':
    DB_NAME = 'biblioteca.sqlite'
    USER_NAME = 'Cristian Diego Góngora Pabón'
    modelo.iniciar(DB_NAME)
    vista.iniciar(USER_NAME)

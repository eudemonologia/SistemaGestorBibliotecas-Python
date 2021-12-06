import vista
import modelo

if __name__ == '__main__':
    DB_Name = 'biblioteca.sqlite'
    USUARIO = 'Cristian Diego Góngora Pabón'
    modelo.iniciar(DB_Name)
    vista.iniciar(USUARIO)

import logging

# Configurar el logger global
logging.basicConfig(
    level=logging.DEBUG,  # Mostrar todos los logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# Función para obtener un logger con nombre
def get_logger(name):
    return logging.getLogger(name)

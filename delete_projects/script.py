import requests
import csv
import logging
import sys
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# LOGGING
logging.basicConfig(
    filename='process.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# CREDENCIALES 
load_dotenv() # Cargo las credenciales desdeun '.env'
email = os.getenv("email")
api_token = os.getenv("api_token")
base_url = os.getenv("base_url")

# AUTENTICACIÓN
auth = HTTPBasicAuth(email, api_token)
headers = {
    "Accept": "application/json"
}

# Intento conectarme al entorno
try:
    auth_check = requests.get(f"{base_url}/rest/api/3/myself", headers = headers, auth = auth)
except Exception as e:
    logging.exception(f"Excepción al comprobar autenticación: {e}")
    sys.exit(1)

if auth_check.status_code != 200:
    logging.error(f"Autenticación fallida (GET /myself): {auth_check.status_code} - {auth_check.text}")
    sys.exit(1)
else: logging.info("Autenticación verificada correctamente.")

# LECTURA Y ELIMINACION DE PROYECTOS
csv_path = 'projects.csv'
# Intento abrir leer el CSV y realizar el proceso de eliminación de proyectos
try:
    with open(csv_path, newline = '', encoding = 'utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = ',')
        logging.info(f"Cabeceras detectadas en CSV: {reader.fieldnames}")

        for row in reader:
            project_key = row.get('PROJECT_KEY', '').strip()
            # Compruebo si la KEY existe
            if not project_key:
                logging.warning(f"Fila con PROJECT_KEY vacío o inexistente: {row}")
                continue

            # Intento eliminar el proyecto
            url = f"{base_url}/rest/api/3/project/{project_key}"
            try:
                response = requests.delete(url, headers = headers, auth = auth)
            except Exception as e:
                logging.error(f"Excepción al intentar eliminar {project_key}: {e}")
                continue

            # Eliminación exitosa
            if response.status_code == 204: logging.info(f"Proyecto eliminado correctamente: {project_key}")

            # Error de autenticación durante el DELETE
            elif response.status_code in (401, 403):
                logging.error(f"Error de autenticación al borrar {project_key}: {response.status_code} - {response.text}")
                sys.exit(1)

            # Otros errores 
            else: logging.error(f"Error eliminando {project_key}: {response.status_code} - {response.text}")
# Si no encuentro el archivo
except FileNotFoundError:
    logging.error(f"No se encontró el fichero '{csv_path}'.")
    sys.exit(1)

# Si ocurre un error de procesamiento
except Exception as e:
    logging.error(f"Error al procesar el CSV: {e}")
    sys.exit(1)

logging.info("Proceso de eliminación de proyectos finalizado.")
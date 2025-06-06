import requests
import csv
import logging
import sys
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# LOGGING
logging.basicConfig(
    filename = 'process.log',
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s: %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

# CREDENCIALES 
load_dotenv() # Cargo las credenciales desdeun '.env'
email = os.getenv("email")
api_token = os.getenv("api_token")
base_url = os.getenv("base_url")
account_id = os.getenv("account_id") # 'account_id' del nuevo Project Lead

# AUTENTICACIÓN
auth = HTTPBasicAuth(email, api_token)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Intento conectarme al entorno
try:
    auth_check = requests.get(f"{base_url}/rest/api/3/myself", headers = headers, auth = auth)
except Exception as e:
    logging.error(f"Excepción al comprobar autenticación: {e}")
    sys.exit(1)

if auth_check.status_code != 200:
    logging.error(f"Autenticación fallida (GET /myself): {auth_check.status_code} - {auth_check.text}")
    sys.exit(1)
else: logging.info("Autenticación verificada.")

# CAMBIO DE PROJECT LEADS DE LOS PROYECTOS
def cambiar_project_lead(project_key: str, lead_account_id: str) -> bool:
    url = f"{base_url}/rest/api/3/project/{project_key}"
    payload = {
        "leadAccountId": lead_account_id
    }

    # Intento realizar un PUT para cambiar el Project Lead
    try:
        resp = requests.put(url, json = payload, headers = headers, auth = auth)
    except Exception as e:
        logging.exception(f"Excepción al cambiar lead del proyecto '{project_key}': {e}")
        return False
    
    # Cambio exitoso
    if resp.status_code == 200: return True

    # Errores de autenticación o permisos
    if resp.status_code in (401, 403):
        logging.error(f"Error de autenticación o permiso en el proyecto '{project_key}': {resp.status_code} - {resp.text}")
        sys.exit(1)

    logging.error(f"Error cambiando Project Lead del proyecto '{project_key}': {resp.status_code} - {resp.text}")
    return False

# LECTURA Y PROCESAMIENTO DEL CSV PARA CAMBIAR EL PROJECT LEAD
csv_path = 'projects.csv'
# Intento abrir leer el CSV y llamar a la función 'cambiar_project_lead()'
try:
    with open(csv_path, newline = '', encoding = 'utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = ',')
        logging.info(f"Cabeceras detectadas en CSV: {reader.fieldnames}")

        for row in reader:
            project_key = row.get('PROJECT_KEY', '').strip()
            # Si hay una fila vacía se lanza un wanrning pero se continúa con la ejecución
            if not project_key:
                logging.warning(f"Fila con 'PROJECT_KEY' vacío o inexistente: '{row}'")
                continue

            logging.info(f"Cambiando Project Lead del protecto '{project_key}' → (accountId: '{account_id}') ...")

            # Si la función 'cambiar_project_lead()' devuelve 'true' indicó que todo va bien, de lo contrario lanzo un error
            if cambiar_project_lead(project_key, account_id): logging.info(f"Project Lead actualizado para el proyecto'{project_key}'")
            else: logging.error(f"Error al actualizar Project Lead en: '{project_key}'")

# Si no encuentro el archivo
except FileNotFoundError:
    logging.error(f"No se encontró el fichero '{csv_path}'.")
    sys.exit(1)

# Si ocurre un error de procesamiento
except Exception as e:
    logging.error(f"Error al procesar el CSV: {e}")
    sys.exit(1)

logging.info("Proceso de cambio de Project Lead finalizado.")
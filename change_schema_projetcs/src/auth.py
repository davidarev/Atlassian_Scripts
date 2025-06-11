import os
import sys
import logging
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Configuro el logger para este módulo
logger = logging.getLogger(__name__)

def get_auth_and_headers():
    # CREDENCIALES
    load_dotenv()  # Cargo las credenciales desde un '.env'
    email = os.getenv("email")
    api_token = os.getenv("api_token")
    base_url = os.getenv("base_url") 

    # Valido las variables obligatorias
    if not all([email, api_token, base_url]):
        logger.error("Faltan variables de entorno esenciales: email, api_token o base_url.")
        sys.exit(1)

    # AUTENTICACIÓN
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json"
    }
    # Intento conectarme al entorno
    try:
        resp = requests.get(f"{base_url}/rest/api/3/myself", headers = headers, auth = auth)
        if resp.status_code != 200:
            logger.error(f"Autenticación fallida (GET /myself): {resp.status_code} - {resp.text}")
            sys.exit(1)
        logger.info("Autenticación verificada correctamente.")
    except Exception as e:
        logger.exception(f"Excepción al comprobar autenticación: {e}")
        sys.exit(1)

    return auth, headers, base_url
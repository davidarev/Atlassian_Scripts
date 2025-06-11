import logging
import sys
import csv
import requests
import os
from utilities import (
    assign_permission_scheme,
    assign_workflow_scheme,
    assign_field_configuration_scheme,
    assign_issue_type_screen_scheme,
    assign_notification_scheme,
    assign_screen_scheme,
    assign_issue_type_scheme,
)
from auth import get_auth_and_headers

# LOGGING
logging.basicConfig(
    filename='process.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

# AUTENTICACIÓN
auth, headers, base_url = get_auth_and_headers()

# LECTURA Y ASIGNACIÓN DE ESQUEMAS
csv_path = 'projects.csv'
# Intento abrir leer el CSV y realizar el proceso de asignación de esquemas a proyectos
try:
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        logger.info(f"Cabeceras detectadas en CSV: {reader.fieldnames}")

        for row in reader:
            project_key = row.get("PROJECT_KEY", "").strip()
            # Compruebo si la KEY existe
            if not project_key:
                logger.warning(f"Fila con 'PROJECT_KEY' vacío o inexistente: {row}")
                continue

            # Verifico la existencia del proyecto
            try:
                resp = requests.get(f"{base_url}/rest/api/3/project/{project_key}", headers=headers, auth=auth)
                if resp.status_code != 200:
                    logger.error(f"No se encontró o no se puede consultar proyecto '{project_key}': "f"{resp.status_code} - {resp.text}")
                    continue
            except Exception as e:
                logger.exception(f"Excepción al consultar proyecto '{project_key}': {e}")
                continue

            # Esquemas tomados de las variables de entorno
            schemes = {
                "perm": os.getenv("PERMISSION_SCHEME_ID"),
                "workflow": os.getenv("WORKFLOW_SCHEME_ID"),
                "fieldconf": os.getenv("FIELD_CONFIG_SCHEME_ID"),
                "issuetype_screen": os.getenv("ISSUE_TYPE_SCREEN_SCHEME_ID"),
                "notification": os.getenv("NOTIFICATION_SCHEME_ID"),
                "screen": os.getenv("SCREEN_SCHEME_ID"),
                "issuetype": os.getenv("ISSUE_TYPE_SCHEME_ID"),
            }

            # Modifico los valores de los esquemas para que sean enteros
            if schemes["perm"]: assign_permission_scheme(base_url, project_key, schemes["perm"], auth, logger)
            if schemes["workflow"]: assign_workflow_scheme(base_url, project_key, schemes["workflow"], auth, logger)
            if schemes["fieldconf"]: assign_field_configuration_scheme(base_url, project_key, schemes["fieldconf"], auth, logger)
            if schemes["issuetype_screen"]: assign_issue_type_screen_scheme(base_url, project_key, schemes["issuetype_screen"], auth, logger)
            if schemes["notification"]: assign_notification_scheme(base_url, project_key, schemes["notification"], auth, logger)
            if schemes["screen"]: assign_screen_scheme(base_url, project_key, schemes["screen"], auth, logger)
            if schemes["issuetype"]: assign_issue_type_scheme(base_url, project_key, schemes["issuetype"], auth, logger)

            logger.info(f"Esquemas reasignados para {project_key}")

# Si no encuentro el archivo
except FileNotFoundError:
    logger.error(f"No se encontró el fichero '{csv_path}'.")
    sys.exit(1)
    
# Si ocurre un error de procesamiento
except Exception as e:
    logger.exception(f"Error al procesar el CSV o durante las asignaciones: {e}")
    sys.exit(1)

logger.info("Proceso completo de reasignación de esquemas.")

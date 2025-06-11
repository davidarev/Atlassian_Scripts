import requests

# Función para modificar el esquema de permisos un proyecto en Jira
def assign_permission_scheme(base_url, project_key, scheme_id, auth, logger):
    url = f"{base_url}/rest/api/3/project/{project_key}/permissionscheme"
    # Creo el payload con el ID del esquema de permisos
    payload = {
        "permissionSchemeId": int(scheme_id)
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Mediante un PUT, intento asignar el esquema de permisos al proyecto
    try:
        r = requests.put(url, json = payload, headers = headers, auth = auth)
        if 200 <= r.status_code < 300: logger.info(f"Permission Scheme asignado ({scheme_id}).")
        else: logger.error(f"Error asignando Permission Scheme a '{project_key}': " f"{r.status_code} - {r.text}")
    except Exception as e:
        logger.error(f"Excepción asignando Permission Scheme a '{project_key}': {e}")

# Función para modificar el esquema de flujo de trabajo de un proyecto en Jira      
def assign_workflow_scheme(base_url, project_key, scheme_id, auth, logger):
    url = f"{base_url}/rest/api/3/project/{project_key}/workflowscheme"
    payload = {
        "workflowSchemeId": int(scheme_id)
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        r = requests.put(url, json = payload, headers = headers, auth = auth)
        if 200 <= r.status_code < 300: logger.info(f"Workflow Scheme asignado ({scheme_id}).")
        else: logger.error(f"Error asignando Workflow Scheme a '{project_key}': " f"{r.status_code} - {r.text}")
    except Exception as e:
        logger.error(f"Excepción asignando Workflow Scheme a '{project_key}': {e}")

# Función para modificar el esquema de campos un proyecto en Jira
def assign_field_configuration_scheme(base_url, project_key, scheme_id, auth, logger):
    url = f"{base_url}/rest/api/3/project/{project_key}/fieldconfigurationscheme"
    payload = {
        "fieldConfigurationSchemeId": int(scheme_id)
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        r = requests.put(url, json = payload, headers = headers, auth = auth)
        if 200 <= r.status_code < 300: logger.info(f"Field Configuration Scheme asignado ({scheme_id}).")
        else: logger.error(f"Error asignando Field Configuration Scheme a '{project_key}': " f"{r.status_code} - {r.text}")
    except Exception as e:
        logger.error(f"Excepción asignando Field Configuration Scheme a '{project_key}': {e}")

# Función para modificar el esquema de pantallas asociadas a issue types un proyecto en Jira
def assign_issue_type_screen_scheme(base_url, project_key, scheme_id, auth, logger):
    url = f"{base_url}/rest/api/3/project/{project_key}/issuescreenscheme"
    payload = {
        "issueTypeScreenSchemeId": int(scheme_id)
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        r = requests.put(url, json = payload, headers = headers, auth = auth)
        if 200 <= r.status_code < 300: logger.info(f"Issue Type Screen Scheme asignado ({scheme_id}).")
        else: logger.error(f"Error asignando Issue Type Screen Scheme a '{project_key}': " f"{r.status_code} - {r.text}")
    except Exception as e:
        logger.error(f"Excepción asignando Issue Type Screen Scheme a '{project_key}': {e}")

# Función para modificar el esquema de notificaciones un proyecto en Jira
def assign_notification_scheme(base_url, project_key, scheme_id, auth, logger):
    url = f"{base_url}/rest/api/3/project/{project_key}/notificationscheme"
    payload = {
        "notificationSchemeId": int(scheme_id)
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        r = requests.put(url, json = payload, headers = headers, auth = auth)
        if 200 <= r.status_code < 300: logger.info(f"Notification Scheme asignado ({scheme_id}).")
        else: logger.error(f"Error asignando Notification Scheme a '{project_key}': " f"{r.status_code} - {r.text}")
    except Exception as e:
        logger.error(f"Excepción asignando Notification Scheme a '{project_key}': {e}")

# Función para modificar el esquema de pantalllas un proyecto en Jira
def assign_screen_scheme(base_url, project_key, scheme_id, auth, logger):
    url = f"{base_url}/rest/api/3/project/{project_key}/screenscheme"
    payload = {
        "screenSchemeId": int(scheme_id)
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        r = requests.put(url, json = payload, headers = headers, auth = auth)
        if 200 <= r.status_code < 300: logger.info(f"Screen Scheme asignado ({scheme_id}).")
        else: logger.error(f"Error asignando Screen Scheme a '{project_key}': " f"{r.status_code} - {r.text}")
    except Exception as e:
        logger.error(f"Excepción asignando Screen Scheme a '{project_key}': {e}")

# Función para modificar el esquema de issue types un proyecto en Jira
def assign_issue_type_scheme(base_url, project_key, scheme_id, auth, logger):
    url = f"{base_url}/rest/api/3/project/{project_key}/issuetypescheme"
    payload = {
        "issueTypeSchemeId": int(scheme_id)
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        r = requests.put(url, json = payload, headers = headers, auth = auth)
        if 200 <= r.status_code < 300: logger.info(f"Issue Type Scheme asignado ({scheme_id}).")
        else: logger.error(f"Error asignando Issue Type Scheme a '{project_key}': " f"{r.status_code} - {r.text}")
    except Exception as e:
        logger.error(f"Excepción asignando Issue Type Scheme a '{project_key}': {e}")
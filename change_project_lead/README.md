# Cambio de Project Lead desde CSV

## 1. Descripción

El script (`script.py`) realiza las siguientes acciones:

1. Carga credenciales y configuración desde un archivo `.env`.
2. Verifica la autenticación contra la API de Jira.
3. Define la función `cambiar_project_lead` que envía una petición `PUT` para actualizar el Project Lead.
4. Lee un archivo `projects.csv` con las claves de proyectos a procesar.
5. Para cada proyecto, invoca la función de cambio de Project Lead usando el `account_id` configurado.
6. Registra la actividad, advertencias y posibles errores en el fichero de log (`process.log`).

---

## 2. Requisitos

* **Python 3.7 o superior**
* **pip** (gestor de paquetes)
* Archivo `.env` con las siguientes variables:

  * `email`
  * `api_token`
  * `base_url`
  * `account_id`

---

## 3. Formato de `projects.csv`

El CSV debe tener una única columna **PROJECT\_KEY** (encabezado exacto) con una clave de proyecto por fila. Ejemplo:

```csv
PROJECT_KEY
PROY1
PROY2
PROY3
```

---

## 4. Uso

Ejecuta el script desde la raíz del repositorio:

```bash
python script.py
```

* Se registrarán mensajes informativos, advertencias y errores en `process.log`.
* Si la autenticación falla o hay un error crítico, el script terminará con código de error.

---

## 5. Ejemplos de ejecución

```bash
$ python script.py
# logs en process.log:
# 2025-06-09 10:15:23 INFO: Autenticación verificada.
# 2025-06-09 10:15:24 INFO: Cabeceras detectadas en CSV: ['PROJECT_KEY']
# 2025-06-09 10:15:25 INFO: Cambiando Project Lead del proyecto 'PROY1' → (accountId: '5f47a8c9e8d6b12') ...
# 2025-06-09 10:15:26 INFO: Project Lead actualizado para el proyecto 'PROY1'
# 2025-06-09 10:15:27 ERROR: Error al actualizar Project Lead en: 'PROY2'
# 2025-06-09 10:15:27 INFO: Proceso de cambio de Project Lead finalizado.
```

---

## 6. Pruebas

Para ejecutar las pruebas automáticas, se recomienda usar **pytest**:

1. Instala pytest:

   ```bash
   pip install pytest
   ```
2. Crea un directorio `tests/` y añade allí tests que simulen las llamadas a la API (p.ej., usando `unittest.mock`).
3. Ejecuta:

   ```bash
   pytest
   ```

> **Nota:** Mockear las respuestas HTTP para evitar modificar datos reales en Jira.

---

## 7. Logging

* El script genera un fichero `process.log` en la carpeta de trabajo.
* El nivel de logging está configurado en `INFO`.
* Formato de los mensajes:

  ```
  2025-06-09 10:15:23 INFO: Mensaje de ejemplo.
  ```

---

## 8. Explicación detallada del código

A continuación se describe paso a paso cada bloque del script `script.py`:

1. **Importaciones y carga de dependencias**

   ```python
   import requests
   import csv
   import logging
   import sys
   import os
   from requests.auth import HTTPBasicAuth
   from dotenv import load_dotenv
   ```

   * `requests`: cliente HTTP para conectar con la API de Jira.
   * `csv`: para leer el fichero CSV de proyectos.
   * `logging`: registra eventos e información de ejecución.
   * `sys`: permite salir del programa con códigos de error.
   * `os`: gestiona variables de entorno y rutas.
   * `HTTPBasicAuth`: maneja autenticación básica HTTP con token.
   * `load_dotenv`: carga variables de entorno desde `.env`.

2. **Configuración del logging**

   ```python
   logging.basicConfig(
       filename='process.log',
       level=logging.INFO,
       format='%(asctime)s %(levelname)s: %(message)s',
       datefmt='%Y-%m-%d %H:%M:%S'
   )
   ```

   Se crea el fichero `process.log` con nivel `INFO` y formato de fecha para un seguimiento ordenado.

3. **Carga de credenciales**

   ```python
   load_dotenv()
   email = os.getenv("email")
   api_token = os.getenv("api_token")
   base_url = os.getenv("base_url")
   account_id = os.getenv("account_id")
   ```

   * `load_dotenv()`: lee las variables definidas en el archivo `.env`.
   * `os.getenv`: obtiene `email`, `api_token`, `base_url` y `account_id`.

4. **Autenticación**

   ```python
   auth = HTTPBasicAuth(email, api_token)
   headers = {"Accept": "application/json", "Content-Type": "application/json"}
   try:
       auth_check = requests.get(f"{base_url}/rest/api/3/myself", headers=headers, auth=auth)
   except Exception as e:
       logging.error(f"Excepción al comprobar autenticación: {e}")
       sys.exit(1)
   ```

   * Se comprueba la ruta `/myself` de la API para validar credenciales.
   * En caso de excepción, se registra un error y finaliza el programa con código 1.

5. **Validación del estado de autenticación**

   ```python
   if auth_check.status_code != 200:
       logging.error(f"Autenticación fallida (GET /myself): {auth_check.status_code} - {auth_check.text}")
       sys.exit(1)
   else:
       logging.info("Autenticación verificada.")
   ```

   * Si la respuesta no es `200 OK`, registra un error y sale con código 1.
   * Si es exitosa, registra un mensaje informativo.

6. **Función `cambiar_project_lead`**

   ```python
   def cambiar_project_lead(project_key: str, lead_account_id: str) -> bool:
       url = f"{base_url}/rest/api/3/project/{project_key}"
       payload = {"leadAccountId": lead_account_id}
       try:
           resp = requests.put(url, json=payload, headers=headers, auth=auth)
       except Exception as e:
           logging.exception(f"Excepción al cambiar lead del proyecto '{project_key}': {e}")
           return False
       if resp.status_code == 200:
           return True
       if resp.status_code in (401, 403):
           logging.error(f"Error de autenticación o permiso en el proyecto '{project_key}': {resp.status_code} - {resp.text}")
           sys.exit(1)
       logging.error(f"Error cambiando Project Lead del proyecto '{project_key}': {resp.status_code} - {resp.text}")
       return False
   ```

   * Envía una petición `PUT` para actualizar el `leadAccountId`.
   * Devuelve `True` si el cambio fue exitoso (`200`), sale o registra error en otros casos.

7. **Lectura y procesamiento del CSV**

   ```python
   csv_path = 'projects.csv'
   try:
       with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
           reader = csv.DictReader(csvfile, delimiter=',')
           logging.info(f"Cabeceras detectadas en CSV: {reader.fieldnames}")
           for row in reader:
               project_key = row.get('PROJECT_KEY', '').strip()
               if not project_key:
                   logging.warning(f"Fila con 'PROJECT_KEY' vacío o inexistente: '{row}'")
                   continue
               logging.info(f"Cambiando Project Lead del proyecto '{project_key}' → (accountId: '{account_id}') ...")
               if cambiar_project_lead(project_key, account_id):
                   logging.info(f"Project Lead actualizado para el proyecto '{project_key}'")
               else:
                   logging.error(f"Error al actualizar Project Lead en: '{project_key}'")
   except FileNotFoundError:
       logging.error(f"No se encontró el fichero '{csv_path}'.")
       sys.exit(1)
   except Exception as e:
       logging.error(f"Error al procesar el CSV: {e}")
       sys.exit(1)
   ```

   * Abre `projects.csv` y recorre cada fila.
   * Para cada `PROJECT_KEY`, invoca la función de cambio de Project Lead.
   * Maneja filas vacías y registra advertencias.

8. **Fin del proceso**

   ```python
   logging.info("Proceso de cambio de Project Lead finalizado.")
   ```

   Marca la conclusión del script.

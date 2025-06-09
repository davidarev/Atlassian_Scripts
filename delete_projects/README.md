# **Eliminación de Proyectos desde CSV**

Este repositorio contiene un script en Python para eliminar proyectos de Jira a partir de una lista definida en un archivo CSV. Está pensado para uso interno por compañeros de equipo con conocimientos de nivel bajo a medio, aunque perfiles más técnicos también lo encontrarán útil.

---

## 1. Descripción

El script (`delete_projects.py`) realiza las siguientes acciones:

1. Carga credenciales y configuración desde un archivo `.env`.
2. Verifica la autenticación contra la API de Jira.
3. Lee un archivo `projects.csv` con las claves de proyectos a eliminar.
4. Intenta eliminar cada proyecto vía la API
5. Registra la actividad y posibles errores en el fichero de log (`process.log`).

---

## 2. Requisitos

* **Python 3.7**
* **pip** (gestor de paquetes)

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
python delete_projects.py
```

* Se registrarán mensajes informativos, advertencias y errores en `process.log`.
* Si la autenticación falla, el script terminará con código de error.

---

## 5. Ejemplos de ejecución

```bash
$ python delete_projects.py
# logs:
# 2025-06-09 10:15:23 INFO: Autenticación verificada correctamente.
# 2025-06-09 10:15:24 INFO: Cabeceras detectadas en CSV: ['PROJECT_KEY']
# 2025-06-09 10:15:25 INFO: Proyecto eliminado correctamente: PROY1
# 2025-06-09 10:15:26 ERROR: Error eliminando PROY2: 404 - Project does not exist
# 2025-06-09 10:15:26 INFO: Proceso de eliminación de proyectos finalizado.
```

---

## 6. Pruebas

Para ejecutar las pruebas automáticas, se recomienda usar **pytest**.

1. Instala pytest:

   ```bash
   pip install pytest
   ```
2. Crea un directorio `tests/` y añade allí tests que simulen las llamadas a la API (p.ej., usando `unittest.mock`).
3. Ejecuta:

   ```bash
   pytest
   ```

> **Nota:** Debes mockear las respuestas HTTP para evitar eliminar proyectos reales durante las pruebas.

---

## 7. Logging

* El script genera un fichero `process.log` en la carpeta de trabajo.
* El nivel de logging está configurado en `INFO`.

---

## 8. Explicación detallada del código

A continuación se describe paso a paso cada bloque del script `delete_projects.py`:

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
   ```

   * `load_dotenv()`: lee el archivo `.env`.
   * `os.getenv`: obtiene `email`, `api_token` y `base_url`.

4. **Autenticación**

   ```python
   auth = HTTPBasicAuth(email, api_token)
   headers = {"Accept": "application/json"}
   try:
       auth_check = requests.get(f"{base_url}/rest/api/3/myself", headers=headers, auth=auth)
   except Exception as e:
       logging.exception(f"Excepción al comprobar autenticación: {e}")
       sys.exit(1)
   ```

   * Se prueba la ruta `/myself` de la API para validar credenciales.
   * En caso de excepción, se registra con nivel `EXCEPTION` y finaliza el programa.

5. **Validación del estado de autenticación**

   ```python
   if auth_check.status_code != 200:
       logging.error(f"Autenticación fallida (GET /myself): {auth_check.status_code} - {auth_check.text}")
       sys.exit(1)
   else:
       logging.info("Autenticación verificada correctamente.")
   ```

   * Si la respuesta no es `200 OK`, registra un error y sale con código 1.
   * Si es exitosa, registra un mensaje informativo.

6. **Lectura del CSV y eliminación de proyectos**

   ```python
   csv_path = 'projects.csv'
   try:
       with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
           reader = csv.DictReader(csvfile, delimiter=',')
           logging.info(f"Cabeceras detectadas en CSV: {reader.fieldnames}")
           for row in reader:
               project_key = row.get('PROJECT_KEY', '').strip()
               if not project_key:
                   logging.warning(f"Fila con PROJECT_KEY vacío o inexistente: {row}")
                   continue
               url = f"{base_url}/rest/api/3/project/{project_key}"
               try:
                   response = requests.delete(url, headers=headers, auth=auth)
               except Exception as e:
                   logging.error(f"Excepción al intentar eliminar {project_key}: {e}")
                   continue
               if response.status_code == 204:
                   logging.info(f"Proyecto eliminado correctamente: {project_key}")
               elif response.status_code in (401, 403):
                   logging.error(f"Error de autenticación al borrar {project_key}: {response.status_code} - {response.text}")
                   sys.exit(1)
               else:
                   logging.error(f"Error eliminando {project_key}: {response.status_code} - {response.text}")
   ```

   * Abre `projects.csv` con codificación UTF-8 BOM-safe.
   * Usa `DictReader` para acceder a la columna `PROJECT_KEY`.
   * Si la clave está vacía, registra `WARNING` y salta la fila.
   * Para cada `project_key`, envía un `DELETE`.
   * Gestiona distintos códigos de respuesta:

     * `204`: eliminado correctamente.
     * `401/403`: error de autenticación, sale con fallo.
     * Otros: registra el error y continúa.

7. **Manejo de excepciones al leer el CSV**

   ```python
   except FileNotFoundError:
       logging.error(f"No se encontró el fichero '{csv_path}'.")
       sys.exit(1)
   except Exception as e:
       logging.error(f"Error al procesar el CSV: {e}")
       sys.exit(1)
   ```

   * `FileNotFoundError`: el CSV no existe, registro y salida.
   * Cualquier otro error en la lectura procesa igual.

8. **Fin del proceso**

   ```python
   logging.info("Proceso de eliminación de proyectos finalizado.")
   ```

   Marca la conclusión del script.
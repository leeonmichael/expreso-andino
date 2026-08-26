"""
Prueba unitaria de la API (ANTES del despliegue).

Usa el cliente de pruebas de Flask sobre la aplicación LOCAL (el objeto `app`),
NO sobre la versión ya desplegada en internet. Simula una petición GET a la
ruta principal "/" y valida que el código de estado HTTP sea exactamente 200 OK.
"""
import os
import sys

# Permite importar app.py, que está dentro de la carpeta backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app import app  # noqa: E402


def test_ruta_principal_devuelve_200():
    app.config["TESTING"] = True
    cliente = app.test_client()
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200

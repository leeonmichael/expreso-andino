"""
Expreso Andino - API (Backend)
--------------------------------
API en Flask que se conecta a una base de datos MySQL y expone:
  - "/"            -> Página HTML con el estado de la conexión a la BD.
  - "/api/status"  -> Estado de la conexión en formato JSON.
  - "/health"      -> Chequeo simple de que el servicio está vivo.

Las credenciales NUNCA se escriben en el código: se leen desde variables
de entorno que Docker Compose inyecta a partir del archivo .env
"""

import os
from flask import Flask, jsonify, render_template_string
import mysql.connector

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuración de la base de datos (leída desde variables de entorno)
# ---------------------------------------------------------------------------
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db"),
    "user": os.environ.get("DB_USER", "root"),
    "password": "SuperClave123!",
    "database": os.environ.get("DB_NAME", "test"),
    "port": int(os.environ.get("DB_PORT", "3306")),
}


def check_db():
    """Intenta conectarse a MySQL. Devuelve (True, None) o (False, mensaje_error)."""
    try:
        conn = mysql.connector.connect(connection_timeout=5, **DB_CONFIG)
        conn.ping(reconnect=False, attempts=1)
        conn.close()
        return True, None
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


# ---------------------------------------------------------------------------
# Plantilla HTML (la "cara" visible de la aplicación)
# ---------------------------------------------------------------------------
PAGE = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Expreso Andino · Estado del sistema</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh; display: grid; place-items: center;
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #e2e8f0; padding: 1.5rem;
    }
    .card {
      background: #ffffff; color: #0f172a; width: 100%; max-width: 460px;
      border-radius: 18px; padding: 2.5rem 2rem; text-align: center;
      box-shadow: 0 20px 60px rgba(0,0,0,.35);
    }
    .badge {
      width: 84px; height: 84px; border-radius: 50%;
      display: grid; place-items: center; margin: 0 auto 1.25rem; font-size: 42px;
    }
    .ok  { background: #dcfce7; color: #16a34a; }
    .err { background: #fee2e2; color: #dc2626; }
    h1 { font-size: 1.4rem; margin-bottom: .5rem; }
    p  { color: #475569; line-height: 1.5; font-size: .95rem; }
    .meta {
      margin-top: 1.75rem; border-top: 1px solid #e2e8f0; padding-top: 1rem;
      font-size: .8rem; color: #94a3b8; display: flex; justify-content: space-between;
    }
    code { background:#f1f5f9; padding:.1rem .35rem; border-radius:6px; font-size:.8rem; }
  </style>
</head>
<body>
  <div class="card">
    {% if ok %}
      <div class="badge ok">&#10003;</div>
      <h1>Conexi&oacute;n exitosa a la base de datos</h1>
      <p>El backend (Flask) se comunic&oacute; correctamente con MySQL.
         La aplicaci&oacute;n est&aacute; desplegada y operativa.</p>
    {% else %}
      <div class="badge err">&#10007;</div>
      <h1>Error de conexi&oacute;n</h1>
      <p>El backend no pudo conectarse a MySQL.<br><code>{{ error }}</code></p>
    {% endif %}
    <div class="meta">
      <span>Proyecto: Expreso Andino</span>
      <span>BD: {{ db_name }}</span>
    </div>
  </div>
</body>
</html>
"""


@app.route("/")
def index():
    ok, error = check_db()
    return render_template_string(PAGE, ok=ok, error=error, db_name=DB_CONFIG["database"])


@app.route("/api/status")
def api_status():
    ok, error = check_db()
    if ok:
        return jsonify(status="ok", message="Conexión exitosa a la base de datos"), 200
    return jsonify(
        status="error",
        message="No se pudo conectar a la base de datos",
        detail=error,
    ), 500


@app.route("/health")
def health():
    return jsonify(status="up"), 200


if __name__ == "__main__":
    # Servidor de desarrollo. En producción se usa Gunicorn (ver Dockerfile).
    app.run(host="0.0.0.0", port=5050, debug=False)

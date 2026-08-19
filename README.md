# 🚂 Expreso Andino — Despliegue con Docker, CI/CD y HTTPS

Proyecto full-stack de ejemplo para la fase de **Implantación del Software** (SENA).
Demuestra el ciclo completo: contenerización con Docker, orquestación con Docker
Compose, integración y entrega continua con GitHub Actions, y despliegue en la nube
(Oracle Cloud IaaS) con dominio gratuito (DuckDNS) y certificado HTTPS (Let's Encrypt
vía Nginx Proxy Manager).

## 🧱 Arquitectura

```
Navegador
   │  (HTTP :80 / HTTPS :443)
   ▼
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│  web        │ ───▶ │  backend     │ ───▶ │  db        │
│  Nginx :80  │      │  Flask :5050 │      │  MySQL     │
│ (proxy)     │      │  (API)       │      │  :3306     │
└─────────────┘      └──────────────┘      └────────────┘
        red interna de Docker (los puertos de backend y db
        NO se exponen al host; solo "web" es accesible)
```

En **producción** el servicio `web` (Nginx simple) se reemplaza por
**Nginx Proxy Manager**, que además gestiona el certificado HTTPS.

## 📂 Estructura

```
expreso-andino/
├── backend/                 # API en Flask
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── web/                     # Nginx (proxy inverso / capa web)
│   ├── nginx.conf
│   └── Dockerfile
├── .github/workflows/
│   └── deploy.yml           # CI/CD: build + push a Docker Hub
├── docker-compose.yml       # LOCAL (construye desde el código)
├── docker-compose.hub.yml   # SIMULACRO (descarga de Docker Hub)
├── docker-compose.prod.yml  # PRODUCCIÓN (con Nginx Proxy Manager)
├── .env.example             # Plantilla de variables
├── .gitignore
└── README.md
```

## ▶️ Ejecución local

```bash
# 1) Copia las variables de entorno
cp .env.example .env        # y edita los valores

# 2) Levanta todo
docker compose up -d --build

# 3) Verifica
docker compose ps

# 4) Abre en el navegador
#    http://localhost   ->  "Conexión exitosa a la base de datos"

# Para detener (conservando la base de datos):
docker compose down
```

## 🔄 CI/CD con GitHub Actions

En cada `push` a `main`, el workflow `.github/workflows/deploy.yml`:
1. Inicia sesión en Docker Hub.
2. Construye las imágenes `expreso-api` y `expreso-web`.
3. Las publica con la etiqueta `latest`.

Requiere configurar en **Settings → Secrets and variables → Actions**:
- `DOCKERHUB_USERNAME` — tu usuario de Docker Hub.
- `DOCKERHUB_TOKEN` — un *Access Token* creado en Docker Hub.

## ☁️ Despliegue en producción (Oracle Cloud + HTTPS)

Resumen (pasos detallados en la guía de la Entrega 3):
1. Crear instancia Ubuntu en Oracle Cloud (Always Free) con IP pública.
2. Abrir puertos 80, 443 y 81 (Ingress Rules + firewall del sistema).
3. Instalar Docker y añadir el usuario al grupo `docker`.
4. Subir `docker-compose.prod.yml` (renombrado a `docker-compose.yml`) y `.env`.
5. `docker compose up -d`.
6. Crear un subdominio en DuckDNS apuntando a la IP pública.
7. En Nginx Proxy Manager (`http://IP:81`) crear un *Proxy Host*:
   dominio → `backend:5050`, y solicitar el certificado Let's Encrypt (Force SSL).

## 🔗 Enlaces del proyecto

- Repositorio: `https://github.com/TU_USUARIO/expreso-andino`
- Docker Hub: `https://hub.docker.com/u/TU_USUARIO`
- Aplicación en producción: `https://TU_SUBDOMINIO.duckdns.org`

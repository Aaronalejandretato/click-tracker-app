# 📊 Click Tracker App

![actions](https://github.com/Aaronalejandretato/click-tracker-app/actions/workflows/ci.yml/badge.svg)


Aplicación web en Flask que registra clics en elementos de la interfaz como métricas personalizadas mediante OpenTelemetry, exportadas a Prometheus y visualizadas en Grafana. Su finalidad es analizar la interacción del usuario en tiempo real, usando herramientas de observabilidad y automatización como Docker Compose, Ansible y GitHub Actions.



## ⚙️ Tecnologías utilizadas

- 🐍 **Python 3.12** + **Flask**
- 📦 **OpenTelemetry SDK** (métricas personalizadas)
- 📈 **Prometheus** (recolección de métricas)
- 📊 **Grafana** (visualización)
- 📦 **Docker & Docker Compose** (contenedorización y orquestación)
- ✅ **GitHub Actions** (CI)
- 👨‍💻 **Ansible** (despliegue remoto automático)


## 🖥️ Estructura del proyecto

```
click-tracker-app/
├── .gihub/                 # Integración continua
│   └── workflows
│       └── deploy.yml
├── app/                     # Código fuente Flask
│   |── main.py
    └── templates/           # HTML 
│       └── index.html
├── ansible/                 # Despliegue remoto con Ansible
│   ├── inventory.ini
│   └── deploy.yml
├── Dockerfile               # Imagen de la app Flask
├── docker-compose.yml       # Orquestación de servicios
├── requirements.txt         # Dependencias Python
├── .gitignore

```

## 🚀 Cómo usar este proyecto

### Clona el repositorio

```bash
git clone https://github.com/Aaronalejandretato/click-tracker-app.git
cd click-tracker-app
```


### Instalar dependencias

```bash
pip install -r requirements.txt
```

Si estás trabajando desde cero, instalar manualmente:

```bash
pip install flask
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-flask opentelemetry-util-http
```

Y guardar las dependencias:

```bash
pip freeze > requirements.txt
```


## 🐳 Uso local con Docker Compose

Crea y activa un entorno virtual (para probar fuera de Docker)

```bash
python -m venv venv
.env\Scripts\Activate.ps1  # En PowerShell
```
Levanta la aplicación con sus servicios:

```bash
docker compose up --build -d
```

Luego accede a:

- 🖥️ Aplicación Flask: http://localhost:5000
- 📈 Prometheus: http://localhost:9090
- 📊 Grafana: http://localhost:3000  
- 🔍 Métricas directas (opcional): http://localhost:9464/metrics


## 🔄 Integración continua (CI) con GitHub Actions

Cada vez que haces un push a `main`, GitHub ejecuta automáticamente:

- Revisión de estilo con `flake8`
- Verificación de formato con `black`

No es necesario configurar nada. Ya está listo en `.github/workflows/ci.yml`.

## 🛠 Despliegue remoto con Ansible (extra)

Aunque Docker Compose es ideal para desarrollo local, este proyecto incluye un **extra opcional** con Ansible para automatizar el despliegue de la app Flask en un servidor Linux desde cero.

```bash
# Lanzar el despliegue (en WSL, Linux o remoto)
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --ask-become-pass

# Ver contenedores activos
docker ps

# Eliminar despliegue manualmente
docker stop click-app && docker rm click-app && docker rmi tuusuario/click-tracker-app
```

### ✔️ ¿Qué hace Ansible?
- Instala Docker
- Descarga la imagen desde Docker Hub
- Ejecuta la app Flask como contenedor en el puerto 5000

## 📌 Comandos útiles

| Acción                              | Comando                                                                                  |
|-------------------------------------|------------------------------------------------------------------------------------------|
| Iniciar entorno virtual             | `.env\Scripts\Activate.ps1`                                                              |
| Instalar dependencias               | `pip install -r requirements.txt`                                                        |
| Guardar dependencias                | `pip freeze > requirements.txt`                                                          |
| Levantar entorno con Docker         | `docker compose up --build -d`                                                           |
| Apagar contenedores                 | `docker compose down`                                                                    |
| Ver logs del contenedor Flask       | `docker compose logs -f flask`                                                           |
| Ejecutar despliegue remoto          | `ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --ask-become-pass`         |
| Eliminar imagenes                   | `docker rmi $(docker images -q)`                                                         |
| Ver contenedores activos            | `docker ps`                                                           |

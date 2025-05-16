python -m venv venv

.\venv\Scripts\Activate.ps1

pip install flask

pip show flask

python app\main.py


🧩 Instalación de dependencias OpenTelemetry

pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-flask opentelemetry-util-http


pip freeze > requirements.txt

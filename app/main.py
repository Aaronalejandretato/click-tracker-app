# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/click", methods=["POST"])
# def click():
#     data = request.get_json()
#     ad_id = data.get("ad_id")
#     print(f"📌 Clic registrado en: {ad_id}")
#     return jsonify({"status": "ok"}), 200

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask, render_template, request, jsonify
from datetime import timedelta  # ← NUEVA IMPORTACIÓN
from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Recursos del servicio (nombre, versión, etc.)
resource = Resource(attributes={"service.name": "click-tracker-app"})

# Exportador OTLP -> Collector
otlp_exporter = OTLPMetricExporter(endpoint="http://otel-collector:4317", insecure=True)

# Configuración del proveedor de métricas con exportación más frecuente (cada 5s)
reader = PeriodicExportingMetricReader(
    otlp_exporter,
    export_interval_millis=5000  # ← ENVÍA métricas cada 5 segundos
)

provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

# Instrumentación manual
meter = metrics.get_meter("click-meter")
click_counter = meter.create_counter(
    name="clicks_por_anuncio",
    description="Número de clics por anuncio",
    unit="1",
)

# Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/click", methods=["POST"])
def click():
    data = request.get_json()
    ad_id = data.get("ad_id")

    # Incrementamos la métrica
    click_counter.add(1, attributes={"anuncio_id": ad_id})

    print(f"📌 Clic registrado en: {ad_id}")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

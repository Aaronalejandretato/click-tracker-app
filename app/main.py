from flask import Flask, render_template, request, jsonify
from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
import time

# Recursos de la app
resource = Resource(attributes={"service.name": "click-tracker-app"})

# Exportador OTLP gRPC al Collector
otlp_exporter = OTLPMetricExporter(endpoint="http://otel-collector:4317", insecure=True)

# Exportación periódica cada 5 segundos
reader = PeriodicExportingMetricReader(otlp_exporter, export_interval_millis=5000)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

# Crear el medidor
meter = metrics.get_meter("click-meter")

# Métrica: número de clics por anuncio
click_counter = meter.create_counter(
    name="clicks_por_anuncio",
    description="Número de clics por anuncio",
    unit="1",
)

# Métrica: tiempo entre clics
tiempo_click = meter.create_histogram(
    name="tiempo_entre_clicks",
    description="Tiempo entre clics en milisegundos",
    unit="ms",
)

# Métrica: clics erróneos simulados (solo para anuncio_3)
error_counter = meter.create_counter(
    name="clicks_erroneos_total",
    description="Número de errores simulados por clics",
    unit="1",
)

# Variables globales
ultimo_click = time.time()
contador_errores = 0  # Cuenta clics en anuncio_3 para simular errores cada 3

# Crear app Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/click", methods=["POST"])
def click():
    global ultimo_click, contador_errores

    data = request.get_json()
    ad_id = data.get("ad_id")

    # Registrar clic total
    click_counter.add(1, attributes={"anuncio_id": ad_id})

    # Calcular y registrar tiempo entre clics
    ahora = time.time()
    diferencia = int((ahora - ultimo_click) * 1000)
    tiempo_click.record(diferencia, attributes={"anuncio_id": ad_id})
    ultimo_click = ahora

    # Simular error cada 3 clics en anuncio_3
    if ad_id == "anuncio_3":
        contador_errores += 1
        if contador_errores % 3 == 0:
            error_counter.add(1, attributes={"anuncio_id": ad_id})
            print("❗ Simulación de error en anuncio_3")

    print(f"📌 Clic registrado en: {ad_id} ({diferencia} ms desde el último clic)")
    return jsonify({"status": "ok"}), 200

# Ejecutar app en todas las interfaces
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

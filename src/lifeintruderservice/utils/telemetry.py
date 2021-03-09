# ----- Opentelemetry | Jaeger -----
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchExportSpanProcessor,
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from config import args

def start_opentelemetry(app):
    trace.set_tracer_provider(TracerProvider())
    jaeger_exporter  = jaeger.JaegerSpanExporter(
        service_name="lifeintruderservice",
        agent_host_name=args.jaeger_agent_host,
        agent_port=int(args.jaeger_agent_port),
    )
    trace.get_tracer_provider().add_span_processor(
        BatchExportSpanProcessor(jaeger_exporter )
    )
    tracer = trace.get_tracer(__name__)
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        SimpleExportSpanProcessor(ConsoleSpanExporter())
    )
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()

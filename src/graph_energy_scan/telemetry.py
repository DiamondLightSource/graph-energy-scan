from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def setup_telemetry():
    tracer_provider = TracerProvider()
    console_exporter = BatchSpanProcessor(ConsoleSpanExporter())
    tracer_provider.add_span_processor(console_exporter)
    trace.set_tracer_provider(tracer_provider)

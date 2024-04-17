from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def setup_telemetry(otel_collector_url: str):
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(otel_collector_url))
    )
    trace.set_tracer_provider(tracer_provider)

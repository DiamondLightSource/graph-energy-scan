from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes

from graph_energy_scan import __version__


def setup_telemetry(otel_collector_url: str):
    tracer_provider = TracerProvider(
        resource=Resource.create(
            {
                ResourceAttributes.SERVICE_NAME: "graph-energy-scan",
                ResourceAttributes.SERVICE_VERSION: __version__,
            }
        )
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(otel_collector_url))
    )
    trace.set_tracer_provider(tracer_provider)

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, Span, SpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes

from graph_energy_scan import __version__


class FilteredSpanProcessor(SpanProcessor):
    inner: SpanProcessor
    filter_types: list[str]

    def __init__(self, inner: SpanProcessor, filter_types: list[str]) -> None:
        self.inner = inner
        self.filter_types = filter_types
        super().__init__()

    def on_start(self, span: Span, parent_context: trace.Context | None = None) -> None:
        self.inner.on_start(span, parent_context)

    def on_end(self, span: ReadableSpan) -> None:
        if span.attributes.get("type") not in self.filter_types:
            self.inner.on_end(span)

    def shutdown(self) -> None:
        self.inner.shutdown()

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        self.inner.force_flush(timeout_millis)


def setup_telemetry(otel_collector_url: str):
    filter_types = ["http.request", "http.response.start", "http.response.body"]
    tracer_provider = TracerProvider(
        resource=Resource.create(
            {
                ResourceAttributes.SERVICE_NAME: "graph-energy-scan",
                ResourceAttributes.SERVICE_VERSION: __version__,
            }
        )
    )
    tracer_provider.add_span_processor(
        FilteredSpanProcessor(BatchSpanProcessor(ConsoleSpanExporter()), filter_types)
    )
    tracer_provider.add_span_processor(
        FilteredSpanProcessor(
            BatchSpanProcessor(OTLPSpanExporter(otel_collector_url)), filter_types
        )
    )
    trace.set_tracer_provider(tracer_provider)

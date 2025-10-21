/**
 * 🔭 DISTRIBUTED TRACING WITH OPENTELEMETRY
 * Silicon Valley-grade observability implementation
 */

const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const opentelemetry = require('@opentelemetry/api');
const { BatchSpanProcessor, ConsoleSpanExporter } = require('@opentelemetry/sdk-trace-base');

class DistributedTracing {
  constructor() {
    this.tracer = null;
    this.sdk = null;
    this.spans = new Map();
    this.metrics = {
      traces_created: 0,
      spans_created: 0,
      errors_captured: 0
    };
  }

  /**
   * Initialize OpenTelemetry SDK
   */
  async initialize() {
    try {
      // Create resource identifying the service
      const resource = Resource.default().merge(
        new Resource({
          [SemanticResourceAttributes.SERVICE_NAME]: 'digimundo',
          [SemanticResourceAttributes.SERVICE_VERSION]: '2.0.0',
          [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'production',
          'service.instance.id': require('crypto').randomUUID(),
        })
      );

      // Configure trace exporter
      // In production, this would send to Jaeger, Zipkin, or cloud provider
      const traceExporter = process.env.OTEL_EXPORTER_OTLP_ENDPOINT
        ? new OTLPTraceExporter({
            url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
            headers: {},
          })
        : new ConsoleSpanExporter(); // Fallback to console for local dev

      // Create SDK
      this.sdk = new NodeSDK({
        resource,
        traceExporter,
        instrumentations: [
          getNodeAutoInstrumentations({
            '@opentelemetry/instrumentation-fs': {
              enabled: true,
            },
            '@opentelemetry/instrumentation-http': {
              enabled: true,
            },
          }),
        ],
      });

      // Initialize the SDK
      await this.sdk.start();

      // Get tracer
      this.tracer = opentelemetry.trace.getTracer(
        'digimundo-tracer',
        '1.0.0'
      );

      console.log('🔭 OpenTelemetry tracing initialized');
      return true;
    } catch (error) {
      console.error('Failed to initialize tracing:', error);
      return false;
    }
  }

  /**
   * Create a new trace span
   */
  startSpan(name, options = {}) {
    const span = this.tracer.startSpan(name, {
      kind: options.kind || opentelemetry.SpanKind.INTERNAL,
      attributes: options.attributes || {},
    });

    // Store span for later reference
    const spanId = span.spanContext().spanId;
    this.spans.set(spanId, span);
    this.metrics.spans_created++;

    return {
      span,
      spanId,
      end: (attributes = {}) => this.endSpan(spanId, attributes),
      recordError: (error) => this.recordError(spanId, error),
      addEvent: (name, attributes) => this.addEvent(spanId, name, attributes),
    };
  }

  /**
   * End a span
   */
  endSpan(spanId, attributes = {}) {
    const span = this.spans.get(spanId);
    if (span) {
      // Add final attributes
      Object.entries(attributes).forEach(([key, value]) => {
        span.setAttribute(key, value);
      });

      span.end();
      this.spans.delete(spanId);
    }
  }

  /**
   * Record an error in a span
   */
  recordError(spanId, error) {
    const span = this.spans.get(spanId);
    if (span) {
      span.recordException(error);
      span.setStatus({
        code: opentelemetry.SpanStatusCode.ERROR,
        message: error.message,
      });
      this.metrics.errors_captured++;
    }
  }

  /**
   * Add an event to a span
   */
  addEvent(spanId, name, attributes = {}) {
    const span = this.spans.get(spanId);
    if (span) {
      span.addEvent(name, attributes);
    }
  }

  /**
   * Create a trace for app startup
   */
  traceStartup() {
    const startupSpan = this.startSpan('app.startup', {
      kind: opentelemetry.SpanKind.INTERNAL,
      attributes: {
        'app.name': 'Digimundo',
        'app.version': '2.0.0',
        'platform': process.platform,
        'arch': process.arch,
      },
    });

    return {
      ...startupSpan,
      tracePhase: (phase, fn) => this.tracePhase(startupSpan.span, phase, fn),
    };
  }

  /**
   * Trace a specific phase within a parent span
   */
  async tracePhase(parentSpan, phaseName, fn) {
    const context = opentelemetry.trace.setSpan(
      opentelemetry.context.active(),
      parentSpan
    );

    return await opentelemetry.context.with(context, async () => {
      const phaseSpan = this.startSpan(`startup.${phaseName}`, {
        attributes: {
          'phase.name': phaseName,
        },
      });

      try {
        const startTime = Date.now();
        const result = await fn();
        const duration = Date.now() - startTime;

        phaseSpan.span.setAttribute('phase.duration_ms', duration);
        phaseSpan.end({ 'phase.status': 'success' });

        return result;
      } catch (error) {
        phaseSpan.recordError(error);
        phaseSpan.end({ 'phase.status': 'error' });
        throw error;
      }
    });
  }

  /**
   * Trace Ollama operations
   */
  traceOllamaOperation(operation, model) {
    return this.startSpan(`ollama.${operation}`, {
      kind: opentelemetry.SpanKind.CLIENT,
      attributes: {
        'ollama.operation': operation,
        'ollama.model': model,
        'ollama.endpoint': 'http://localhost:11434',
      },
    });
  }

  /**
   * Trace cache operations
   */
  traceCacheOperation(operation, hit) {
    const span = this.startSpan(`cache.${operation}`, {
      attributes: {
        'cache.operation': operation,
        'cache.hit': hit,
      },
    });

    return span;
  }

  /**
   * Trace IPC operations
   */
  traceIPC(channel, direction = 'receive') {
    return this.startSpan(`ipc.${direction}`, {
      kind: direction === 'receive' ? opentelemetry.SpanKind.SERVER : opentelemetry.SpanKind.CLIENT,
      attributes: {
        'ipc.channel': channel,
        'ipc.direction': direction,
      },
    });
  }

  /**
   * Create distributed trace context for cross-process communication
   */
  injectContext(carrier = {}) {
    const activeSpan = opentelemetry.trace.getActiveSpan();
    if (activeSpan) {
      const context = opentelemetry.trace.setSpan(
        opentelemetry.context.active(),
        activeSpan
      );
      
      opentelemetry.propagation.inject(context, carrier);
    }
    return carrier;
  }

  /**
   * Extract trace context from carrier
   */
  extractContext(carrier) {
    return opentelemetry.propagation.extract(
      opentelemetry.context.active(),
      carrier
    );
  }

  /**
   * Get metrics
   */
  getMetrics() {
    return {
      ...this.metrics,
      active_spans: this.spans.size,
    };
  }

  /**
   * Graceful shutdown
   */
  async shutdown() {
    // End all active spans
    for (const [spanId, span] of this.spans) {
      span.end();
    }
    this.spans.clear();

    // Shutdown SDK
    if (this.sdk) {
      await this.sdk.shutdown();
    }

    console.log('🔭 OpenTelemetry tracing shutdown complete');
  }
}

// Singleton instance
let tracingInstance = null;

function getTracing() {
  if (!tracingInstance) {
    tracingInstance = new DistributedTracing();
  }
  return tracingInstance;
}

module.exports = {
  DistributedTracing,
  getTracing,
};
/**
 * @fileoverview Enterprise observability with OpenTelemetry
 * @module Telemetry
 * @author Digimundo Team
 * @version 2.0.0
 */

import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { 
  ConsoleSpanExporter,
  SimpleSpanProcessor,
  BatchSpanProcessor
} from '@opentelemetry/sdk-trace-base';
import { PrometheusExporter } from '@opentelemetry/exporter-prometheus';
import { MeterProvider, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';
import * as api from '@opentelemetry/api';
import pino from 'pino';
import { EventEmitter } from 'events';

/**
 * Telemetry configuration
 */
export interface ITelemetryConfig {
  serviceName: string;
  serviceVersion: string;
  environment: string;
  jaegerEndpoint?: string;
  prometheusPort?: number;
  logLevel?: 'trace' | 'debug' | 'info' | 'warn' | 'error' | 'fatal';
  enableConsoleExport?: boolean;
  enableAutoInstrumentation?: boolean;
  customAttributes?: Record<string, string>;
}

/**
 * Custom span attributes for Digimundo
 */
export enum DigiSpanAttributes {
  AGENT_ID = 'digimundo.agent.id',
  AGENT_TYPE = 'digimundo.agent.type',
  MESSAGE_ID = 'digimundo.message.id',
  MESSAGE_PRIORITY = 'digimundo.message.priority',
  MODEL_NAME = 'digimundo.model.name',
  CACHE_HIT = 'digimundo.cache.hit',
  MEMORY_TYPE = 'digimundo.memory.type',
  OPERATION_TYPE = 'digimundo.operation.type',
}

/**
 * Custom metrics for Digimundo
 */
export interface IDigimundoMetrics {
  agentCount: api.UpDownCounter;
  messageCount: api.Counter;
  messageLatency: api.Histogram;
  memoryUsage: api.ObservableGauge;
  errorRate: api.ObservableGauge;
  cacheHitRate: api.ObservableGauge;
  modelInferenceTime: api.Histogram;
  queueSize: api.ObservableGauge;
}

/**
 * Structured logger
 */
export class StructuredLogger {
  private logger: pino.Logger;

  constructor(config: ITelemetryConfig) {
    this.logger = pino({
      name: config.serviceName,
      level: config.logLevel || 'info',
      formatters: {
        level: (label) => ({ level: label }),
        bindings: (bindings) => ({
          pid: bindings.pid,
          host: bindings.hostname,
          service: config.serviceName,
          version: config.serviceVersion,
          environment: config.environment,
        }),
      },
      timestamp: pino.stdTimeFunctions.isoTime,
      serializers: {
        err: pino.stdSerializers.err,
        error: pino.stdSerializers.err,
      },
    });
  }

  /**
   * Log with trace context
   */
  public logWithContext(
    level: 'trace' | 'debug' | 'info' | 'warn' | 'error' | 'fatal',
    message: string,
    context?: Record<string, any>
  ): void {
    const span = api.trace.getActiveSpan();
    const spanContext = span?.spanContext();

    const logData = {
      ...context,
      traceId: spanContext?.traceId,
      spanId: spanContext?.spanId,
      traceFlags: spanContext?.traceFlags,
    };

    this.logger[level](logData, message);
  }

  public trace(message: string, context?: Record<string, any>): void {
    this.logWithContext('trace', message, context);
  }

  public debug(message: string, context?: Record<string, any>): void {
    this.logWithContext('debug', message, context);
  }

  public info(message: string, context?: Record<string, any>): void {
    this.logWithContext('info', message, context);
  }

  public warn(message: string, context?: Record<string, any>): void {
    this.logWithContext('warn', message, context);
  }

  public error(message: string, error?: Error, context?: Record<string, any>): void {
    this.logWithContext('error', message, { ...context, error });
  }

  public fatal(message: string, error?: Error, context?: Record<string, any>): void {
    this.logWithContext('fatal', message, { ...context, error });
  }
}

/**
 * Telemetry system
 */
export class TelemetrySystem extends EventEmitter {
  private sdk?: NodeSDK;
  private tracer: api.Tracer;
  private meter: api.Meter;
  private logger: StructuredLogger;
  private metrics: IDigimundoMetrics;
  private metricsData: Map<string, any> = new Map();

  constructor(private readonly config: ITelemetryConfig) {
    super();
    
    this.logger = new StructuredLogger(config);
    this.tracer = api.trace.getTracer(config.serviceName, config.serviceVersion);
    this.meter = api.metrics.getMeter(config.serviceName, config.serviceVersion);
    this.metrics = this.setupMetrics();
    
    this.initialize();
  }

  /**
   * Initialize OpenTelemetry
   */
  private initialize(): void {
    const resource = new Resource({
      [SemanticResourceAttributes.SERVICE_NAME]: this.config.serviceName,
      [SemanticResourceAttributes.SERVICE_VERSION]: this.config.serviceVersion,
      [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: this.config.environment,
      ...this.config.customAttributes,
    });

    // Setup exporters
    const traceExporter = this.config.jaegerEndpoint
      ? new JaegerExporter({
          endpoint: this.config.jaegerEndpoint,
        })
      : new ConsoleSpanExporter();

    const spanProcessor = this.config.enableConsoleExport
      ? new SimpleSpanProcessor(new ConsoleSpanExporter())
      : new BatchSpanProcessor(traceExporter);

    // Setup SDK
    this.sdk = new NodeSDK({
      resource,
      instrumentations: this.config.enableAutoInstrumentation
        ? [getNodeAutoInstrumentations()]
        : [],
      spanProcessor,
    });

    // Start SDK
    this.sdk.start()
      .then(() => {
        this.logger.info('OpenTelemetry initialized successfully');
        this.emit('initialized');
      })
      .catch((error) => {
        this.logger.error('Failed to initialize OpenTelemetry', error as Error);
        this.emit('error', error);
      });

    // Setup Prometheus metrics exporter
    if (this.config.prometheusPort) {
      const prometheusExporter = new PrometheusExporter(
        { port: this.config.prometheusPort },
        () => {
          this.logger.info(`Prometheus metrics available at http://localhost:${this.config.prometheusPort}/metrics`);
        }
      );
    }
  }

  /**
   * Setup custom metrics
   */
  private setupMetrics(): IDigimundoMetrics {
    return {
      agentCount: this.meter.createUpDownCounter('digimundo.agents.count', {
        description: 'Number of active agents',
        unit: 'agents',
      }),

      messageCount: this.meter.createCounter('digimundo.messages.total', {
        description: 'Total number of messages processed',
        unit: 'messages',
      }),

      messageLatency: this.meter.createHistogram('digimundo.message.latency', {
        description: 'Message processing latency',
        unit: 'ms',
      }),

      memoryUsage: this.meter.createObservableGauge('digimundo.memory.usage', {
        description: 'Memory usage in bytes',
        unit: 'bytes',
      }),

      errorRate: this.meter.createObservableGauge('digimundo.error.rate', {
        description: 'Error rate percentage',
        unit: '%',
      }),

      cacheHitRate: this.meter.createObservableGauge('digimundo.cache.hit_rate', {
        description: 'Cache hit rate percentage',
        unit: '%',
      }),

      modelInferenceTime: this.meter.createHistogram('digimundo.model.inference_time', {
        description: 'Model inference time',
        unit: 'ms',
      }),

      queueSize: this.meter.createObservableGauge('digimundo.queue.size', {
        description: 'Current queue size',
        unit: 'messages',
      }),
    };
  }

  /**
   * Create a new span
   */
  public startSpan(
    name: string,
    options?: api.SpanOptions,
    fn?: (span: api.Span) => Promise<any>
  ): api.Span | Promise<any> {
    const span = this.tracer.startSpan(name, options);

    if (fn) {
      return api.context.with(api.trace.setSpan(api.context.active(), span), async () => {
        try {
          const result = await fn(span);
          span.setStatus({ code: api.SpanStatusCode.OK });
          return result;
        } catch (error) {
          span.recordException(error as Error);
          span.setStatus({
            code: api.SpanStatusCode.ERROR,
            message: (error as Error).message,
          });
          throw error;
        } finally {
          span.end();
        }
      });
    }

    return span;
  }

  /**
   * Record agent activity
   */
  public recordAgentActivity(
    agentId: string,
    agentType: string,
    operation: string,
    duration: number,
    success: boolean
  ): void {
    const span = this.tracer.startSpan(`agent.${operation}`);
    
    span.setAttributes({
      [DigiSpanAttributes.AGENT_ID]: agentId,
      [DigiSpanAttributes.AGENT_TYPE]: agentType,
      [DigiSpanAttributes.OPERATION_TYPE]: operation,
      'operation.success': success,
      'operation.duration': duration,
    });

    if (!success) {
      span.setStatus({ code: api.SpanStatusCode.ERROR });
    }

    span.end();

    // Update metrics
    this.metrics.messageLatency.record(duration, {
      agent_type: agentType,
      operation,
      success: String(success),
    });
  }

  /**
   * Record message processing
   */
  public recordMessage(
    messageId: string,
    priority: string,
    agentId: string,
    processingTime: number
  ): void {
    this.metrics.messageCount.add(1, {
      agent_id: agentId,
      priority,
    });

    this.metrics.messageLatency.record(processingTime, {
      agent_id: agentId,
      priority,
    });

    const span = api.trace.getActiveSpan();
    if (span) {
      span.setAttributes({
        [DigiSpanAttributes.MESSAGE_ID]: messageId,
        [DigiSpanAttributes.MESSAGE_PRIORITY]: priority,
        [DigiSpanAttributes.AGENT_ID]: agentId,
      });
    }
  }

  /**
   * Record model inference
   */
  public recordModelInference(
    modelName: string,
    inferenceTime: number,
    tokenCount: number,
    cached: boolean
  ): void {
    this.metrics.modelInferenceTime.record(inferenceTime, {
      model: modelName,
      cached: String(cached),
    });

    const span = api.trace.getActiveSpan();
    if (span) {
      span.setAttributes({
        [DigiSpanAttributes.MODEL_NAME]: modelName,
        [DigiSpanAttributes.CACHE_HIT]: cached,
        'model.tokens': tokenCount,
        'model.inference_time': inferenceTime,
      });
    }
  }

  /**
   * Record memory operation
   */
  public recordMemoryOperation(
    memoryType: string,
    operation: string,
    size: number,
    duration: number
  ): void {
    const span = this.tracer.startSpan(`memory.${operation}`);
    
    span.setAttributes({
      [DigiSpanAttributes.MEMORY_TYPE]: memoryType,
      [DigiSpanAttributes.OPERATION_TYPE]: operation,
      'memory.size': size,
      'operation.duration': duration,
    });

    span.end();
  }

  /**
   * Update observable metrics
   */
  public updateMetrics(data: {
    memoryUsage?: number;
    errorRate?: number;
    cacheHitRate?: number;
    queueSize?: number;
    agentCount?: number;
  }): void {
    for (const [key, value] of Object.entries(data)) {
      if (value !== undefined) {
        this.metricsData.set(key, value);
      }
    }

    // Observable gauges will read from metricsData
    this.metrics.memoryUsage.addCallback((result) => {
      result.observe(this.metricsData.get('memoryUsage') || 0);
    });

    this.metrics.errorRate.addCallback((result) => {
      result.observe(this.metricsData.get('errorRate') || 0);
    });

    this.metrics.cacheHitRate.addCallback((result) => {
      result.observe(this.metricsData.get('cacheHitRate') || 0);
    });

    this.metrics.queueSize.addCallback((result) => {
      result.observe(this.metricsData.get('queueSize') || 0);
    });
  }

  /**
   * Create custom dashboard data
   */
  public getDashboardData(): {
    traces: number;
    metrics: Record<string, any>;
    logs: number;
    health: string;
  } {
    return {
      traces: 0, // Would be fetched from Jaeger
      metrics: Object.fromEntries(this.metricsData),
      logs: 0, // Would be fetched from log aggregator
      health: 'healthy',
    };
  }

  /**
   * Shutdown telemetry
   */
  public async shutdown(): Promise<void> {
    this.logger.info('Shutting down telemetry system...');
    
    if (this.sdk) {
      await this.sdk.shutdown();
    }

    this.logger.info('Telemetry system shutdown complete');
    this.emit('shutdown');
  }
}

/**
 * Singleton instance
 */
let telemetryInstance: TelemetrySystem | null = null;

/**
 * Initialize telemetry
 */
export function initializeTelemetry(config: ITelemetryConfig): TelemetrySystem {
  if (!telemetryInstance) {
    telemetryInstance = new TelemetrySystem(config);
  }
  return telemetryInstance;
}

/**
 * Get telemetry instance
 */
export function getTelemetry(): TelemetrySystem | null {
  return telemetryInstance;
}

/**
 * Decorator for automatic span creation
 */
export function Trace(spanName?: string) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const telemetry = getTelemetry();
      if (!telemetry) {
        return originalMethod.apply(this, args);
      }

      const name = spanName || `${target.constructor.name}.${propertyKey}`;
      
      return telemetry.startSpan(name, {}, async (span) => {
        span.setAttributes({
          'function.name': propertyKey,
          'function.args': JSON.stringify(args).substring(0, 100),
        });

        return originalMethod.apply(this, args);
      });
    };

    return descriptor;
  };
}

/**
 * Decorator for metrics collection
 */
export function Metric(metricName: string) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const startTime = Date.now();
      const telemetry = getTelemetry();

      try {
        const result = await originalMethod.apply(this, args);
        
        if (telemetry) {
          const duration = Date.now() - startTime;
          telemetry.recordAgentActivity(
            'system',
            target.constructor.name,
            propertyKey,
            duration,
            true
          );
        }

        return result;
      } catch (error) {
        if (telemetry) {
          const duration = Date.now() - startTime;
          telemetry.recordAgentActivity(
            'system',
            target.constructor.name,
            propertyKey,
            duration,
            false
          );
        }
        
        throw error;
      }
    };

    return descriptor;
  };
}
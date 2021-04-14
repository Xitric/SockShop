'use strict';

const { diag, DiagConsoleLogger, DiagLogLevel } = require("@opentelemetry/api");
const { NodeTracerProvider } = require("@opentelemetry/node");
const { SimpleSpanProcessor } = require("@opentelemetry/tracing");
const { CollectorTraceExporter } = require("@opentelemetry/exporter-collector");
const { registerInstrumentations } = require("@opentelemetry/instrumentation");
const { HttpInstrumentation } = require("@opentelemetry/instrumentation-http");
const { ExpressInstrumentation } = require("@opentelemetry/instrumentation-express");

const provider = new NodeTracerProvider();

diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.INFO);

provider.addSpanProcessor(
    new SimpleSpanProcessor(
      new CollectorTraceExporter({
        serviceName: process.env.SERVICE_NAME,
        url: `http://collector:55681/v1/trace`,
      })
    )
  );

provider.register();

registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
  ],
  tracerProvider: provider,
});

console.log("tracing initialized");

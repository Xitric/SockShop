# SockShop with OpenTelemetry Instrumentation

This repository contains changes to the [SockShop](https://microservices-demo.github.io/) microservice reference
application from [Weaveworks](https://www.weave.works/) in order to instrument the application with various tracing
agents, such as those for [OpenTelemetry](https://opentelemetry.io/). The original license of the SockShop application
is carried over.

Services are configured to send telemetry data to local OpenTelemetry collectors, which then forward the data to a Humio
cloud account, or optionally a locally running Humio instance.

## Deployment

The `deploy-scripts` folder contains deployment options for a range of platforms we have used in evaluating the
OpenTelemetry instrumentation.

## Load Test

The `load-test` folder contains a load test comparing the performance of various instrumentation techniques. This test
assumes the existence of a Kubernetes cluster, and provides scripts for automatically running long-running tests.

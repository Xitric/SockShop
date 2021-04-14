# SockShop with OpenTelemetry instrumentation
This repository contains changes to the [SockShop](https://microservices-demo.github.io/) microservice reference application from [Weaveworks](https://www.weave.works/) in order to instrument the application with [OpenTelemetry](https://opentelemetry.io/). The original license of the SockShop application is carried over.

Services are configured to send telemetry data to local OpenTelemetry agents, which then forward the data to a Humio cloud account, or optionally a locally running Humio instance.

## Deployment
The `deploy-scripts` folder contains deployment options for a range of platforms we have used in evaluating the OpenTelemetry instrumentation.

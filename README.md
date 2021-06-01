# SockShop with OpenTelemetry Instrumentation

This repository contains changes to the [SockShop](https://microservices-demo.github.io/) microservice reference
application from [Weaveworks](https://www.weave.works/) in order to instrument the application with various tracing
agents, such as those from [OpenTelemetry](https://opentelemetry.io/). The original license of the SockShop application
is carried over.

Services are configured to send telemetry data to local OpenTelemetry collectors, which then forward the data to a Humio
cloud account, or optionally a locally running Humio instance.

This repository contains sample applications and automated test scripts used as part of our Master's Thesis _"System
Observability for Danish Software Companies Using Distributed Architectures"_.

## Directory Structure
- `deploy-scripts`: Deployment options for a range of platforms we have used in evaluating the OpenTelemetry
instrumentation and our Humio exporter.

- `load-test`: Contains a fully automated load test bench comparing the performance of various instrumentation
techniques. This test assumes the existence of a Kubernetes cluster, and provides scripts for automatically executing
long-running tests.

- `services-control`: Three Java microservices copied from the respective SockShop repositories. These microservices
have been updated, by us, to a newer version of Spring Boot to support OTel instrumentation with dependency injection.
The microservices in this directory contain no instrumentation, and they are used as control applications in tests. They
are also used as the base applications for instrumentation with Java agents.

- `services-di`: Four microservices copied from the respective SockShop repositories. The three Java microservices have
been updated, by us, to a newer version of Spring Boot to support OTel instrumentation with dependency injection. We
have also added the dependencies on the dependency injection instrumentation. Lastly, we have instrumented the Node.js
microservice with OTel instrumentation. The microservices in this directory are used to evaluate the performance
overhead of dependency injected instrumentation.

- `special-agent`: Dockerfile for creating an image wrapping the SpecialAgent Java agent. Used in the test to evaluate
the overhead of bytecode instrumentation with SpecialAgent.

- `user-test`: Four scenarios of misconfigured SockShop deployments in a Kubernetes cluster. Used during our user test
to evaluate the utility of the observability pipeline we developed.

## Claim of Ownership
Each directory contains a README with details on our claim of ownership. For a quick overview, we summarize the claims
below:

- The development of the SockShop application is by no means ours to claim. As such, the source code inside the
directories `services-control` and `services-di` is copies of microservices from the SockShop project. These
microservices have been updated, by us, to a newer version of Spring Boot to support tracing with dependency injection
from the [Spring Cloud Sleuth OTel](https://github.com/spring-cloud-incubator/spring-cloud-sleuth-otel) project.

- The `user-test` directory contains a number of deployment scripts for Kubernetes. These deployment scripts
also come from the original SockShop project, but they have been modified to inject faults for various scenarios in our
user tests.

- The `deploy-scripts` directory contains scripts for deploying SockShop on various infrastructures. This is a mixture of
scripts from the SockShop project and our own work.

- The `load-test` directory contains a fully automated performance test bed, for which we claim complete ownership
with the exception of the Kubernetes deployment scripts for the SockShop application. The remaining scripts are ours to
claim.

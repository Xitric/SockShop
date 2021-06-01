# SockShop Microservices with Dependency Injected Trace Instrumentation
This directory contains four microservices from the SockShop project. The three java microservices `carts`, `orders`, and `shipping` have been updated to use a newer version of Spring Boot, and we have added dependencies on the Spring Cloud Sleuth OTel project to dependency inject trace instrumentation. The Node.js microservice `front-end` has similarly been instrumented with OTel via the creation of the file `tracing.js`.

We do not claim ownership of the microservices themselves. However, we do claim ownership of the changes required to add instrumentation. For the Java microservices, this has required changing dependencies in the pom files, changing the Spring `application.properties`, as well as updating the applications from Spring Boot 1.4 to Spring Boot 2.4.4, which resulted in many breaking changes. For the Node.js application, this required creating the `tracing.js` file as well as modifying the run configuration.

Consider this directory to be a series of "forks" of individual repositories, updated with the dependencies required for our Master's Thesis. The original repositories are:

- `carts`: https://github.com/microservices-demo/carts
- `front-end`: https://github.com/microservices-demo/front-end
- `orders`: https://github.com/microservices-demo/orders
- `shipping`: https://github.com/microservices-demo/shipping

## Build
Use the following command to build a new Docker image from within each microservice directory, replacing `<group-name>` and `<version>` as appropriate:

```
sudo GROUP=<group-name> COMMIT=<version> ./scripts/build.sh
```

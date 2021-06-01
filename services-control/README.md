# SockShop Microservices with Dependency Injected Trace Instrumentation
This directory contains three microservices from the SockShop project, which have been updated to use a newer version of Spring Boot to provide the same base configuration as the services in the `services-di` directory. The microservices in this directory are used as the bases for Java agent instrumentation, as well as control applications in performance tests.

We do not claim ownership of the microservices themselves. However, we do claim ownership of the changes required to update the services from Spring Boot 1.4 to Spring Boot 2.4.4, which resulted in many breaking changes.

Consider this directory to be a series of "forks" of individual repositories, updated with the dependencies required for our Master's Thesis. The original repositories are:

- `carts`: https://github.com/microservices-demo/carts
- `orders`: https://github.com/microservices-demo/orders
- `shipping`: https://github.com/microservices-demo/shipping

## Build
Use the following command to build a new Docker image from within each microservice directory, replacing `<group-name>` and `<version>` as appropriate:

```
sudo GROUP=<group-name> COMMIT=<version> ./scripts/build.sh
```

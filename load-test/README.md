# SockShop Load Tests
This directory contains load tests developed using [Locust](https://locust.io/), for activating various parts of the SockShop application. The intention is to see how the application performs both without instrumentation, as well as with instrumentation using various techniques.

These load tests will record request latencies and throughput, while resource consumption of the SockShop services is assumed to be measured by the Kubernetes cluster.

## Running the Tests
Running these tests requires Docker, since the tests will be executed in distributed mode using Docker compose. This enables Locust to utilize multiple cores on the client machine, thus generating a bigger load on the SockShop application.

To run a test, execute the following command, where _name_ is the name of the workload file to execute, and _N_ is the number of worker instances to start up. Each worker will execute a separate portion of the simulated clients:

```bash
SCRIPT=<name> docker-compose up -d --scale worker=<N>
```

For instance, this command will run the `commerce_client` workload with 4 workers:

```bash
SCRIPT=commerce_client.py docker-compose up -d --scale worker=4
```

Once the command has been executed, the locust UI will be accessible at `localhost:8089`.

## Workloads
### Realistic Workload
The file `commerce_client.py` contains a workload that simulates a real user browsing the web page. This client simulates all requests for web resources that are normally invoked when accessing the frontend. These requests were derived from intercepting network traffic with the tool [Postman](https://www.postman.com/) while manually browsing the webshop.

The client performs the following requests (relative weight):
- Opening the catalogue (5)
- View details on a specific product (10)
- Add a product to the basket (7)
- Proceed to checkout and finalize the purchase (5)

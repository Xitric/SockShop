# SockShop Load Tests
This directory contains load tests developed using [Locust](https://locust.io/), for activating various parts of the SockShop application. The intention is to see how the application performs both without instrumentation, as well as with instrumentation using various techniques.

These load tests will record request latencies and throughput, while resource consumption of the SockShop services is assumed to be measured by the Kubernetes cluster. To measure resource consumption, we have used the [Prometheus Community Kubernetes Helm Charts](https://github.com/prometheus-community/helm-charts).

We claim ownership of all work in this directory, with the exception of the SockShop deployment files for Kubernetes, which can be found in `k8s/control`, `k8s/di`, `k8s/otel`, and `k8s/sa`. For each of these deployment files, however, we have added additional declarations for instrumenting applications with dependency injection or Java agents. Thus, these deployment files differ a fair bit from the ones found in the original SockShop repository.

## Directory Structure
- `runner.py`: Python script for automatically executing a performance test of various permutations. The levels for each factor of the test can be configured inside this script, which affects the permutations to run. Expect a regular execution of this script to take more than 30 hours.

- `runLoad.sh`: Shell script to automaticaly fetch the IP address of the SockShop front-end service in Kubernetes and execute a sample Locust workload. Useful for interactive testing and debugging of the test bed.

- `grafana-dashboard.json`: The confifuration of the dashboard we have used inside Grafana for monitoring the execution of the performance tests. It monitors the CPU, memory, and network consumption of all SockShop microservices.

- `docker-compose.yaml`: Docker-compose file for deploying a Locust cluster of one master and a configurable number of workers. See [below](#Locust) for a detailed description.

- `analyzer.py`: Entry-point script for running the analysis step of the performance test results. When a test is done executing, it creates a local directory named `test_results`. The analysis scripts will load these test results and generate PDF graphs using gnuplot.

- `workloads`: Python files describing workloads that Locust workers can execute against the SockShop application. See [below](#Locust) for a detailed description.

- `k8s`: Kubernetes deployment files for the SockShop application with various instrumentation techniques, as well as deployment files for the OTel collector with our Humio exporter, Jaeger with our Humio storage plugin, Istio operator, and a Fluentd service for log collection.

- `analysis`: The actual Python scripts for analyzing the test results, as well as gnuplot files for generating PDF graphs.

## Locust
To run the Locust cluster with docker-compose, the following environment variables must be available (they can be specified in-line when executing the docker-compose command):

- `SCRIPT`: The name of the workload script to execute on the workers. One of:
    - `cart_client.py`: A simple workload that simply queries the contents of the user's cart.
    - `checkout_client.py`: A slightly more complex workload that continuously posts and order to SockShop.
    - `commerce_client.py`: A realistic workload of a user that navigates the entire SockShop web store. This consists of browsing the catalogue, inspecting individual products, adding products to the cart, and proceeding to checkout. This workload was designe by tracing an actual user interacting with SockShop using the [Postman](https://www.postman.com/) interceptor.
- `TEST_NAME`: The name of the test, used to label files in the test_results directory.
- `HOST`: The IP address of the front-end microservice from SockShop, on the form `http://{ip}:{port}`.
- `USERS`: The total number of clients to simulate across all workers.
- `RATE`: The number of new clients to initialize every second. This is used to configure the ramp up speed.
- `DURATION`: The amount of time to run the test, on the form `%Hh%Mm%Ss`. For instance `1h30m0s`.
- `WORKERS`: The number of Locust workers to spin up. Must be at least 1.

## Running the Tests
Running these tests requires Docker, since the tests will be executed in distributed mode using Docker compose. This enables Locust to utilize multiple cores on the client machine, thus generating a bigger load on the SockShop application.

To run a test, first navigate into the file `runer.py` and change the levels of each factor at the top of the file:

- `workloads`: An array of the names of the Locust workloads to execute throughout the test. Must be one of `cart_client`, `checkout_client`, or `commerce_client`.

- `clients`: A dictionary mapping the current workload name to an array of client counts to iterate through during the test.

- `instrumentations`: An array of the names of the instrumentation techniques to include in the test. Must be one of `sa`, `otel`, `di`, or `control`.

Furthermore, it is possible to configure some execution parameters of each permutation:

- `rampup_clients_per_second`: The number of clients to initialize every second.

- `locust_workers`: The number of Locust workers to deploy in the cluster.

- `run_duration`: The amount of seconds to execute each permutation. This should be large enougg to ensure that the system under test stabilizes. The actual duration for each permutation will be longer to allow for the clients to ramp up (affected by client count and ramp up rate), as well as to add some slack at the beginning and end of each permutation execution.

The test is then executed by simply running the file `runner.py`. This file assumes the existence of a locally available Kubernetes cluster.

## Workloads
### View Cart
The file `cart_client.py` contains a sythetic and light-weight workload that simulates a user continuously opening their cart. This causes two services to be invoked in SockShop.

### Checkout
The file `checkout_client.py` contains a  synthetic and heavy-weight workload that simulates a user continuously posting orders against the SockShop application. This causes six services to be invoked, with many remote procedure calls taking place.

### Realistic Workload
The file `commerce_client.py` contains a workload that simulates a real user browsing the web page. This client simulates all requests for web resources that are normally invoked when accessing the frontend. These requests were derived from intercepting network traffic with the tool [Postman](https://www.postman.com/) while manually browsing the webshop.

The client performs the following requests (relative weight):
- Opening the catalogue (5)
- View details on a specific product (10)
- Add a product to the basket (7)
- Proceed to checkout and finalize the purchase (5)

# This file contains a script for automatically executing load tests and
# collecting their data

import os
import time
import json
import subprocess
import requests
from pathlib import Path

# The levels for the client factor
clients = {
    "cart_client": [0, 100, 200, 300, 400, 500, 600, 700, 800],
    "checkout_client": [0, 20, 40, 60, 80],
}
# The levels for the workload factor
workloads = ["cart_client", "checkout_client"]
# The levels for the instrumentation technique factor
instrumentations = ["sa", "otel", "di", "control"]

# Server seems to be able to keep up with this
rampup_clients_per_second = 2
# Seems to be a good distribution
locust_workers = 8
# Time, in seconds, used to run each test
run_duration = 30 * 60

# Grafana queries and their target files
grafana_queries = [
    {
        "name": "cluster_cpu",
        "query": "sum(rate(container_cpu_usage_seconds_total%7Bid%3D%22%2F%22%7D%5B4m%5D))",
    },
    {
        "name": "carts_cpu",
        "query": "sum(rate(container_cpu_usage_seconds_total%7Bcontainer%3D%22carts%22%7D%5B4m%5D))",
    },
    {
        "name": "carts_memory",
        "query": "sum(rate(container_memory_usage_bytes%7Bcontainer%3D%22carts%22%7D%5B5m%5D))",
    },
    {
        "name": "carts_network",
        "query": "sum(rate(container_network_transmit_bytes_total%7Bpod%3D~%22carts.*%22%7D%5B4m%5D))",
    },
    {
        "name": "orders_cpu",
        "query": "sum(rate(container_cpu_usage_seconds_total%7Bcontainer%3D%22orders%22%7D%5B4m%5D))",
    },
    {
        "name": "orders_memory",
        "query": "sum(rate(container_memory_usage_bytes%7Bcontainer%3D%22orders%22%7D%5B5m%5D))",
    },
    {
        "name": "orders_network",
        "query": "sum(rate(container_network_transmit_bytes_total%7Bpod%3D~%22orders.*%22%7D%5B4m%5D))",
    },
    {
        "name": "shipping_cpu",
        "query": "sum(rate(container_cpu_usage_seconds_total%7Bcontainer%3D%22shipping%22%7D%5B4m%5D))",
    },
    {
        "name": "shipping_memory",
        "query": "sum(rate(container_memory_usage_bytes%7Bcontainer%3D%22shipping%22%7D%5B5m%5D))",
    },
    {
        "name": "shipping_network",
        "query": "sum(rate(container_network_transmit_bytes_total%7Bpod%3D~%22shipping.*%22%7D%5B4m%5D))",
    },
]

# Generates the name prefix for all files related to a specific test
def as_test_name(instrumentation, workload, clients):
    return instrumentation + workload + str(clients)

# Converts seconds into a time format understood by Locust
def as_time_string(seconds):
    return time.strftime('%Hh%Mm%Ss', time.gmtime(seconds))

# Calculates the expected time spent for ramping up a test
def get_rampup_time(clients, rate):
    # We'll add a bit of time to be on the safe side
    return (clients / rate) * 1.3

# Starts the Locust cluster in headless mode
def start_locust(name, workload, host, duration, clients, rate, scale):
    os.system(f"TEST_NAME={name} SCRIPT={workload}.py HOST={host} DURATION={duration} USERS={clients} RATE={rate} WORKERS={scale} docker-compose up -d --scale worker={scale}")

# Stops the Locust cluster
def stop_locust():
    os.system("docker-compose down")

# Pull the test results out of the Locust master
def copy_locust_files(test_name):
    os.system(f"docker cp loadtest_master_1:/home/locust/{test_name}_stats.csv test_results/{test_name}/")
    os.system(f"docker cp loadtest_master_1:/home/locust/{test_name}_stats_history.csv test_results/{test_name}/")
    os.system(f"docker cp loadtest_master_1:/home/locust/{test_name}_failures.csv test_results/{test_name}/")
    for worker in range(locust_workers):
        os.system(f"docker cp loadtest_worker_{worker+1}:/home/locust/all-stats.txt test_results/{test_name}/all-stats-{worker+1}.txt")

# Download metric results from Grafana
def copy_grafana_results(test_name, start, end):
    # Login to Grafana
    session = requests.Session()
    session.post("http://10.97.37.12/login", data={"user":"admin","password":"prom-operator"})

    # Pull metrics
    for metric in grafana_queries:
        file_name = metric["name"]
        query = metric["query"]

        response = session.get(f"http://10.97.37.12/api/datasources/proxy/1/api/v1/query_range?query={query}&start={start}&end={end}&step=30")
        with open(f"test_results/{test_name}/{test_name}_{file_name}.json", "w") as outfile:
            json.dump(response.json(), outfile)

# Get the address of the front-end host to send requests to
def get_host():
    get_host_ip_process = subprocess.Popen('kubectl get services | grep "front-end" | grep -Po "NodePort\s*\K(\d+\.\d+\.\d+\.\d+)"', shell=True, stdout=subprocess.PIPE)
    ip = get_host_ip_process.stdout.read()[:-1].decode("utf-8")

    get_host_port_process = subprocess.Popen('kubectl get services | grep "front-end" | grep -Po "<none>\s*\K(\d+)"', shell=True, stdout=subprocess.PIPE)
    port = get_host_port_process.stdout.read()[:-1].decode("utf-8")
    
    return f"http://{ip}:{port}"

# Ensure that the collector is running in the cluster
def start_collector():
    os.system("kubectl apply -f k8s/otel-collector.yaml")
    time.sleep(60)

def stop_collector():
    os.system("kubectl delete -f k8s/otel-collector.yaml")
    time.sleep(60)

def deploy_app(name):
    os.system(f"kubectl apply -f k8s/{name}/sockshop.yaml")
    time.sleep(180)

def remove_app(name):
    os.system(f"kubectl delete -f k8s/{name}/sockshop.yaml")
    time.sleep(180)

def run():
    Path(f"test_results").mkdir(parents=True, exist_ok=True)
    start_collector()

    for test_instrumentation in instrumentations:
        print(f"Deploying app: {test_instrumentation}")
        deploy_app(test_instrumentation)

        # The host changes every time we change instrumentation
        test_host = get_host()
        print(f"New host is {test_host}")

        for test_workload in workloads:
            for test_clients in clients[test_workload]:
                # deploy_app(test_instrumentation)
                # test_host = get_host()
                # print(f"New host is {test_host}")

                test_name = as_test_name(
                    test_instrumentation,
                    test_workload,
                    test_clients,
                )
                Path(f"test_results/{test_name}").mkdir(parents=True, exist_ok=True)

                # Time of test is the base duration, plus time for rampup, plus
                # 60 seconds buffer
                test_duration = run_duration + get_rampup_time(test_clients, rampup_clients_per_second) + 60
                test_duration_string = as_time_string(test_duration)

                # Run load test
                print(f"Running test: {test_name}")
                start_locust(
                    test_name,
                    test_workload,
                    test_host,
                    test_duration_string,
                    test_clients,
                    rampup_clients_per_second,
                    locust_workers,
                )
                print(f"Sleeping for {test_duration} seconds")
                time.sleep(test_duration)

                # Prepare timespan to pull test results from Grafana
                # We go 15 seconds back in time to use some of the buffer we
                # prepared previously. This ensure that we do not get weird
                # values at the start or end of test runs
                grafana_end = time.time() - 15
                grafana_start = grafana_end - run_duration

                print(f"Pulling test results for: {test_name}")

                # Pull test results from Locust
                copy_locust_files(test_name)
                stop_locust()

                # Pull test results from Grafana
                copy_grafana_results(test_name, int(grafana_start), int(grafana_end))

                # remove_app(test_instrumentation)

        print(f"Removing app: {test_instrumentation}")
        remove_app(test_instrumentation)
        print("App removed")
    
    print("Stopping test")
    stop_collector()
    print("Test stopped")

if __name__ == '__main__':
    run()

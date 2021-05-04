import os
import re
import json
import math

def run(path):
    cpu_out = os.path.join(path, 'cpu.csv')
    mem_out = os.path.join(path, 'mem.csv')
    net_out = os.path.join(path, 'net.csv')

    for test in os.listdir(path):
        cpu_in = os.path.join(path, test, f'{test}_carts_cpu.json')
        __analyze_data(cpu_in, cpu_out, test)

        mem_in = os.path.join(path, test, f'{test}_carts_memory.json')
        __analyze_data(mem_in, mem_out, test)

        net_in = os.path.join(path, test, f'{test}_carts_network.json')
        __analyze_data(net_in, net_out, test)

def __get_client_count(test_name):
    result = re.search(r'\D(\d+)$', test_name)
    return int(result.group(1))

def __get_technique(test_name):
    result = re.search(r'(sa|otel|di|control)', test_name)
    return result.group(1)

def __get_workload(test_name):
    result = re.search(r'(sa|otel|di|control)([\D\_]+)\d', test_name)
    return result.group(2)

def __analyze_data(input_path, output_path, test_name):
    with open(input_path, 'r') as file:
        data_json = json.load(file)
        metrics = data_json['data']['result'][0]['values']

        # Min, max, avg
        min_v = None
        max_v = None
        sum_v = 0
        n = 0
        for metric in metrics:
            value = float(metric[1])
            if min_v == None or min_v > value:
                min_v = value
            if max_v == None or max_v < value:
                max_v = value
            sum_v = sum_v + value
            n = n + 1
        
        avg = sum_v / n

        # Stdev
        stdev_sum = 0
        for metric in metrics:
            value = float(metric[1])
            stdev_sum = stdev_sum + (value - avg) ** 2
        
        stdev = math.sqrt(stdev_sum / (n - 1))
    
    with open(output_path, 'a') as file:
        file.write(f'{__get_technique(test_name)},{__get_workload(test_name)},{__get_client_count(test_name)},{min_v},{max_v},{avg},{stdev}\n')

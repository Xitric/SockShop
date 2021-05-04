import os
import re

out_file = "latencies.csv"

def run(path):
    out_path = os.path.join(path, out_file)

    for test in os.listdir(path):
        clients = __get_client_count(test)
        stats_path = os.path.join(path, test, f'{test}_stats.csv')

        __collect_latency_metrics(stats_path, out_path, test, clients)

def __get_client_count(test_name):
    result = re.search(r'\D(\d+)$', test_name)
    return int(result.group(1))

def __get_technique(test_name):
    result = re.search(r'(sa|otel|di|control)', test_name)
    return result.group(1)

def __get_workload(test_name):
    result = re.search(r'(sa|otel|di|control)([\D\_]+)\d', test_name)
    return result.group(2)

def __collect_latency_metrics(stats_path, result_path, test_name, clients):
    avg = 0

    if clients != 0:
        with open(stats_path, 'r') as file:
            # Skip header line
            file.readline()

            for line in file:
                entry = StatsEntry(line)
                if entry.requests > clients:
                    avg = entry.response_avg
    
    with open(out_file, 'a') as file:
        file.write(f'{__get_technique(test_name)},{__get_workload(test_name)},{__get_client_count(test_name)},{avg}\n')
        
class HistoryEntry:
    def __init__(self, line):
        entries = line.split(',')
        self.timestamp = int(entries[0])
        self.users = int(entries[1])
        self.type = entries[2]
        self.name = entries[3]
        self.request_rate = float(entries[4])
        self.failure_rate = float(entries[5])
        self.p50 = float(entries[6])
        self.p66 = float(entries[7])
        self.p75 = float(entries[8])
        self.p80 = float(entries[9])
        self.p90 = float(entries[10])
        self.p95 = float(entries[11])
        self.p98 = float(entries[12])
        self.p99 = float(entries[13])
        self.p999 = float(entries[14])
        self.p9999 = float(entries[15])
        self.p100 = float(entries[16])
        self.request_total = int(entries[17])
        self.failure_total = int(entries[18])
        self.med_response_total = float(entries[19])
        self.avg_response_total = float(entries[20])
        self.min_response_total = float(entries[21])
        self.max_response_total = float(entries[22])
        self.avg_content_total = float(entries[23])

class StatsEntry:
    def __init__(self, line):
        entries = line.split(',')
        self.type = entries[0]
        self.name = entries[1]
        self.requests = int(entries[2])
        self.failures = int(entries[3])
        self.response_med = float(entries[4])
        self.response_avg = float(entries[5])
        self.response_min = float(entries[6])
        self.response_max = float(entries[7])
        self.content_size_avg = float(entries[8])
        self.request_rate = float(entries[9])
        self.failurerate = float(entries[10])
        self.p50 = float(entries[11])
        self.p66 = float(entries[12])
        self.p75 = float(entries[13])
        self.p80 = float(entries[14])
        self.p90 = float(entries[15])
        self.p95 = float(entries[16])
        self.p98 = float(entries[17])
        self.p99 = float(entries[18])
        self.p999 = float(entries[19])
        self.p9999 = float(entries[20])
        self.p100 = float(entries[21])

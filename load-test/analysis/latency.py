import os
import subprocess
from . import indexer

from typing import Optional

temp_output = os.path.join(os.path.dirname(__file__), 'gnuplot/data.csv')


class StatsEntry:
    def __init__(self, line):
        entries = line.split(',')
        self.type = entries[0]
        self.name = entries[1]
        self.requests = 0 if 'N/A' in entries[2] else int(entries[2])
        self.failures = 0 if 'N/A' in entries[3] else int(entries[3])
        self.response_med = 0 if 'N/A' in entries[4] else float(entries[4])
        self.response_avg = 0 if 'N/A' in entries[5] else float(entries[5])
        self.response_min = 0 if 'N/A' in entries[6] else float(entries[6])
        self.response_max = 0 if 'N/A' in entries[7] else float(entries[7])
        self.content_size_avg = 0 if 'N/A' in entries[8] else float(entries[8])
        self.request_rate = 0 if 'N/A' in entries[9] else float(entries[9])
        self.failure_rate = 0 if 'N/A' in entries[10] else float(entries[10])
        self.p50 = 0 if 'N/A' in entries[11] else float(entries[11])
        self.p66 = 0 if 'N/A' in entries[12] else float(entries[12])
        self.p75 = 0 if 'N/A' in entries[13] else float(entries[13])
        self.p80 = 0 if 'N/A' in entries[14] else float(entries[14])
        self.p90 = 0 if 'N/A' in entries[15] else float(entries[15])
        self.p95 = 0 if 'N/A' in entries[16] else float(entries[16])
        self.p98 = 0 if 'N/A' in entries[17] else float(entries[17])
        self.p99 = 0 if 'N/A' in entries[18] else float(entries[18])
        self.p999 = 0 if 'N/A' in entries[19] else float(entries[19])
        self.p9999 = 0 if 'N/A' in entries[20] else float(entries[20])
        self.p100 = 0 if 'N/A' in entries[21] else float(entries[21])


class HistoryEntry:
    def __init__(self, line):
        entries = line.split(',')
        self.timestamp = 0 if 'N/A' in entries[0] else int(entries[0])
        self.users = 0 if 'N/A' in entries[1] else int(entries[1])
        self.type = entries[2]
        self.name = entries[3]
        self.request_rate = 0 if 'N/A' in entries[4] else float(entries[4])
        self.failure_rate = 0 if 'N/A' in entries[5] else float(entries[5])
        self.p50 = 0 if 'N/A' in entries[6] else float(entries[6])
        self.p66 = 0 if 'N/A' in entries[7] else float(entries[7])
        self.p75 = 0 if 'N/A' in entries[8] else float(entries[8])
        self.p80 = 0 if 'N/A' in entries[9] else float(entries[9])
        self.p90 = 0 if 'N/A' in entries[10] else float(entries[10])
        self.p95 = 0 if 'N/A' in entries[11] else float(entries[11])
        self.p98 = 0 if 'N/A' in entries[12] else float(entries[12])
        self.p99 = 0 if 'N/A' in entries[13] else float(entries[13])
        self.p999 = 0 if 'N/A' in entries[14] else float(entries[14])
        self.p9999 = 0 if 'N/A' in entries[15] else float(entries[15])
        self.p100 = 0 if 'N/A' in entries[16] else float(entries[16])
        self.request_total = 0 if 'N/A' in entries[17] else int(entries[17])
        self.failure_total = 0 if 'N/A' in entries[18] else int(entries[18])
        self.med_response_total = 0 if 'N/A' in entries[19] else float(entries[19])
        self.avg_response_total = 0 if 'N/A' in entries[20] else float(entries[20])
        self.min_response_total = 0 if 'N/A' in entries[21] else float(entries[21])
        self.max_response_total = 0 if 'N/A' in entries[22] else float(entries[22])
        self.avg_content_total = 0 if 'N/A' in entries[23] else float(entries[23])


def run(in_path: str, out_path: str):
    index = indexer.index(in_path)
    __analyze_data(index, in_path, out_path)


def __analyze_data(index: indexer.Index, in_path: str, out_path: str):
    for workload in index:
        for clients in sorted(index[workload], key=lambda key: int(key)):
            if clients == 0:
                continue

            # clients,control_med,control_50,control_95,control_failures,control_request_rate,di_...
            result_entry = f'{clients},'

            for technique in index[workload][clients]:
                test_name = f'{technique}{workload}{clients}'
                data_file = os.path.join(in_path, test_name, f'{test_name}_stats.csv')

                stats = __extract_stats(data_file)
                result_entry += f'{stats.response_med},{stats.p50},{stats.p95},{stats.failures},{stats.request_rate},'

            with open(temp_output, 'a') as file:
                file.write(f'{result_entry[:-1]}\n')

        gnuplot_script_location = os.path.join(os.path.dirname(__file__), f'gnuplot/latency.plg')
        subprocess.call(
            f'gnuplot -e "data=\'{temp_output}\'; result=\'{workload}_latency.pdf\'" {gnuplot_script_location}',
            cwd=out_path)
        os.remove(temp_output)


def __extract_stats(in_path: str) -> Optional[StatsEntry]:
    with open(in_path, 'r') as file:
        # Skip header line
        file.readline()

        for line in file:
            entry = StatsEntry(line)
            if (entry.type == 'GET' and entry.name == '/cart') or \
                    (entry.type == 'POST' and entry.name == '/orders'):
                return entry

    return None

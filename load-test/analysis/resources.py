import os
import json
import math
import subprocess
from . import indexer

data_types = ["cpu", "memory", "network"]
temp_output = os.path.join(os.path.dirname(__file__), 'gnuplot/data.csv')


def run(in_path: str, out_path: str):
    index = indexer.index(in_path)

    for data_type in data_types:
        __analyze_data(index, in_path, out_path, data_type)


def __analyze_data(index: indexer.Index, in_path: str, out_path: str, data_type: str):
    for workload in index:
        for clients in sorted(index[workload], key=lambda key: int(key)):
            # clients,control_avg,control_err,di_avg,di_err,...
            result_entry = f'{clients},'

            for technique in index[workload][clients]:
                test_name = f'{technique}{workload}{clients}'
                data_file = os.path.join(in_path, test_name, f'{test_name}_carts_{data_type}.json')
                avg = __compute_avg(data_file)
                stdev = __compute_stdev(data_file, avg)
                result_entry += f'{avg},{stdev},'

            with open(temp_output, 'a') as file:
                file.write(f'{result_entry[:-1]}\n')

        gnuplot_script_location = os.path.join(os.path.dirname(__file__), f'gnuplot/{data_type}_usage.plg')
        subprocess.call(
            f'gnuplot -e "data=\'{temp_output}\'; result=\'{workload}_{data_type}.pdf\'" {gnuplot_script_location}',
            cwd=out_path)
        os.remove(temp_output)


def __compute_avg(in_path: str) -> float:
    with open(in_path, 'r') as file:
        data_json = json.load(file)
        metrics = data_json['data']['result'][0]['values']

        min_v = None
        max_v = None
        sum_v = 0
        n = 0
        for metric in metrics:
            value = float(metric[1])
            if min_v is None or min_v > value:
                min_v = value
            if max_v is None or max_v < value:
                max_v = value
            sum_v += value
            n += 1

        return sum_v / n


def __compute_stdev(in_path: str, avg: float) -> float:
    with open(in_path, 'r') as file:
        data_json = json.load(file)
        metrics = data_json['data']['result'][0]['values']

        stdev_sum = 0
        n = 0
        for metric in metrics:
            value = float(metric[1])
            stdev_sum += (value - avg) ** 2
            n += 1

        return math.sqrt(stdev_sum / (n - 1))

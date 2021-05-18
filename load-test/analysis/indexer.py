import os
import re

from typing import Dict, List

Index = Dict[str, Dict[int, List[str]]]


def index(in_path: str) -> Index:
    workload_index: Index = {}

    for test in os.listdir(in_path):
        workload = get_workload(test)
        clients = get_client_count(test)
        technique = get_technique(test)

        client_index = workload_index.get(workload, {})
        technique_index = client_index.get(clients, [])
        technique_index.append(technique)
        client_index[clients] = technique_index
        workload_index[workload] = client_index

    return workload_index


def get_client_count(test_name: str) -> int:
    result = re.search(r'\D(\d+)$', test_name)
    return int(result.group(1))


def get_technique(test_name: str) -> str:
    result = re.search(r'(sa|otel|di|control)', test_name)
    return result.group(1)


def get_workload(test_name: str) -> str:
    result = re.search(r'(sa|otel|di|control)([\D_]+)\d', test_name)
    return result.group(2)

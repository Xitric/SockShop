# This file contains a script for automatically analyzing the test data

import os
import analysis

if __name__ == '__main__':
    test_dir = os.path.abspath('../test_results')
    result_dir = os.path.abspath('.')
    analysis.run_latency(test_dir, result_dir)
    analysis.run_resources(test_dir, result_dir)


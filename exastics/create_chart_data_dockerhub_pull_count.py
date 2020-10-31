#!/usr/bin/env python3

import exastics.chartdata
import json
import sys


if __name__ == '__main__':
    base_dir = sys.argv[1]
    output_file = sys.argv[2]

    chart_data = [
        {
            'series': 'pull_count',
            'points': list(map(
                lambda obj: {'x': obj[0], 'y': obj[1]['pull_count']},
                exastics.chartdata.get_datetime_and_json_data(base_dir)
            ))
        }
    ]

    with open(output_file, 'w') as f:
        json.dump(chart_data, f, indent=4)
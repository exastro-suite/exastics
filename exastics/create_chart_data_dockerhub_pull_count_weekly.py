#!/usr/bin/env python3

import exastics.chartdata
import json
import sys
import datetime


if __name__ == '__main__':
    base_dir = sys.argv[1]
    output_file = sys.argv[2]

    #
    # 日次データ取得
    #
    history = sorted(
        list(exastics.chartdata.get_datetime_and_json_data(base_dir)),
        key=lambda obj: obj[0]
    )

    #
    # 週ごとの最終pull_countを保持
    #
    weekly_data = {}

    for dt_str, data in history:

        dt = datetime.datetime.fromisoformat(dt_str)

        # ISO週番号
        iso_year, iso_week, _ = dt.isocalendar()

        week_key = f"{iso_year}-{iso_week:02d}"

        # 同じ週なら後ろのデータで上書き
        # → その週の最新データが残る
        weekly_data[week_key] = {
            'date': dt,
            'pull_count': data['pull_count']
        }

    #
    # 週順に並べ替え
    #
    weekly_entries = sorted(
        weekly_data.values(),
        key=lambda obj: obj['date']
    )

    #
    # 前週との差分計算
    #
    points = []

    previous_pull_count = None

    for entry in weekly_entries:

        current_pull_count = entry['pull_count']

        if previous_pull_count is None:
            weekly_increase = 0
        else:
            weekly_increase = (
                current_pull_count -
                previous_pull_count
            )

        points.append({
            'x': entry['date'].strftime('%Y-%m-%d'),
            'y': weekly_increase
        })

        previous_pull_count = current_pull_count

    chart_data = [
        {
            'series': 'weekly_pull_count',
            'points': points
        }
    ]

    with open(output_file, 'w') as f:
        json.dump(chart_data, f, indent=4)

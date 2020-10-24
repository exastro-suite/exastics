#!/usr/bin/env python3

import datetime
import dateutil.parser
import json
import pathlib
import os
import sys


class GitHubTag:
    def __init__(self, release):
        self.tag_name = release['tag_name']
        self.id = release['id']

        self.assets = []
        for asset in release['assets']:
            self.assets.append(GitHubAsset(asset))


class GitHubAsset:
    def __init__(self, asset):
        self.id = asset['id']
        self.download_count = asset['download_count']


def get_datetime_from_filename(filename):
    return_value = None

    name, ext = os.path.splitext(filename)
    if ext == '.json':
        try:
            dateutil.parser.isoparse(name)
            return_value = name
        except ValueError:
            pass
    
    return return_value


def get_github_releases(base_dir):
    for dirpath, _, filenames in os.walk(base_dir):
        for filename in filenames:
            dt = get_datetime_from_filename(filename)
            if not dt:
                continue

            try:
                with open(pathlib.PurePath(dirpath, filename)) as file:
                    github_releases = json.load(file)
            except Exception as e:
                print(str(e), type(e))
                continue

            yield (dt, github_releases)


def append_tag_time_series(tag_time_series, dt, github_tag):
    try:
        tag_time_series.setdefault(github_tag.tag_name, []).append((dt, github_tag))
    except AttributeError as e:
        print(github_tag)
        raise


def collect_tag_time_series(tag_time_series, dt, releases):
    all_assets = []

    for release in releases:
        github_tag = GitHubTag(release)
        append_tag_time_series(tag_time_series, dt, github_tag)
                
        all_assets += release['assets']
    
    presudo_github_tag = GitHubTag({
        'tag_name': 'total',
        'id': 0,
        'assets': all_assets
    })

    append_tag_time_series(tag_time_series, dt, presudo_github_tag)


def create_chart_data_entry(tag_name):
    download_counts = {}

    def download_counter(github_tag):
        for asset in github_tag.assets:
            download_counts[asset.id] = asset.download_count
        
        return sum(download_counts.values())

    return {
        'series': tag_name,
        'points': list(map(
            lambda obj: {'x': obj[0], 'y': download_counter(obj[1])},
            sorted(tag_time_series[tag_name], key=lambda obj: obj[0])
        ))
    }


def create_chart_data(tag_time_series):
    chart_data = []

    for tag_name in sorted(tag_time_series.keys(), reverse=True):
        entry = create_chart_data_entry(tag_name)

        if tag_name == 'total':
            chart_data.insert(0, entry)
        else:
            chart_data.append(entry)

    return chart_data


if __name__ == '__main__':
    base_dir = sys.argv[1]
    output_file = sys.argv[2]

    tag_time_series = {}
    for dt, github_releases in get_github_releases(base_dir):
        collect_tag_time_series(tag_time_series, dt, github_releases)

    chart_data = create_chart_data(tag_time_series)

    with open(output_file, 'w') as f:
        json.dump(chart_data, f, indent=4)
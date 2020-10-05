#!/usr/bin/env python3

import datetime
import pathlib
import pytz
import os
import requests
import sys
import urllib.parse

try:
    github_account = sys.argv[1]
    github_repository = sys.argv[2]

    dt = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

    current_year_month = dt.strftime('%Y-%m')
    print(f'current_year_month ... {current_year_month}')

    current_date_time = dt.isoformat(timespec='seconds')
    print(f'current_date_time ... {current_date_time}')
    
    url_parts = (
        'https',
        'api.github.com',
        urllib.parse.quote(f'/repos/{github_account}/{github_repository}/releases'),
        '',
        '',
        ''
    )
    url = urllib.parse.urlunparse(url_parts)
    print(f'url ... {url}')
    
    response = requests.get(url, headers={'Accept': 'application/vnd.github.v3+json'})
    print(f'response.status_code ... {response.status_code}')
    print(f'response.text ... {response.text}')
    
    if response.status_code != requests.codes.ok:
        raise Exception('HTTP status code is not 200')

    filepath = pathlib.PurePath(github_repository, 'releases', current_year_month, current_date_time + '.json')
    print(f'filepath ... {filepath}')

    os.makedirs(filepath.parent, exist_ok=True)
    with open(filepath, mode='w') as f:
        f.write(response.text)
    
    print("succeeded")

except Exception as e:
    print("failed")
    print(e)

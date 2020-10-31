import exastics.collect
import pathlib
import sys
import urllib.parse


if __name__ == '__main__':
    dockerhub_account = sys.argv[1]
    dockerhub_repository = sys.argv[2]

    url_parts = (
        'https',
        'hub.docker.com',
        urllib.parse.quote(f'/v2/repositories/{dockerhub_account}/{dockerhub_repository}/'),
        '',
        '',
        ''
    )

    headers = {
        'Accept': 'application/json'
    }

    output_dir = pathlib.PurePath(dockerhub_repository, 'dockerhub-repository')

    exastics.collect.publish_api(url_parts, headers, output_dir)

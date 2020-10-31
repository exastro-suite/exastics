import exastics.collect
import pathlib
import sys
import urllib.parse


if __name__ == '__main__':
    github_account = sys.argv[1]
    github_repository = sys.argv[2]

    url_parts = (
        'https',
        'api.github.com',
        urllib.parse.quote(f'/repos/{github_account}/{github_repository}/releases'),
        '',
        '',
        ''
    )

    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    output_dir = pathlib.PurePath(github_repository, 'github-releases')

    exastics.collect.publish_api(url_parts, headers, output_dir)

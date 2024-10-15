#!/bin/bash -x

python3 -m exastics.publish_github_api_releases exastro-suite it-automation
python3 -m exastics.publish_github_api_releases exastro-suite oase
python3 -m exastics.publish_github_api_releases exastro-suite Settings-CloudSystemTemplate-1st

python3 -m exastics.publish_dockerhub_api_repository exastro it-automation
python3 -m exastics.publish_dockerhub_api_repository exastro exastro-it-automation-migration

python3 -m exastics.create_chart_data_github_download_count ./it-automation/github-releases                    ./docs/assets/chart-data/it-automation-github-download-count.json
python3 -m exastics.create_chart_data_github_download_count ./oase/github-releases                             ./docs/assets/chart-data/oase-github-download-count.json
python3 -m exastics.create_chart_data_github_download_count ./Settings-CloudSystemTemplate-1st/github-releases ./docs/assets/chart-data/Settings-CloudSystemTemplate-1st-github-download-count.json

python3 -m exastics.create_chart_data_dockerhub_pull_count ./it-automation/dockerhub-repository/ ./docs/assets/chart-data/it-automation-dockerhub-pull-count.json

python3 -m exastics.create_chart_data_dockerhub_pull_count ./exastro-it-automation-migration/dockerhub-repository/ ./docs/assets/chart-data/exastro-it-automation-dockerhub-pull-count.json

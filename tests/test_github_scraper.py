import json
import pytest
from github_scraper_test.scraper import GitHubScraper
from requests.exceptions import ProxyError


def base_success_case(input_file, output_file):
	github_scraper = GitHubScraper(input_file=input_file, output_file=output_file)
	github_scraper.run_scraper()
	with open(github_scraper.output_data_file_name, 'r') as output_file:
		result = json.loads(output_file.read())
		for url in result:
			assert list(url.keys()) == ['url']


def base_failed_case(input_file, exeption_type):
	github_scraper = GitHubScraper(input_file=input_file, 
								   output_file='any_file.json')
	with pytest.raises(exeption_type):
		github_scraper.run_scraper()


def test_success_repos():
	github_scraper = GitHubScraper(input_file='tests/input_fixtures/input_fixture_success_repos.json', 
								   output_file='tests/output_fixtures/output_fixture_success_repos.json')
	github_scraper.run_scraper()
	with open(github_scraper.output_data_file_name, 'r') as output_file:
		result = json.loads(output_file.read())
		for url in result:
			assert list(url.keys()) == ['url', 'extra']
			assert list(url['extra'].keys()) == ['owner', 'language_stats']


def test_success_issues():
	input_file='tests/input_fixtures/input_fixture_success_issues.json'
	output_file='tests/output_fixtures/output_fixture_success_issues.json'
	base_success_case(input_file, output_file)


def test_success_wikis():
	input_file='tests/input_fixtures/input_fixture_success_wikis.json'
	output_file='tests/output_fixtures/output_fixture_success_wikis.json'
	base_success_case(input_file, output_file)


def test_success_cyrillic():
	input_file='tests/input_fixtures/input_fixture_success_cyrillic.json'
	output_file='tests/output_fixtures/output_fixture_success_cyrillic.json'
	base_success_case(input_file, output_file)


def test_wrong_type():
	input_file='tests/input_fixtures/input_fixture_wrong_type.json'
	base_failed_case(input_file, ValueError)


def test_no_proxies():
	input_file='tests/input_fixtures/input_fixture_no_proxies.json'
	base_failed_case(input_file, KeyError)


def test_no_keywords():
	input_file='tests/input_fixtures/input_fixture_no_keywords.json'
	base_failed_case(input_file, KeyError)


def test_no_input_data_file():
	input_file='tests/input_fixtures/input_fixture_no_input_file.json'
	base_failed_case(input_file, FileNotFoundError)


def test_wrong_proxies():
	input_file='tests/input_fixtures/input_fixture_wrong_proxies.json'
	base_failed_case(input_file, ProxyError)


def test_empty_proxies():
	input_file='tests/input_fixtures/input_fixture_empty_proxies.json'
	base_failed_case(input_file, ValueError)
	
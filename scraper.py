from lxml import html
from random import randint
import json
import requests
import urllib.parse

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class GitHubScraper():

	def __init__(self, input_file='input_data.json', output_file='output_data.json'):
		# base object params
		self.https_proxies = []
		self.base_url = 'https://github.com/'
		self.search_query_url = urllib.parse.urljoin(self.base_url, 'search')
		self.params = {}

		# xpathes
		self.xpath_dict = {'repositories': './/ul[contains(@class, "repo-list")]//a[contains(@class, "v-align-middle")]/@href', 
						   'issues': './/div[contains(@id, "issue_search_results")]//div[contains(@class, "text-normal")]/a/@href',
						   'wikis': './/div[contains(@id, "wiki_search_results")]//div[contains(@class, "text-normal")]/a/@href'}
		self.repo_owner_xpath = './/a[contains(@rel, "author")]/text()'
		self.repo_langs_links_xpath = './/h2[contains(text(), "Languages")]/following-sibling::ul//a'
		self.repo_langs_stats_xpath = './span/text()'

		# filenames
		self.input_data_file_name = input_file
		self.output_data_file_name = output_file


	def read_input_data(self):
		"""Read input data from file."""
		try:
			with open(self.input_data_file_name, 'r') as input_data_file:
				data = json.loads(input_data_file.read())
				self.params['q'] = '+'.join(data['keywords'])
				query_type = data['type'].lower()
				if query_type not in self.xpath_dict.keys():
					raise ValueError('Query type should be Repositories, Issues or Wikis.')
				self.params['type'] = query_type
				self.https_proxies = data['proxies']
		except Exception as e:
			logger.error('Reading from an input file has failed.')
			raise e

	def write_output_data(self, output_data):
		"""Write output data to file."""
		try:
			with open(self.output_data_file_name, 'w') as output_data_file:
				output_data_file.write(output_data)
		except Exception as e:
			logger.error('Writing to output file has failed.')
			raise e

	def random_proxy(self):
		"""Get random proxy."""
		try:
			proxy_id = randint(0, len(self.https_proxies) - 1)
			return {'https': self.https_proxies[proxy_id]}
		except Exception as e:
			logger.error('No proxies!')
			raise e

	def send_request(self, url, params=None):
		"""
		Send GET request using selected proxies.
		url: url for request
		params: params for GET request
		"""
		proxy = self.random_proxy()
		try:
			response = requests.get(url, proxies=proxy, params=params)
			if response.status_code != 200:
				raise HTTPError(f'Status code is not "200": {response.status_code}')
			return html.fromstring(response.content)
		except Exception as e:
			logger.error(f'Request to url: {url} with params: {params} and proxy: {proxy} has failed!')
			raise e


	def run_scraper(self):
		"""Run GitHub scraer. Main method."""
		logger.info('Scraping is started...')
		# read input data and send request for links
		self.read_input_data()
		content_tree = self.send_request(self.search_query_url, self.params)
		links = content_tree.xpath(self.xpath_dict[self.params['type']])
		links_list = [{'url': urllib.parse.urljoin(self.base_url, link)} for link in links]
		logger.info(f'Found {len(links_list)} links at first page.')

		# add additional info in case type of query is 'Repostitories'
		if self.params['type'] == 'repositories':
			logger.info('Scraping extra data for Repositories.')
			for link in links_list:

				# add owner name
				link['extra'] = {'owner': None, 'language_stats': {}}
				extra_content_tree = self.send_request(link['url'])
				link['extra']['owner'] = extra_content_tree.xpath(self.repo_owner_xpath)[0]

				# add languages stats
				languages_links = extra_content_tree.xpath(self.repo_langs_links_xpath)
				for languages_link in languages_links:
					language_data = languages_link.xpath(self.repo_langs_stats_xpath )
					link['extra']['language_stats'][language_data[0]] = language_data[1].rstrip('%')

		# write data to output file
		self.write_output_data(json.dumps(links_list))
		logger.info(f'Scraping is finished. Open {self.output_data_file_name} to see results.')



if __name__ == '__main__':
	github_scraper = GitHubScraper()
	github_scraper.run_scraper()

# encoding: utf-8
import csv
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

__author__ = "Yan Berezkin"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = [""]
__license__ = "Free_To_Use"

__version__ = "1.0.0"
__maintainer__ = "Yan Berezkin"
__email__ = "yan.berezkin@gmail.com"
__status__ = "Development"  # stable


def get_datetime(timestamp):
	"""
	Convert timestamp format: (ex. 1569434133)
	To datetime format: (ex. 2019-09-25 12:55:33)
	:param timestamp:
	:return: datetime_object
	"""
	dt_object = datetime.fromtimestamp(timestamp)
	return dt_object


def get_timestamp(dt_object):
	"""
	Convert datetime format: (ex. 2019-09-25 12:55:33)
	To timestamp format: (ex. 1569434133)
	:param dt_object:
	:return: timestamp
	"""
	timestamp = datetime.timestamp(dt_object)
	return timestamp


class XsellcoAPI:
	HOST = 'https://api.xsellco.com'
	API_VERSION = 'v1'
	URL = '{}/{}'.format(HOST, API_VERSION)

	def __init__(self, user_name, password):
		self.user_name = user_name
		self.password = password
		self.basic = HTTPBasicAuth(self.user_name, self.password)

		self.session = requests.Session()
		self.session.auth = self.basic
		self.session.headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
		}
		self.last_response = None

	def send_request(
			self, method, url, params=None, body=None, json=None,
			request_headers=None):

		response = None
		request_params = {}

		if params:
			request_params.update({'params': params})
		if request_headers:
			request_params.update({'headers': request_headers})

		if json is not None:
			request_params.update({'json': json})
		else:
			request_params['data'] = body

		if method == 'POST':
			response = self.session.post(url, **request_params)

		if method == 'PUT':
			response = self.session.put(url, **request_params)

		if method == 'GET':
			response = self.session.get(url, **request_params)

		self.last_response = response

		if response is not None and response.ok:
			try:
				response.raise_for_status()
			except requests.exceptions.HTTPError as ex:
				raise
		try:
			return response.json()
		except ValueError:
			return response.content
		except Exception as ex:
			print(ex)
			return response

	def get_users(self, user_id=None, username=None, page_limit=100):
		"""
		:param page_limit: integer	Max number of result per request OPTIONAL Max= 100 Default= 100
		:param username: string		Valid username on the client OPTIONAL
		:param user_id: integer		Valid user identifier OPTIONAL
		:return: response_parsed
		"""

		endpoint = 'users'
		url = '{}/{}'.format(self.URL, endpoint)
		params = {'page_limit': page_limit}

		if user_id:
			url = '{}/{}'.format(url, user_id)

		if username:
			params['username'] = str(username)

		return self.send_request('GET', url, params=params)

	def get_channels(
			self, channel_id=None, channel_name=None, channel_type=None,
			channel_country=None, channel_currency=None, page_limit=100):
		"""
		:param page_limit: integer
		:param channel_id:
		:param channel_name:
		:param channel_type: # ['amazon', 'ebay', 'walmart', 'website', 'demo', 'shopify', 'newegg', 'facebook']
		:param channel_country:
		:param channel_currency:
		:return:
		"""
		endpoint = 'channels'
		url = '{}/{}'.format(self.URL, endpoint)
		params = {'page_limit': page_limit}

		params.update({
			'id': channel_id,
			'name': channel_name,
			'type': channel_type,
			'country': channel_country,
			'currency': channel_currency,
		})
		return self.send_request('GET', url, params=params)

	def get_repricer_report(self, channel_name=None):
		endpoint = 'repricers'
		url = '{}/{}'.format(self.URL, endpoint)

		response = self.send_request('GET', url)

		_data = response.decode('utf-8').splitlines()
		reader = csv.DictReader(_data, delimiter=',')
		output = list()
		for line in reader:
			if len(line) != len(reader.fieldnames) and None in line.keys():
				line[reader.fieldnames[-1]] = line[reader.fieldnames[-1]] + ','.join(line[None])
				del line[None]
			output.append(dict(line))
		return output

	def upload_repricer_report(self, file_path):
		endpoint = 'repricers'
		url = '{}/{}'.format(self.URL, endpoint)
		data = open(file_path, 'rb').read()
		response = self.send_request('POST', url, body=data)
		return response

	def repricer_report_to_dict(self, data=None):
		if data is None:
			data = self.get_repricer_report()
		repricer_dict = dict()
		reader = csv.DictReader(data, delimiter=',', quotechar='"')
		for line in reader:
			repricer_dict[line['sku']] = dict(line)
		return repricer_dict

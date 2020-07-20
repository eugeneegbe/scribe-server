'''Add article data to the database
'''

import os
import sys
import json
import pandas as pd

from datetime import datetime

from scribe.models import Article, Reference, Section, Domain
from scribe.main.utils import commit_changes_to_db, get_base_url, get_object_first_key_value


def extract_article_data(file):
	'''Extracts article data from the file and sends object of the data to db
	'''
	article_data = []

	data = pd.read_csv(file, sep='\t').values
	
	for row in data:
				article = {}
					
				article['wd_item'] = row[0]
				article['name'] = row[1]
				article['lang_code'] = row[2]
				article['wd_q_id'] = row[3]
				article['tag'] = row[4]
				article['domain'] = row[6]
				article['redlink'] = row[7]
				article['category'] = row[8]
				article_data.append(article)

			# create article objects at once
	article_data = [ Article(wd_item=article['wd_item'], name=article['name'],
							 wd_q_id=article['wd_q_id'], tag=article['tag'],
							 lang_code=article['lang_code'], red_link=article['redlink'],
							 category=article['category'],
							 domain=article['domain']) for article in article_data]
	return article_data

def extract_reference_data(file, lang_code):
	'''Extracts reference data from the file and sends object of the data to db

	'''

	reference_data = []

	with open(file, encoding='utf-8') as data_file:
		file_data = json.loads(data_file.read())

		if file_data:
			print(file_data[0])
			# file is not empty
			for data in file_data:
				reference = Reference(publisher_name=data['publisher_name'], 
									  wd_q_id=data['wd_q_id'],
									  publication_title=data['publication_title'],
									  summary=data['summary'],
									  url=data['url'],
									  quality=data['quality'],
									  lang_code = lang_code,
									  publication_date=datetime.strptime(data['publication_date'].split('T')[0], '%Y-%m-%d'),
									  content_selection_method=data['content_selection_method'])
				reference_data.append(reference)
		else:
			pass # report an error here

	return reference_data



def extract_section_data(section_data_file):
	section_data = []

	data = pd.read_csv(section_data_file, sep='\t').values
	
	for row in data:
		section = {}
			
		section['order_number'] = row[0]
		section['quality'] = row[1]
		section['label'] = row[2]
		section['wd_q_id'] = row[3]
		section['lang_code'] = row[4]
		section_data.append(section)

	# create article objects at once
	section_data = [ Section(order_number=section['order_number'], label=section['label'],
							 quality=section['quality'], wd_q_id=section['wd_q_id'],
							 lang_code=section['lang_code']) for section in section_data]
	return section_data


def extract_domain_data(domain_data_file, lang_code):
	domain_data = []
	with open(domain_data_file) as f:
		lines = f.readlines()
		if lines:
			# file is not empty
			for line in lines:

				data = json.loads(line)
				
				score_info = data['scores']['wikidata']
				# extract key values of the twitter entry in score
				score_key_value = ['', '']
				en_title = ''
				en_title = ''
				twitter_handle = ''
				twitter_followers = ''
				wd_q_id = ''
				if score_info is not None:
					score_key_value = get_object_first_key_value(score_info[0]['twitter'])
					twitter_handle = score_key_value[0]
					twitter_followers = score_key_value[1]
					en_title = score_info[0]['en_title']
					wd_q_id = score_info[0]['qid']

				# Extract relevant info in data object
				domain_name = data['domain']
				wikipedia_score = data['scores']['wikipedia']
				wikipedia_domain = data['scores']['wikipediadomain']
				search_result_score = data['scores']['search_result_score']

				# Extract relevent info in data['score']['wikidata']['twitter']

				domain = Domain(domain_name=domain_name, wikipedia_score=wikipedia_score,
								 wikipedia_domain=wikipedia_domain,
								 search_result_score=search_result_score,
								 en_title=en_title,
								 lang_code=lang_code,
								 wd_q_id=wd_q_id,
								 twitter_handle=twitter_handle,
								 twitter_followers=twitter_followers)
				domain_data.append(domain)
	return domain_data


def write_data(article_data):

	if commit_changes_to_db(data=article_data):
		print('Something is Wrong:(')
	else:
		print('Data Added!', file=sys.stderr)

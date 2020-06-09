'''Add article data to the database
'''

import sys
import json

from datetime import datetime

from scribe.models import Article, Reference
from scribe.main.utils import commit_changes_to_db


def extract_article_data(file, lang_code):
	'''Extracts article data from the file and sends object of the data to db
	'''
	article_data = []

	with open(file) as f:
		lines = f.readlines()

	if lines:
		# file is not empty

		# we remove the heading
		lines.pop(0)

		# remove new lines characteers
		lines = [line.replace('\n','') for line in lines]

		# we remove the domain name
		lines = [line.replace('http://www.wikidata.org/entity/','') for line in lines]

		for line in lines:
			article = {}
			name, wd_q_id = line.split(',')[1], line.split(',')[0],
			# lang_code = file[:2] # first tow characters of a file name for the code

			article['name'] = name
			article['wd_q_id'] = wd_q_id
			article['lang_code'] = lang_code
			article_data.append(article)
	else:
		pass # report an error here

	# create article objects at once
	article_data = [ Article(name=article['name'], wd_q_id=article['wd_q_id'], lang_code=article['lang_code']) \
					for article in article_data]
	return article_data

def extract_reference_data(file):
	'''Extracts reference data from the file and sends object of the data to db

	STEPS TO ADD ARTICLE/REFERENCE DATA ON COMMAND LINE

	from scribe import db
	from scribe.db.add_data import extract_article_data, extract_reference_data, write_data

	ca_article_data = extract_article_data('scribe/db/ca_article_data.tsv', 'ca')
	ar_article_data = extract_article_data('scribe/db/ar_article_data.tsv', 'ar')

	write_data(ca_article_data)
	write_data(ar_article_data)

	ca_ref_data = extract_reference_data('scribe/db/ca_ref.txt')
	ar_ref_data = extract_reference_data('scribe/db/ar_ref.txt')


	write_data(ca_ref_data)
	write_data(ar_ref_data)
	'''

	reference_data = []

	with open(file) as f:
		lines = f.readlines()

	if lines:
		# file is not empty
		file_data = json.loads(lines[0])
		for data in file_data:
			article_id = Article.query.filter_by(wd_q_id=data['wd_q_id']).first().id
			reference = Reference(article_id=article_id,
								  publisher_name=data['publisher_name'], 
								  wd_q_id=data['wd_q_id'],
								  publication_title=data['publication_title'],
								  summary=data['summary'],
								  url=data['url'],
								  quality=data['quality'],
								  publication_date=datetime.strptime(data['publication_date'].split('T')[0], '%Y-%m-%d'),
								  content_selection_method=data['content_selection_method'])
			reference_data.append(reference)
	else:
		pass # report an error here

	return reference_data

def write_data(article_data):

	if commit_changes_to_db(data=article_data):
		print('Something is Wrong:(')
	else:
		print('Data Added!', file=sys.stderr)



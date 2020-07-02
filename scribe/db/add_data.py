'''Add article data to the database
'''

import os
import sys
import json

from datetime import datetime

from scribe.models import Article, Reference, Section, Domain
from scribe.main.utils import commit_changes_to_db, get_base_url, get_object_first_key_value


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

		# replace tabs with spaces
		lines = [line.replace('\t', ' ') for line in lines]

		# replace four spaces with spaces
		lines = [line.replace('    ', ' ') for line in lines]
		for line in lines:
			article = {}
			print(line.split(' ', 2))
			name = line.split(' ', 2)[2] # limit split to first 2 spaces
			wd_q_id = line.split(' ', 2)[0]
			domain = line.split(' ', 2)[1]
			# lang_code = file[:2] # first tow characters of a file name for the code

			article['name'] = name
			article['wd_q_id'] = wd_q_id
			article['lang_code'] = lang_code
			article['domain'] = domain
			article_data.append(article)
	else:
		pass # report an error here

	# create article objects at once
	article_data = [ Article(name=article['name'], wd_q_id=article['wd_q_id'], lang_code=article['lang_code'],
							 domain=article['domain']) for article in article_data]
	return article_data

def extract_reference_data(file, lang_code):
	'''Extracts reference data from the file and sends object of the data to db

	'''

	reference_data = []

	with open(file) as f:
		lines = f.readlines()

		if lines:
			# file is not empty
			file_data = json.loads(lines[0])
			for data in file_data:
				reference = Reference(publisher_name=data['publisher_name'], 
									  wd_q_id=data['wd_q_id'],
									  publication_title=data['publication_title'].encode('unicode_escape'),
									  summary=data['summary'].encode('unicode_escape'),
									  url=data['url'],
									  quality=data['quality'],
									  lang_code = lang_code,
									  publication_date=datetime.strptime(data['publication_date'].split('T')[0], '%Y-%m-%d'),
									  content_selection_method=data['content_selection_method'])
				reference_data.append(reference)
		else:
			pass # report an error here

	return reference_data


def check_article_type(language):
	articles = Article.query.filter_by(lang_code=language[:2]).all()

	article_options = []
	root = 'scribe/db/data/' + language

	for article in articles:
		article_option = {}
		directory = os.listdir(root)
		article_types =[]
		for fname in directory:
			if os.path.isfile(root + os.sep + fname):
				f = open(root + os.sep + fname, 'r')
				if article.wd_q_id in f.read():
					article_types.append( root + '/' + fname.split('.')[0] +'-sections.tsv' )
				# add article type to type array
				f.close()
		if len(article_types) > 0:
			article_option['id'] = article.id
			article_option['lang_code'] = article.lang_code
			article_option['article_types'] = article_types
			article_options.append(article_option)
	return article_options


def create_article_sections(article_options):
	article_sections = []

	for article_option in article_options:
		section_files = article_option['article_types']
		for file_name in section_files:
			f = open(file_name, 'r')
			lines = f.readlines()
			if lines:
				lines.pop(0)
				lines = [line.replace('\n','') for line in lines]
				for line in lines:
					article = Article.query.filter_by(id=article_option['id']).first()
					order_number, label = int(line.split('\t')[0]), line.split('\t')[2]
					quality = int(line.split('\t')[1])
					# lang_code = file[:2] # first tow characters of a file name for the code
					section = Section(label=label, article_id=article.id, lang_code=article_option['lang_code'],
									  order_number=order_number, quality=quality)
					article_sections.append(section)
			f.close()
	return article_sections


def extract_domain_data(domain_data_file):
	domain_data = []
	all_references = Reference.query.all()
	with open(domain_data_file) as f:
		lines = f.readlines()
		if lines:
			# file is not empty
			for line in lines:

				data = json.loads(line)
				
				for reference in all_references:
					
					ref_base_url = get_base_url(reference.url)
					score_info = data['scores']['wikidata']

					if data['domain'] == ref_base_url and score_info is not None:
						# extract key values of the twitter entry in score
						score_key_value = get_object_first_key_value(score_info[0]['twitter'])

						# Extract relevant info in data object
						domain_name = data['domain']
						wikipedia_score = data['scores']['wikipedia']
						wikipedia_domain = data['scores']['wikipediadomain']
						search_result_score = data['scores']['search_result_score']

						# Extract relevant info in data['score']
						en_title = score_info[0]['en_title']
						wd_q_id = score_info[0]['qid']

						# Extract relevent info in data['score']['wikidata']['twitter']
						twitter_handle = score_key_value[0]
						twitter_followers = score_key_value[1]

						domain = Domain(domain_name=domain_name, wikipedia_score=wikipedia_score,
										wikipedia_domain=wikipedia_domain,
										search_result_score=search_result_score,
										en_title=en_title,
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

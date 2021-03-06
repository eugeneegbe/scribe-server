
import sys

import json
import unicodedata

from urllib.parse import urlsplit

from scribe import db

from scribe.models import Section, Article, Reference, Statistics, Domain


def commit_changes_to_db(data=None):
    """
    Test for the success of a database commit operation.

    """
    if data is not None:
        for d in data:
            db.session.add(d)
    try:
        db.session.commit()
    except Exception as e:
        # TODO: We could add a try catch here for the error
        print('-------------->>>>>', file=sys.stderr)
        print(str(e), file=sys.stderr)
        db.session.rollback()
        # for resetting non-commited .add()
        db.session.flush()
        return True
    return False


def convert_date(date_str):
    print(date_str, file=sys.stderr)
    date = date_str.split(' ');
    return date[1] + ' ' + date[0] + ', ' + date[2]


def decode_text(text):
    try:
        text = text.decode('UTF-8')
    except (UnicodeDecodeError, AttributeError):
        pass
    return "".join(char for char in
                   unicodedata.normalize('NFKD', text)
                   if unicodedata.category(char) != 'Mn')


def get_reference_resource_data(article_name):
    """
    Get proposed references about an article's section

    Keyword arguments:
    article_name -- name of the sectioin whose references are to be obtained
    """
    resource_object = {}
    resource_object['resources'] = []
    article = Article.query.filter_by(name=article_name).first()
    # article_id = Article.query.filter_by(name=article_name).first().id
    # sections = Section.query.filter_by(label=section_name).all()
    # active_section = None

    # # Collect sections of particular article
    # for section in sections:
    #     if section.article_id == str(article_id):
    #         active_section = section

    # # We get that sections references
    # reference_data = Reference.query.filter_by(section_id=active_section.id).all()
    # # Add references of that article which do not have a section
    # other_reference_data = Reference.query.filter_by(article_id=article_id).all()

    # for other_reference in other_reference_data:
    #     # check if reference has no specified section
    #     if other_reference.section_id == 0:
    #             data_object = {}
    #             data_object['section_label'] = 'Proposed Reference'
    #             data_object['content'] = other_reference.summary
    #             data_object['url'] = other_reference.url
    #             data_object['domain'] = 'Proposed'
    #             resource_object['resources'].append(data_object)


    # for data in reference_data:
    #     data_object = {}
    #     data_object['section_label'] = section_name
    #     data_object['content'] = data.summary
    #     data_object['url'] = data.url
    #     data_object['domain'] = Article.query.filter_by(id=section.article_id).first().domain
    #     resource_object['resources'].append(data_object)
    # resource_object['article_name'] = article_name

    # get the article language code to be used to fetch references in same language
    article_lang_code = article.lang_code


    # collect all references in that language code
    all_reference_data = Reference.query.filter_by(wd_q_id=article.wd_q_id).all()
    count = 0
    for data in all_reference_data:
        if data.lang_code == article.lang_code:
            data_object = {}
            data_object['content'] = data.summary
            data_object['publication_title'] = data.publication_title
            data_object['url'] = data.url
            data_object['domain'] = Article.query.filter_by(name=article_name).first().domain
            resource_object['resources'].append(data_object)
    resource_object['article_name'] = decode_text(article_name)
    return resource_object


def get_reference_data(url):
    reference_data = {}
    reference = Reference.query.filter_by(url=url).first()
    if reference is not None:
        reference_data['publisher_name'] = reference.publisher_name
        reference_data['publication_title'] = decode_text(reference.publication_title)
        reference_data['publication_date'] = convert_date(reference.publication_date.strftime('%d %B %Y'))
        reference_data['retrieved_date'] = convert_date(reference.retrieved_date.strftime('%d %B %Y'))
    return reference_data


def get_section_data(article_name):
    """
    Get proposed sections about an article

    Keyword arguments:
    article_name -- name of the article whose sections is to be obtained
    """
    section_count = 0
    all_sections_data = {}
    parse = {}
    sections = []
    article = Article.query.filter_by(name=article_name.lower()).first()
    sections_data = Section.query.filter_by(wd_q_id=article.wd_q_id).all()
    for section_data in sections_data:
        if section_data.lang_code == article.lang_code:
            section = {}
            section['line'] = decode_text(section_data.label)
            section['number'] = str(section_count + 1)
            sections.append(section)
            section_count += 1
    parse['sections'] = sections
    all_sections_data['parse'] = parse
    return all_sections_data


def add_stats_data(data):
    """
    Add stats data about reference to database
    
    """

    article_id = Article.query.filter_by(name=data['article']).first().id
    references_used = data['ref']
    sections_used = data['selectedSection']
    statistic = Statistics(article_id=article_id, references_used=references_used,
                           sections_used=sections_used)
    db.session.add(statistic)
    if commit_changes_to_db():
        print(data['article'], file=sys.stderr )
        return ('Failure')
    else:
        return ('Success')
    return ('Failure')


def get_stats_data(url):
    """Get reference stats data

    """
    stats_data = {}
    sections = []
    statistic_data = Statistics.query.filter_by(references_used=url).all()
    
    for stat in statistic_data:
        sections.append(stat.sections_used)
    
    stats_data['sections'] = list(set(sections))
    stats_data['frequency'] = len(statistic_data)

    return  json.dumps(stats_data)


def get_object_first_key_value(data_object):
    key_value = []
    if len(data_object) > 0:
        iterator = iter(data_object)
        key = next(iterator)
        value = data_object[key]
        key_value.append(key)

        if len(value) > 0:
            key_value.append(value)
        else:
            key_value.append('')
    else:
        key_value.append('')
        key_value.append('')

    return key_value


def get_base_url(url):
    try:
        netloc = urlsplit(url).netloc
        if netloc.startswith("www."):
            netloc = netloc.replace("www.","")
        return netloc if len(netloc) > 0 else None
    except:
        return None


def get_domain_data(url):
    domain_info = {}
    base_url = get_base_url(url)
    domain = Domain.query.filter_by(domain_name=base_url).first()

    domain_info['wikipedia_score'] = domain.wikipedia_score
    domain_info['wikipedia_domain'] = domain.wikipedia_domain
    domain_info['search_result_score'] = domain.search_result_score
    domain_info['twitter_handle'] = domain.twitter_handle
    domain_info['twitter_followers'] = domain.twitter_followers

    return domain_info

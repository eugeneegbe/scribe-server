
import sys

from scribe.models import Section, Article, Reference


def get_reference_resource_data(section_name):
    """
    Get proposed references about an article's section

    Keyword arguments:
    article_name -- name of the sectioin whose references are to be obtained
    """
    resource_object = {}
    resource_object['resources'] = []
    section = Section.query.filter_by(label=section_name).first()
    print(section, file=sys.stderr)

    reference_data = Reference.query.filter_by(section_id=section.id).all()
    for data in reference_data:
        data_object = {}
        data_object['section_label'] = section_name
        data_object['content'] = data.summary
        data_object['url'] = data.url
        data_object['domain'] = Article.query.filter_by(id=section.article_id).first().domain
        resource_object['resources'].append(data_object)
    # resource_object['article_name'] = article_name
    return resource_object

def get_reference_data(url):
    reference_data = {}
    reference = Reference.query.filter_by(url=url).first()
    print(url, file=sys.stderr)
    reference_data['publisher_name'] = reference.publisher_name
    reference_data['publication_title'] = reference.publication_title
    reference_data['publication_date'] = reference.publication_date
    reference_data['retrieved_date'] = reference.retrieved_date
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
    sections_data = Section.query.filter_by(article_id=article.id).all()
    for section_data in sections_data:
        section = {}
        section['line'] = section_data.label
        section['number'] = str(section_count + 1)
        sections.append(section)
        section_count += 1
    parse['sections'] = sections
    all_sections_data['parse'] = parse
    return all_sections_data
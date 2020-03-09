
import sys

from scribe.models import Section, Article, Reference


def get_reference_resource_data(article_name, section_name):
    """
    Get proposed references about an article's section

    Keyword arguments:
    article_name -- name of the sectioin whose references are to be obtained
    """
    resource_object = {}
    resource_object['resources'] = []
    article_id = Article.query.filter_by(name=article_name).first().id
    sections = Section.query.filter_by(label=section_name).all()
    active_section = None

    # Collect sections of particular article
    for section in sections:
        if section.article_id == str(article_id):
            active_section = section

    # We get that sections references
    reference_data = Reference.query.filter_by(section_id=active_section.id).all()
    # Add references of that article which do not have a section
    other_reference_data = Reference.query.filter_by(article_id=article_id).all()

    for other_reference in other_reference_data:
        # check if reference has no specified section
        if other_reference.section_id == 0:
                data_object = {}
                data_object['publication_title'] = other_reference.publication_title
                data_object['section_label'] = 'Proposed Reference'
                data_object['content'] = other_reference.summary
                data_object['url'] = other_reference.url
                data_object['domain'] = 'Proposed'
                resource_object['resources'].append(data_object)


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
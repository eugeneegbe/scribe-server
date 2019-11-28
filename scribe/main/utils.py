
import sys

from scribe.models import Edit, Section


def get_reference_resource_data(section_name):
    """
    Get proposed content about an article

    Keyword arguments:
    article_name -- name of the article whose data is to be obtained
    """
    resource_object = {}
    resource_object['resources'] = []
    edit_data = Edit.query.filter_by(section_label=section_name).all()
    for data in edit_data:
        data_object = {}
        data_object['section_label'] = data.section_label
        data_object['content'] = data.content
        data_object['url'] = data.url
        data_object['domain'] = data.domain
        resource_object['resources'].append(data_object)
    # resource_object['article_name'] = article_name
    return resource_object


def get_section_data(article_name):
    section_count = 0
    all_sections_data = {}
    parse = {}
    sections = []
    sections_data = Section.query.filter_by(article_name=article_name.lower()   ).all()
    print(sections_data, file=sys.stderr)
    for section_data in sections_data:
        section = {}
        section['line'] = section_data.label
        section['number'] = str(section_count + 1)
        sections.append(section)
        section_count += 1
    parse['sections'] = sections
    all_sections_data['parse'] = parse
    return all_sections_data
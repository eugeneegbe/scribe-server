
import sys

from scribe.models import Edit


def get_reference_resource_data(article_name):
    """
    Get proposed content about an article

    Keyword arguments:
    article_name -- name of the article whose data is to be obtained
    """
    resource_object = {}
    resource_object['resources'] = []
    edit_data = Edit.query.filter_by(article_name=article_name).all()
    for data in edit_data:
        data_object = {}
        data_object['section_label'] = data.section_label
        data_object['content'] = data.content
        data_object['url'] = data.url
        data_object['domain'] = data.domain
        resource_object['resources'].append(data_object)
    resource_object['article_name'] = article_name
    return resource_object

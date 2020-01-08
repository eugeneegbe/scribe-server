import os
import sys

from flask import Blueprint, request
from scribe.main.utils import get_reference_resource_data, get_section_data, get_reference_data


main = Blueprint('main', __name__)


@main.route('/api/v1/references')
def getReferencesData():
    section_name = request.args.get('section')
    resource_data = get_reference_resource_data(section_name)
    if resource_data:
        return resource_data
    else:
        return '<h2> Unable to get data at the moment</h2>'

@main.route('/api/v1/references/resources')
def getReferenceResourceData():
    url = request.args.get('link')
    print(request.args, file=sys.stderr)
    reference_data = get_reference_data(url)
    if reference_data:
        return reference_data
    else:
        return '<h2> Unable to get data at the moment</h2>'


@main.route('/api/v1/sections')
def getSectionData():
    article_name = request.args.get('article')
    resource_data = get_section_data(article_name)
    if resource_data:
        return resource_data
    else:
        return '<h2> Welcome to Scribe service</h2>'


@main.route('/')
def home():
    return '<h2> Welcome to Scribe service</h2>'

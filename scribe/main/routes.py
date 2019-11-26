import os
import sys

from flask import Blueprint, request
from scribe.main.utils import get_reference_resource_data, get_section_data


main = Blueprint('main', __name__)


@main.route('/api/v1')
def getReferencesData():
    article_name = request.args.get('article')
    resource_data = get_reference_resource_data(article_name)
    if resource_data:
        return resource_data
    else:
        return '<h2> Welcome to Scribe service</h2>'


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

import os
import sys
import json

from flask import Blueprint, request
from scribe.main.utils import get_reference_resource_data, get_section_data, get_reference_data, add_stats_data, get_stats_data


main = Blueprint('main', __name__)


@main.route('/api/v1/references')
def getReferencesData():
    section_name = request.args.get('section')
    article_name = request.args.get('article')
    resource_data = get_reference_resource_data(article_name, section_name)
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



@main.route('/api/v1/stats', methods=['POST', 'GET'])
def AddReferenceStatsData():
    stats_data = json.loads(request.data.decode('utf8'))
    print(stats_data, file=sys.stderr)
    if stats_data:
        add_stats_data(stats_data)
    else:
        return '<h2> Unable to get data at the moment</h2>'


@main.route('/api/v1/stats/references', methods=['POST', 'GET'])
def getReferenceStatsData():
    url = request.args.get('url')
    if url is None:
        return '<h2> Unable to get data at the moment</h2>'
    else:
        return get_stats_data(url)


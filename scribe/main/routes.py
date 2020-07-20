import os
import sys
import json

from flask import Blueprint, request
from scribe.main.utils import (get_reference_resource_data, get_section_data, get_reference_data,
                               add_stats_data, get_stats_data, get_domain_data)


main = Blueprint('main', __name__)


@main.route('/api/v1/references')
def getReferencesData():
    '''
    Get references for a particular article 
    TODO: Add posibility to get references by section
    '''

    # section_name = request.args.get('section')
    article_name = request.args.get('article')
    resource_data = get_reference_resource_data(article_name)
    if resource_data:
        return resource_data
    else:
        return '<h2> Unable to get data at the moment</h2>'


@main.route('/api/v1/references/resources')
def getReferenceResourceData():
    '''
    Get data about reference url which will be used to construct template for VE
    '''
    url = request.args.get('link')
    reference_data = get_reference_data(url)
    if reference_data:
        return reference_data
    else:
        return '<h2> This url has no reference in our records</h2>'


@main.route('/api/v1/domain')
def getDomainData():
    '''
    Get data about a particular reference domain
    '''
    url = request.args.get('link')
    domain_data = get_domain_data(url)
    if domain_data:
        return domain_data
    else:
        return '<h2> This domain may not have data in our records</h2>'


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
    # print(stats_data, file=sys.stderr)
    if stats_data:
        add_stats_data(stats_data)
    else:
        return '<h2> Unable to get data at the moment</h2>'
    return ('Success')


@main.route('/api/v1/stats/references', methods=['POST', 'GET'])
def getReferenceStatsData():
    url = request.args.get('url')
    if url is None:
        return '<h2> Unable to get data at the moment</h2>'
    else:
        return get_stats_data(url)


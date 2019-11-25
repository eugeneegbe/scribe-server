import os
import sys

from flask import Blueprint, render_template, session, redirect, url_for, request
from scribe.main.utils import get_resource_data

main = Blueprint('main', __name__)

@main.route('/api/v1')
def home():
	article_name = request.args.get('article')
	resource_data = get_resource_data(article_name )
	if resource_data:
		return resource_data
	else:
		return '<h2> Welcome to Scribe service</h2>'



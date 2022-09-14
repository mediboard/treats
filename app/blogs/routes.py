from app.blogs import bp
from app.errors import create_notfound_error
from flask_cors import cross_origin
import app.conditions.controller as controller
from flask import request
from app.utils import calculate_results_summary
import feedparser
import json


@bp.route('/medium/<string:username>')
@cross_origin(supports_credentials=True)
def main(username):
	return feedparser.parse("https://medium.com/feed/" + username).entries

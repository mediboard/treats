from app.feedback import bp
from flask_cors import cross_origin
from flask import request
import feedparser
import requests
import os


POST_MESSAGE_URI = 'https://slack.com/api/chat.postMessage'
SLACK_TOKEN = os.environ.get('SLACK_TOKEN') or 'xoxb-3696292071424-4127307855559-MyLmh7vMxTsKDWdRrmxfBS1A'
FEEDBACK_CHANNEL = os.environ.get('FEEDBACK_CHANNEL') or 'C03L560LN3B';

@bp.route('/slack', methods = ['POST'])
@cross_origin(supports_credentials=True)
def slack():
	headers = {'Authorization': 'Bearer ' + SLACK_TOKEN}

	response = requests.post(POST_MESSAGE_URI, data={'text': request.form['text'], 'channel': FEEDBACK_CHANNEL}, headers=headers)
	print(response);

	return {"status": "good"}
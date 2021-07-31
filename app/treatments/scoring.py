from app.treatments.models import Analytic

# Thinking of an API where we can feed in the analytics and it produces a score, we can
# worry about aggregating the score for each part in the controllers
def get_efficacy_score(analytics):
	# Just a p-val average for now - this is an area of great improvement
	for analytic in analytics:

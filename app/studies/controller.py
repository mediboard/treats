from app import db
from app.models import Study, Criteria, Measure, Analytics, Baseline,
	Group
from sqlalchemy.orm import joinedload


def get_study(study_name):
	studies = db.session.query(Study)\
		.filter_by(name)
		.joinedload(Study.criteria)\
		.joinedload(Study.measures)\
		.joinedload(Study.analytics)\
		.joinedload(Study.baselines)\
		.joinedload(Study.groups).get(1)

	return studies

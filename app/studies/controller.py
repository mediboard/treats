from app import db
from app.models import Study, Criteria, Measure, Analytics, Baseline,\
	Group, StudyTreatment, StudyCondition
from sqlalchemy.orm import joinedload, raiseload


# TODO: this is a 30 second query...
def get_study(study_id):
	studies = db.session.query(Study)\
		.filter_by(id = study_id)\
		.options(
			joinedload(Study.criteria),
			joinedload(Study.measures).joinedload(Measure.outcomes),
			joinedload(Study.analytics),
			joinedload(Study.baselines),
			joinedload(Study.groups),
			joinedload(Study.conditions).joinedload(StudyCondition.conditions),
			joinedload(Study.treatments).joinedload(StudyTreatment.treatments),
			raiseload('*')
		)

	return studies.all()

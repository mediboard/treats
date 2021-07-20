from app.treatments.models import Baseline, Treatment, Administration, Study, Group
from app import db
from sqlalchemy.orm import aliased


def get_demographics(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	admin_query = db.session.query(Administration).join(treatment_query, Administration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(Group).join(admin_query, Group.id == admin_query.c.group).subquery()
	study_query = db.session.query(Study).join(group_query, Study.id == group_query.c.study).subquery()
	baselines = db.session.query(Baseline).join(study_query, Baseline.study == study_query.c.id).all()

	return [baseline for baseline in baselines if baseline.is_demographic()]


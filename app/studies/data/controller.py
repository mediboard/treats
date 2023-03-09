from app import db
from app.models import Study, Treatment, StudyTreatment, Condition, StudyCondition, Baseline
from sqlalchemy import and_, func, or_


def query_attr(attr, study_subquery, limit):
  attr_counts = db.session.query(getattr(Study, attr), func.count(Study.id))\
    .join(study_subquery, study_subquery.c.id == Study.id)\
    .group_by(getattr(Study, attr))\
    .order_by(func.count(Study.id).desc())\
    .limit(limit)\
    .all()

  return attr_counts


def agg_treatments(study_subquery, limit):
  treat_counts_query = db.session.query(Treatment.name, func.count(StudyTreatment.study))\
    .join(StudyTreatment, StudyTreatment.treatment == Treatment.id)\
    .join(study_subquery, study_subquery.c.id == StudyTreatment.study)\
    .group_by(Treatment.name)\
    .order_by(func.count(StudyTreatment.study).desc())\
    .limit(limit)\
    .all()

  return treat_counts_query


def agg_conditions(study_subquery, limit):
  condition_counts = db.session.query(Condition.name, func.count(StudyCondition.study))\
    .join(StudyCondition, StudyCondition.condition == Condition.id)\
    .join(study_subquery, study_subquery.c.id == StudyCondition.study)\
    .group_by(Condition.name)\
    .order_by(func.count(StudyCondition.study).desc())\
    .limit(limit)\
    .all()
  
  return condition_counts 


def agg_baselines(study_subquery, limit):
  baseline_counts = db.session.query(Baseline.sub_type, func.sum(Baseline.value))\
    .join(study_subquery, study_subquery.c.id == Baseline.study)\
    .group_by(Baseline.sub_type)\
    .all()

  return baseline_counts 


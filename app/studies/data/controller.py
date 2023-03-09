from app import db
from app.models import Study
from sqlalchemy import and_, func, or_


def query_attr(attr, study_subquery, limit):
  attr_counts = db.session.query(getattr(Study, attr), func.count(Study.id))\
    .join(study_subquery, study_subquery.c.id == Study.id)\
    .group_by(getattr(Study, attr))\
    .order_by(func.count(Study.id).desc())\
    .limit(limit)\
    .all()

  return attr_counts


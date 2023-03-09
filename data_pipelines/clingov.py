import sys

# The main workflow to run all workflows
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from workflows.studies_workflow import studies_workflow
from workflows.treatments_workflow import run_treatments_workflow 
from workflows.groups_workflow import groups_workflow 
from workflows.measures_workflow import measures_workflow 
from workflows.effects_workflow import effects_workflow
from workflows.conditions_workflow import conditions_workflow 
from workflows.baselines_workflow import baselines_workflow 
from workflows.study_treatments_workflow import study_treatments_workflow
from workflows.outcomes_workflow import outcomes_workflow 
from workflows.upload_treatments import upload_treatments_workflow


engine = create_engine("postgresql://meditreats:meditreats@localhost:5432/meditreats")
#session_maker = sessionmaker(bind=engine)

# def prep_new_schema():
#   session = session_maker()
#   with session.begin():
#     session.execute("SET search_path TO temp_schema")

#   return session.connection()


# We're going to run the migrations manually
# def run_migrations():
#   sys.path.append('..')
#   from app import create_app

#   app = create_app('dev.cfg')

#   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://meditreats:meditreats@localhost:5432/meditreats?search_path=temp_schema'

#   with app.app_context():
#       from flask_migrate import upgrade
#       upgrade()


def run_clingov_pipelines():
  connection = engine.connect()
  # studies_workflow(connection, False)

  # groups_workflow(connection)
  # effects_workflow(connection, True)
  # conditions_workflow(connection)
  # baselines_workflow(connection)

  # measures_workflow(connection)
  # outcomes_workflow(connection)

  # This takes a while
  # upload_treatments_workflow(connection)
  study_treatments_workflow(connection)


if __name__ == '__main__':
  run_clingov_pipelines()

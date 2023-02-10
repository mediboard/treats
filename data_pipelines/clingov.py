import sys

# The main workflow to run all workflows
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from workflows.studies_workflow import studies_workflow


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
  studies_workflow(connection, False)


if __name__ == '__main__':
  run_clingov_pipelines()

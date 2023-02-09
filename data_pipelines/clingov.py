# The main workflow to run all workflows
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://user:password@host:port/database")
session_maker = sessionmaker(bind=engine)

def prep_new_schema():
  session = session_maker()
  with session.begin():
    session.execute("CREATE SCHEMA temp_schema")
    session.execute("SET search_path TO temp_schema")
    transaction.commit()

  return session.connection();

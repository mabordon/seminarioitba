from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from itbatools import get_db_property_hook

engine=create_engine(get_db_property_hook().database_uri)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
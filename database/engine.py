from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_URL = "mysql+pymysql://cbpadmin:cbpadmin1234@cbp-db.cluster-crxjgn1izzc0.ap-northeast-1.rds.amazonaws.com:3306/cbp_db"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

Base = declarative_base()

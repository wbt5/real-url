from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class CCDanMu(Base):
    __tablename__ = 'cc_record_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(8092))
    name = Column(String(255))
    content_type = Column(String(255))
    created_at = Column(Integer)
    updated_at = Column(Integer)
    url = Column(String(256))
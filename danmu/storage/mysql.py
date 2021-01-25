from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Persist(object):
    def __init__(self):
        self.engine = create_engine('')
        self.session_maker = sessionmaker(bind=self.engine)
    
    def save(self, row):
        session = self.session_maker()
        session.add(row)
        session.commit()
        session.close()
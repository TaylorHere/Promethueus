from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
engine = create_engine('sqlite:///word_dict.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


class words_space(Base):
    __tablename__ = 'words_space'
    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=True, unique=True)
    count = Column(Integer, nullable=True)

    def __init__(self, word=None):
        self.key = word

    def __str__(self):
        return self.key

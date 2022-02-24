from sqlalchemy import Column, String, Table, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from base import Base
# from professor import lecture_professor

# lecture_professor = Table('lecture_professor', Base.metadata,
#                           Column('lecture_id', ForeignKey('lecture.id'), primary_key=True),
#                           Column('professor_id', ForeignKey('professor.id'), primary_key=True))

class Lecture(Base):
    __tablename__ = 'lecture'

    id = Column(String, primary_key=True)
    url = Column(String)
    name = Column(String)
    subject_type = Column(String)
    semester = Column(String)
    sws = Column(String)
    longtext = Column(String)
    shorttext = Column(String)
    language = Column(String)
    hyperlink = Column(String)
    description = Column(String)
    professor_ids = Column(ARRAY(String))
    children = relationship("Timetable")
    # professors = relationship('Professor', secondary=lecture_professor, back_populates='lectures')

    def __init__(self, id, url, name, subject_type, semester, sws, longtext, shorttext, language, hyperlink, description, professor_ids):
        self.id = id
        self.url = url
        self.name = name
        self.subject_type = subject_type
        self.semester = semester
        self.sws = sws
        self.longtext = longtext
        self.shorttext = shorttext
        self.language = language
        self.hyperlink = hyperlink
        self.description = description
        self.professor_ids = professor_ids

class Professor(Base):
    __tablename__ = 'professor'

    id = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)
    # lectures = relationship('Lecture', secondary=lecture_professor, back_populates='professors')

    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Lecture_Professor(Base):
    __tablename__ = 'lecture_professor'

    lecture_id = Column(String, ForeignKey('lecture.id'), primary_key=True)
    professor_id = Column(String, ForeignKey('professor.id'), primary_key=True)

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
    children = relationship("Timetable")
    professors = relationship('Professor', secondary='lecture_professor')
    root_id = relationship('StudyProgram', secondary='lecture_studyprogram')

    def __init__(self, id, url, name, subject_type, semester, sws, longtext, shorttext, language, hyperlink, description):
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

class Professor(Base):
    __tablename__ = 'professor'

    id = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)

    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url

class Lecture_Studyprogram(Base):
    __tablename__ = 'lecture_studyprogram'

    lecture_id = Column(String, ForeignKey('lecture.id'), primary_key=True)
    studyprogram_id = Column(String, ForeignKey('study_program.id'), primary_key=True)

class StudyProgram(Base):
    __tablename__ = 'study_program'
    id = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)

    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url
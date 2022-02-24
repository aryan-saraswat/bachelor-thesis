import json
import io
from entities.lecture import Lecture, Professor
# from entities.lecture import lecture_professor
from entities.timetable import Timetable
# from entities.professor import Professor, lecture_professor
from base import Base, Session, engine

DATA_DIRECTORY = 'scrapers/merged_data.json'
Base.metadata.create_all(engine)

session = Session()

all_lectures = session.query(Lecture).all()
for lecture in all_lectures:
    session.delete(lecture)
session.commit()

all_timetables = session.query(Timetable).all()
for timetable in all_timetables:
    session.delete(timetable)
session.commit()

all_professors = session.query(Professor).all()
for professor in all_professors:
    session.delete(professor)
session.commit()

# all_lecture_professor = session.query(lecture_professor)
# for entry in all_lecture_professor:
#     session.delete(entry)
# session.commit()


with io.open(DATA_DIRECTORY, 'r') as data_file:
    data_json = json.load(data_file)
    print(len(data_json))
    already_entered_professors = []
    for lecture in data_json:
        professor_ids = [professor['id'] for professor in lecture['persons']]
        temp_lecture = Lecture(lecture['id'], lecture['url'], lecture['name'], lecture['subject_type'], lecture['semester'], lecture['sws'], lecture['longtext'], lecture['shorttext'], lecture['language'], lecture['hyperlink'], lecture['description'], professor_ids)
        session.add(temp_lecture)

        timetable_entries = lecture['timetable']
        for entry in timetable_entries:
            if entry['id'] != "":
                temp_entry = Timetable(entry['id'], entry['day'], entry['time']['from'], entry['time']['to'], entry['rhythm'], 'duration', entry['room'], entry['status'], entry['comment'], entry['elearn'], entry['einzeltermine_link'], lecture['id'], entry['dates'])
                session.add(temp_entry)

        professors = lecture['persons']
        for professor in professors:
            if professor['id'] not in already_entered_professors:
                temp_professor = Professor(professor['id'], professor['name'], professor['url'])
                session.add(temp_professor)
                already_entered_professors.append(professor['id'])

    session.commit() # saving lectures
    data_file.close()

session.commit()
session.close()
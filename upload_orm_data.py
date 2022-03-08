import json
import io
from entities.lecture import Lecture, Professor, StudyProgram
from entities.timetable import Timetable
# from entities.studyprogram import StudyProgram
from base import Base, Session, engine

DATA_DIRECTORY = 'scrapers/merged_data.json'
STUDYPROGRAMS_DIRECTORY = 'scrapers/study_programs.json'
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

all_studyprograms = session.query(StudyProgram).all()
for study_program in all_studyprograms:
    session.delete(study_program)
session.commit()

professors_dict = {}
studyprograms_dict = {}

with io.open(STUDYPROGRAMS_DIRECTORY, 'r') as studyprograms_data:
    studyprograms_json = json.load(studyprograms_data)
    for studyprogram in studyprograms_json:
        if studyprogram['id'] not in studyprograms_dict.keys():
            studyprograms_dict[studyprogram['id']] = StudyProgram(studyprogram['id'], studyprogram['name'], studyprogram['url'])
    studyprograms_data.close()

with io.open(DATA_DIRECTORY, 'r') as data_file:
    data_json = json.load(data_file)
    print(len(data_json))
    for lecture in data_json:
        professors = lecture['persons']
        for professor in professors:
            if professor['id'] not in professors_dict.keys():
                professors_dict[professor['id']] = Professor(professor['id'], professor['name'], professor['url'])

    count = 0
    for lecture in data_json:
        temp_lecture = Lecture(lecture['id'], lecture['url'], lecture['name'], lecture['subject_type'], lecture['semester'], lecture['sws'], lecture['longtext'], lecture['shorttext'], lecture['language'], lecture['hyperlink'], lecture['description'])

        professors = lecture['persons']
        for professor in professors:
            temp_lecture.professors.append(professors_dict[professor['id']])

        root_id = lecture['root_id']
        for root in root_id:
            temp_lecture.root_id.append(studyprograms_dict[root])

        timetable_entries = lecture['timetable']
        for timetable_entry in timetable_entries:
            if timetable_entry['id'] == "":
                timetable_entry['id'] = str(count)
                count += 1
            if 'dates' not in timetable_entry.keys():
                temp_entry = Timetable(timetable_entry['id'], timetable_entry['day'], timetable_entry['time']['from'],
                                       timetable_entry['time']['to'], timetable_entry['rhythm'], 'duration',
                                       timetable_entry['room'], timetable_entry['status'], timetable_entry['comment'],
                                       timetable_entry['elearn'], timetable_entry['einzeltermine_link'], lecture['id'], [])
            else:
                temp_entry = Timetable(timetable_entry['id'], timetable_entry['day'], timetable_entry['time']['from'],
                                       timetable_entry['time']['to'], timetable_entry['rhythm'], 'duration',
                                       timetable_entry['room'], timetable_entry['status'], timetable_entry['comment'],
                                       timetable_entry['elearn'], timetable_entry['einzeltermine_link'], lecture['id'],
                                       timetable_entry['dates'])
            temp_lecture.children.append(temp_entry)
        session.add(temp_lecture)

    data_file.close()

session.commit()
session.close()
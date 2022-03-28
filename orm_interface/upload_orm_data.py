import json
import io
from entities.lecture import Lecture, Professor, StudyProgram, Timetable
from base import Base, Session, engine
import datetime

DATA_DIRECTORY = 'D:\\Thesis scraper\\scrapers\\merged_data.json'
STUDYPROGRAMS_DIRECTORY = 'D:\\Thesis scraper\\scrapers\\study_programs.json'
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
    date_regex = "\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$"
    for lecture in data_json:
        lecture_id = lecture['id']
        lecture_url = lecture['url']
        lecture_name = lecture['name']
        lecture_subject_type = lecture['subject_type']
        lecture_semester = lecture['semester']
        lecture_sws = lecture['sws']
        lecture_longtext = lecture['longtext']
        lecture_shorttext = lecture['shorttext']
        lecture_language = lecture['language']
        lecture_hyperlink = lecture['hyperlink']
        lecture_description = lecture['description']
        lecture_keywords = lecture["keywords"]

        if lecture_subject_type == 'Übung' and 'Übung' not in lecture_name:
            lecture_name = 'Übung zu ' + lecture_name
        elif lecture_subject_type == 'Übung/mit Tutorien' and 'Übung/mit Tutorien' not in lecture_name:
            lecture_name = 'Übung/mit Tutorien zu ' + lecture_name
        elif lecture_subject_type == 'Tutorium' and 'Tutorium' not in lecture_name:
            lecture_name = 'Tutorium zu ' + lecture_name
        elif lecture_subject_type == 'Einführung' and 'Einfürhrung' not in lecture_name:
            lecture_name = 'Einführung zu ' + lecture_name

        temp_lecture = Lecture(id=lecture_id, name=lecture_name, url=lecture_url, subject_type=lecture_subject_type,
                               semester=lecture_semester,sws=lecture_sws, longtext=lecture_longtext, shorttext=lecture_shorttext,
                               language=lecture_language,hyperlink=lecture_hyperlink, description=lecture_description,
                               keywords=lecture_keywords)

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

            duration = ''
            duration_from = duration_to = datetime.date(1999,2,4)
            if type(timetable_entry['duration']) == str:
                if 'am' in timetable_entry['duration']:
                    duration = 'AM'
                elif 'von' in timetable_entry['duration']:
                    duration = 'VON'
                elif len(timetable_entry['duration']) == 0:
                    duration = 'EMPTY'

            dates = []
            if 'dates' in timetable_entry.keys():
                dates = timetable_entry['dates']
                if len(dates) > 0:
                    duration_from = dates[0]
                    duration_to = dates[-1]

            temp_entry = Timetable(timetable_entry['id'], timetable_entry['day'], timetable_entry['time']['from'],
                                       timetable_entry['time']['to'], timetable_entry['rhythm'], duration, duration_from, duration_to,
                                       timetable_entry['room'], timetable_entry['status'], timetable_entry['comment'],
                                       timetable_entry['elearn'], timetable_entry['einzeltermine_link'], lecture['id'],
                                       dates)
            temp_lecture.timetables.append(temp_entry)
        session.add(temp_lecture)

    data_file.close()

session.commit()
session.close()
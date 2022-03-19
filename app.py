from flask import Flask, jsonify, request
from flask_cors import CORS
from orm_interface.base import Session
from orm_interface.entities.lecture import StudyProgram, Lecture

session = Session()

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/get_studyprograms", methods=["GET"])
def get_studyprograms():
    all_studyprograms = session.query(StudyProgram).all()
    response = []
    for studyprogram in all_studyprograms:
        lectures = studyprogram.lectures
        seminar, vorlesung, vorlesung_uebung, uebung = 0,0,0,0
        for lecture in lectures:
            if len(lecture.sws.strip()) > 0:
                if lecture.subject_type == "Vorlesung":
                    vorlesung += int(lecture.sws)
                elif lecture.subject_type == "Seminar":
                    seminar += int(lecture.sws)
                elif lecture.subject_type == "Vorlesung/Übung":
                    vorlesung_uebung += int(lecture.sws)
                elif lecture.subject_type == "Übung":
                    uebung += int(lecture.sws)

        response.append({
            "id": studyprogram.id,
            "name": studyprogram.name,
            "url": studyprogram.url,
            "stats": {
                "Vorlesung": vorlesung,
                "Vorlesung/Übung": vorlesung_uebung,
                "Übung": uebung,
                "Seminar": seminar
            }
        })
    return jsonify(response)

@app.route("/get_lecture_with_id", methods=["GET"])
def get_lecture_with_id():
    args = request.args
    lecture = session.query(Lecture).filter(Lecture.id==args.get('id')).first()
    if not lecture:
        return "not found"
    response = {
        "id": lecture.id,
        "url": lecture.url,
        "name": lecture.name,
        "subject_type": lecture.subject_type,
        "sws": lecture.sws,
        "longtext": lecture.longtext,
        "shorttext": lecture.shorttext,
        "language": lecture.language,
        "description": lecture.description
    }

    return jsonify(response)

@app.route("/get_lectures_with_root_id", methods=["GET"])
def get_lectures_with_root_id():
    args = request.args
    root_id = args.get('id')
    studyprogram = session.query(StudyProgram).filter(StudyProgram.id==root_id).first()
    lectures = studyprogram.lectures
    response = []
    for lecture in lectures:
        timetables = lecture.timetables
        response_timetables = []
        for timetable in timetables:
            response_timetables.append({
                "id": timetable.id,
                "comment": timetable.comment,
                "day": timetable.day,
                "duration": {
                    "from": timetable.duration_from,
                    "to": timetable.duration_to
                },
                "elearn": timetable.elearn,
                "rhythm": timetable.rhythm,
                "room": timetable.room,
                "status": timetable.status,
                "time": {
                    "from": timetable.time_from,
                    "to": timetable.time_to
                }
            })
        response.append({
            "id": lecture.id,
            "url": lecture.url,
            "name": lecture.name,
            "subject_type": lecture.subject_type,
            "sws": lecture.sws,
            "longtext": lecture.longtext,
            "shorttext": lecture.shorttext,
            "language": lecture.language,
            "description": lecture.description,
            "timetable": response_timetables
        })
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
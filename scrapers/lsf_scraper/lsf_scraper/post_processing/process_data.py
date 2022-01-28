import io
import json

# LECTURE_DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), "scrapers", "lsf_scraper", "lecture_results.json"))
LECTURE_DATA = 'D:\\Thesis scraper\\scrapers\\lsf_scraper\\lecture_results.json'
OUTPUT_FILE = 'D:\\Thesis scraper\\scrapers\\lsf_scraper\\lsf_scraper\\Data\\post_processed_lectures.json'

def merge_lectures_with_same_id(subjects_list) -> dict:
    seen_subjects_dict = {}
    for entry in subjects_list:
        if entry['id'] in seen_subjects_dict.keys():
            seen_subjects_dict[entry['id']]['parent_id'].append(entry['parent_id'])
        else:
            seen_subjects_dict[entry['id']] = entry
            seen_subjects_dict[entry['id']]['parent_id'] = [entry['parent_id']]

    return seen_subjects_dict

def process_timetable_of_subject(subject):
    processed_timetable = []
    for entry in subject['timetable']['entries']:
        times = entry['time'].split('\xa0bis\xa0')
        if len(times) == 2:
            time = {
                'from': times[0].replace('\xa0',''),
                'to': times[1].replace('\xa0',''),
            }
            entry['time'] = time

        durations = entry['duration'].split('\xa0bis\xa0')
        if len(durations) == 2:
            duration = {
                'from': durations[0].replace('\xa0',''),
                'to': durations[1].replace('\xa0','')
            }
            entry['duration'] = duration

        processed_timetable.append(entry)

    subject['timetable'] = processed_timetable
    return subject

def create_list_from_lecture_dict(lectures_dict):
    lecture_list = []
    for key, value in lectures_dict.items():
        lecture_list.append(value)
    return lecture_list

with io.open(LECTURE_DATA, encoding='utf8') as json_file:
    data = json.load(json_file)
    subjects_dict = {}
    categories_dict = {}
    einzeltermine_dict = {}
    subjects_list = []
    einzeltermine_list = []

    for entry in data:
        if 'subject_type' in entry.keys():
            subjects_list.append(entry)
        elif 'type' in entry.keys():
            einzeltermine_list.append(entry)

    merged_lectures = merge_lectures_with_same_id(subjects_list)

    print(len(merged_lectures))
    for key, value in merged_lectures.items():
        merged_lectures[key] = process_timetable_of_subject(value)
    print(type(merged_lectures))

    with io.open(OUTPUT_FILE, 'w', encoding='UTF8') as output_file:
        json.dump(merged_lectures, output_file, ensure_ascii=False)
        output_file.close()

    json_file.close()
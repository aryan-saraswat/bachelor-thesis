import io
import json
from difflib import SequenceMatcher
from pprint import pprint

lsf_data_directory = '.\\lsf_scraper\\lsf_scraper\\Data\\post_processed_lectures.json'
vdb_data_directory = '.\\vdb_scraper\\vdb_scraper\\Data\\post_processed_descriptions.json'
merged_data_directory = '.\\merged_data.json'

def clear_merged_data_directory():
    open(merged_data_directory, 'w').close()

def similar(name1, nameList):
    ratio = 0
    result = ''
    for name in nameList:
        if SequenceMatcher(None, name1, name).ratio() > ratio:
            ratio = SequenceMatcher(None, name1, name).ratio()
            result = name
    if ratio > 0.60:
        return (result, ratio)
    else:
        return (None, None)

with io.open(vdb_data_directory, encoding='UTF8') as vdb_data, io.open(lsf_data_directory, encoding='UTF8') as lsf_data, io.open(merged_data_directory, 'w', encoding='UTF8') as output_file:
    vdb_json = json.load(vdb_data)
    lsf_json = json.load(lsf_data)

    print(len(vdb_json))
    print(len(lsf_json))
    print(lsf_json)
    matches = 0
    somewhat_same = 0
    similarity_too_low = 0

    lecture_name_list = list(vdb_json.keys()) # list of names of lectures in the Vorlesungsdatenbank data (descriptions)
    distant_matches = []

    for lecture in lsf_json:
        subject = lecture['name']
        # if 'zu' in subject:
        #     subject = ' '.join(subject.split(' ')[2:]).replace('"', '')
        if subject in vdb_json.keys(): # checking if the subject from the lsf_data is in the keys of the vdb dictionary
            matches = matches + 1
            lecture['description'] = vdb_json[subject]['description']['en'] # en because only English description is relevant for us
            # print('exact match:\t{}\t---->\t{}'.format(subject, lsf_value['name']))
        else:
            result = similar(subject, lecture_name_list)
            closest_match, ratio = result[0], result[1]
            if not closest_match:
                similarity_too_low = similarity_too_low + 1
                print('no match for:\t{}'.format(subject))
            else:
                somewhat_same = somewhat_same + 1
                distant_matches.append({
                    "original": subject,
                    "closest_match": closest_match,
                    "ratio": ratio
                })
                lecture['description'] = vdb_json[closest_match]['description']['en'] # if it's a close enough match, then merge the descriptions anyway (English ones)

    print(len(distant_matches))
    pprint(distant_matches)
    print('exact matches: {}, somewhat same: {}, no close enough match: {}'.format(matches, somewhat_same, similarity_too_low))

    json.dump(lsf_json, output_file, ensure_ascii=False)
    output_file.close()
    vdb_data.close()
    lsf_data.close()
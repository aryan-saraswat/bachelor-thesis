import io
import json

VDB_DATA_DIRECTORY = 'D:\\Thesis scraper\\scrapers\\vdb_scraper\\description_results.json'
VDB_DESTINATION_DIRECTORY = 'D:\\Thesis scraper\\scrapers\\vdb_scraper\\vdb_scraper\\Data\\post_processed_descriptions.json'

with io.open(VDB_DATA_DIRECTORY, encoding='utf8') as json_file:
    data = json.load(json_file)
    lectures_dict = {}
    lectures_set = set()
    lectures_list = []

    print(len(data))
    for entry in data:
        if entry['name'] in lectures_dict.keys():
            print('duplicate found {}'.format(entry['id']))
        else:
            lectures_dict[entry['name']] = entry

    print(len(lectures_dict))

    with io.open(VDB_DESTINATION_DIRECTORY, 'w', encoding='UTF8') as output_file:
        json.dump(lectures_dict, output_file, ensure_ascii=False)
        output_file.close()

    json_file.close()
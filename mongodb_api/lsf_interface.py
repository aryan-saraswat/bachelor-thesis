from pymongo import MongoClient
from pprint import pprint

class LsfInterface:

    def __init__(self, port=27017):
        self.client = MongoClient(port=port)
        self.db = self.client.thesis_test  #thesis_test is the name of the database where different collections are stored

    def clean_collection(self):
        result = self.db.lsf_einz_7.delete_many({})
        return result

    def find_lecture_by_name(self, lecture_name) -> list:
        lectures = self.db.merged_data_1.find({"name": lecture_name})
        result = []
        for lecture in lectures:
            result.append(lecture)
        return result

    def find_lectures_with_description(self):
        lectures = self.db.merged_data_1.find({})
        result = []
        for lecture in lectures:
            if len(lecture['description']) == 0:
                result.append(lecture)
        return result
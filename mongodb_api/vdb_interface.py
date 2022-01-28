from pymongo import MongoClient
from pprint import pprint

class VdbInterface:

    def __init__(self, port=27017):
        self.client = MongoClient(port=port)
        self.db = self.client.thesis_test  #thesis_test is the name of the database where different collections are stored

    def find_lecture_by_name(self, lecture_name: str) -> list:
        lectures = self.db.vdb6_en.find({"name": lecture_name})
        result = []
        for lecture in lectures:
            result.append(lecture)
        return result
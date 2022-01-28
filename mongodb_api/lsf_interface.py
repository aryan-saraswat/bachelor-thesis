from pymongo import MongoClient
from pprint import pprint

class LsfInterface:

    def __init__(self, port=27017):
        self.client = MongoClient(port=port)
        self.db = self.client.thesis_test  #thesis_test is the name of the database where different collections are stored

    def find_lecture_by_name(self, lecture_name) -> list:
        lectures = self.db.new9.find({"name": lecture_name})
        result = []
        for lecture in lectures:
            result.append(lecture)
        return result
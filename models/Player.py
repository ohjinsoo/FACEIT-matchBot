import json

class Player:

    def __init__(self, j):
         self.__dict__ = json.loads(j)
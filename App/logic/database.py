
"""For now, store the words as JSON in a file. Later, we can use a database.
"""

import json
import os


class Database:
    def __init__(self, database_path):
        self.database_path = database_path
        self.database = self.load_database()

    def load_database(self):
        if not os.path.exists(self.database_path):
            return {}
        else:
            with open(self.database_path, "r") as f:
                return json.load(f)
            
    def save_database(self):
        with open(self.database_path, "w") as f:
            json.dump(self.database, f)


    def add_word(self, word): # TODO
        if word not in self.database:
            self.database[word] = 1
        else:
            self.database[word] += 1


    




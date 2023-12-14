
class Word:
    def __init__(self, text, start_time, end_time):
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
    
    def save_to_database(self):
        print(f"saving to database: {self.text}")
        pass


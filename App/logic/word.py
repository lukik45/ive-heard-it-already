

class Phrase:
    next_id = 1 #fixme: read this value from metadata file

    @staticmethod
    def get_next_id():
        current_id = Phrase.next_id
        Phrase.next_id += 1
        return current_id
    

    def __init__(self, phrase):
        self.id = Phrase.get_next_id()


class Word:
    def __init__(self, text, start_time, end_time):
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
    
    def save_to_database(self):
        print(f"saving to database: {self.text}")
        pass

    # def spawn_in_gui(self, gui_container):
        
    #     gui_container.add(self)

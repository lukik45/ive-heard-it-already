class Phrase:
    next_id = 1 #fixme: read this value from metadata file

    @staticmethod
    def get_next_id():
        current_id = Phrase.next_id
        Phrase.next_id += 1
        return current_id
    

    def __init__(self, phrase):
        self.id = Phrase.get_next_id()

from queue import Queue
import json

class Interpreter:
    """Interprets the transcription and converts it to our data 
    representation system
    """
    def __init__(self):
        self.previous_transcript_length = 0
        self.words = []
        

    def interpret(self, transcript_queue: Queue, command_queue: Queue, words_queue: Queue):
        
        while not command_queue.empty():
            try:
                transcript_json = transcript_queue.get()
                transcript = json.loads(transcript_json)["partial"]
                if self.previous_transcript_length <= len(transcript):
                    # cut the transcript to only the new part
                    words_queue.put(transcript)
                    self.previous_transcript_length = len(transcript)
                else:  # if no changes were made to the transcript
                    continue
            except KeyError: # if the transcript is final or text?
                continue




            print(transcript)
            

    
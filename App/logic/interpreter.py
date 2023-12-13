from queue import Queue
import json
from collections import deque
from word import Word

class Interpreter:
    """Interprets the transcription and converts it to our data 
    representation system
    """
    def __init__(self):
        self.previous_transcript_length = 0
        self.words = []
        
    def interpret_words(self, transcript_queue: Queue, command_queue: Queue, words_queue: Queue):
        last_transcript_length = 0
        
        while not command_queue.empty():
            try:
                transcript_json: list = json.loads(transcript_queue.get())["partial_result"]
                if last_transcript_length < len(transcript_json):
                    new_words = transcript_json[last_transcript_length:]

                elif last_transcript_length > len(transcript_json):
                    new_words = transcript_json
                    last_transcript_length = len(transcript_json)
                
                else: # if no changes were made to the transcript
                    continue
                    
                for word in new_words:
                    # words_queue.put(word["word"])
                    
                    # create a new word object
                    word_object = Word(word["word"], word["start"], word["end"])
                    words_queue.put(word_object)
                    print(word["word"])
                    last_transcript_length += 1

            except KeyError: # if the transcript is final or text?
                continue
            except Exception as e:
                print(e)
                continue

    
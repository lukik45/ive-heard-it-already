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
                    words_queue.put(word["word"])
                    last_transcript_length += 1


            except Exception as e:
                print(e)
                continue
            # try:
            #     # wait for the item to appear in the queue
            #     transcript_json = transcript_queue.get()
            #     transcript = json.loads(transcript_json)["partial"]
            #     if self.previous_transcript_length <= len(transcript):
            #         # cut the transcript to only the new part
            #         words_queue.put(transcript)
            #         self.previous_transcript_length = len(transcript)
            #     else:  # if no changes were made to the transcript
            #         continue
            # except KeyError: # if the transcript is final or text?
            #     continue




            # print(transcript)
            continue

    
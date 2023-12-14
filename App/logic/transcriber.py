import pyaudio
import numpy as np
from abc import ABC, abstractmethod
from queue import Queue
from vosk import Model, KaldiRecognizer
from metadata import *
import json
from _utils import *



class Transcriber(ABC):
    """Abstract class for transcribers"""
    def __init__(self):
        self.p = pyaudio.PyAudio()
        # fixme: works only on this mac
        

        self.stream = self.p.open(rate=SAMPLE_RATE,
                                  channels=CHANNELS,
                                  format=AUDIO_FORMAT,
                                  input=True,
                                  input_device_index=get_input_device_index(self.p),
                                  frames_per_buffer=CHUNK_SIZE)
        self.stream.start_stream()
    
    @abstractmethod
    def transcribe(self, transcript_queue: Queue, command_queue: Queue):
        """Reads the audio stream and puts the JSON transcript in the queue
        args:
            transcript_queue: Queue
                Queue to put the transcript in
            command_queue: Queue
                Queue to check for commands
        """
        pass

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        # super().__del__(self)


class VoskTranscriber(Transcriber):
    def __init__(self, model_type="small"):
        super().__init__()
        if model_type == "small":
            # fixme - make this path relative
            self.model = Model(r"/Users/lukik45mb/projects/ive-heard-it-already/vosk-model-small-en-us-0.15")
        elif model_type == "large":
            self.model = Model(r"/Users/lukik45mb/projects/ive-heard-it-already/vosk-model-en-us-0.22")
        else:
            raise ValueError("Invalid model type")
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)
        self.recognizer.SetWords(True)
        self.recognizer.SetPartialWords(True)
        

    def transcribe(self, transcript_queue: Queue, command_queue: Queue):
        while not command_queue.empty(): # TODO: add a command to stop the transcription
            with open('partial.txt', 'a') as f:
                
                data = self.stream.read(CHUNK_SIZE, exception_on_overflow = False)
                if len(data) == 0:
                    print('no data----------------------------------')
                    break
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    # transcript_queue.put(result)
                    # print('accept waveform---------------------------')
                    # print('result: ', result)
                    continue
                else:
                    partial_result = self.recognizer.PartialResult()
                    transcript_queue.put(partial_result)
            # final_result = self.recognizer.FinalResult()
            # transcript_queue.put(final_result)

        


    
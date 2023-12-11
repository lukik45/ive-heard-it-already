import pyaudio
import numpy as np
from abc import ABC, abstractmethod
from queue import Queue
from vosk import Model, KaldiRecognizer
from metadata import *



class Transcriber(ABC):
    """Abstract class for transcribers"""
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(rate=SAMPLE_RATE,
                                  channels=CHANNELS,
                                  format=AUDIO_FORMAT,
                                  input=True,
                                  frames_per_buffer=CHUNK_SIZE)
        self.stream.start_stream()
    
    @abstractmethod
    def transcribe(self):
        pass

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        super().__del__()


class VoskTranscriber(Transcriber):
    def __init__(self):
        super().__init__()
        self.model = Model(r"/Users/lukik45mb/projects/ive-heard-it-already/vosk-model-small-en-us-0.15")
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)
        self.recognizer.SetWords(True)

    def transcribe(self, transcript_queue: Queue, command_queue: Queue):
        while not command_queue.empty(): # TODO: add a command to stop the transcription
            data = self.stream.read(CHUNK_SIZE, exception_on_overflow = False)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                transcript_queue.put(result)
            else:
                partial_result = self.recognizer.PartialResult()
                transcript_queue.put(partial_result)
        # final_result = self.recognizer.FinalResult()
        # transcript_queue.put(final_result)

        


    
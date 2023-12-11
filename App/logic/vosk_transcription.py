from vosk import Model, KaldiRecognizer
import pyaudio
from test import test_all









def main():
    if not test_all():
        raise Exception("Audio input not set up correctly")



    model = Model(r"/Users/lukik45mb/projects/ive-heard-it-already/vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)



    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, 
                    channels=1, 
                    rate=16000, 
                    input=True, 
                    frames_per_buffer=8192)
    stream.start_stream()

    while True:
        print('starting...')
        data = stream.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            print('accepted')
            print(recognizer.Result())
        else:
            print(recognizer.PartialResult())

    print(recognizer.FinalResult())

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    main()
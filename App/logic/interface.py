import transcriber as tr
from interpreter import Interpreter


def transcribe_audio(transcript_queue, command_queue):
    transcriber = tr.VoskTranscriber(model_type='large') #fixme - possible issue due to the naming
    transcriber.transcribe(transcript_queue, command_queue)



def interpret_transcript(transcript_queue, command_queue, words_queue):
    interpreter = Interpreter()
    interpreter.interpret(transcript_queue, command_queue, words_queue)



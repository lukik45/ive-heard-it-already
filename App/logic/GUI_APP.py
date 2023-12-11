import customtkinter as ctk
from queue import Queue
from threading import Thread
import interface
from time import sleep
from test import test_all


transcript_queue = Queue()
words_queue = Queue()
command_queue = Queue() # for multithread communication


class SideMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=0)

        self.start_recording_button = ctk.CTkButton(self, text="Start Recording", command=self.start_recording_button_clicked)
        self.start_recording_button.grid(row=0, column=0)

        self.stop_recording_button = ctk.CTkButton(self, text="Stop Recording", command=self.stop_recording_button_clicked)
        self.stop_recording_button.grid(row=1, column=0)


    def start_recording_button_clicked(self):
        print("start recording button clicked!")

    def stop_recording_button_clicked(self):
        print("stop recording button clicked!")

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=0)

        self.transcript_label = ctk.CTkLabel(self, text="Hello, Tkinter!")
        self.transcript_label.grid(row=0, column=0)


class WordFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.text_label = ctk.CTkLabel(self, text="", wraplength=200)
        self.text_label.grid(row=0, column=0, sticky="nsew")

    def update_text_label(self, text):
                self.text_label.configure(text=text)



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x400")
        self.title("I've heard it already!")
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)

        self.side_menu = SideMenuFrame(self)
        self.side_menu.grid(row=0, column=0, sticky="nsw")

        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.word_frame = WordFrame(self)  
        self.word_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

    


    def update_ui(self, ):
        while not command_queue.empty():
            
            if not words_queue.empty():

                word = words_queue.get()
                self.word_frame.update_text_label(word)
            sleep(0.05)
            




def main():
    test_all()


    app = App()

    command_queue.put(True) #TODO - this should be handled by the GUI
    trancription_thread = Thread(target=interface.transcribe_audio, 
                                 args=(transcript_queue, command_queue))
    trancription_thread.start()

    interpretation_thread = Thread(target=interface.interpret_transcript,
                                   args=(transcript_queue, command_queue, words_queue))
    interpretation_thread.start()

    ui_thread = Thread(target=app.update_ui) # words_queue already accesible
    ui_thread.start()






    app.mainloop()

if __name__ == "__main__":
    main()
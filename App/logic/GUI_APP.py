import customtkinter as ctk
from queue import Queue
from threading import Thread
import interface
from time import sleep
from test import test_all
from word import Word


transcript_queue = Queue()
words_queue = Queue()
command_queue = Queue() # for multithread communication


class TopMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=0)

        self.start_recording_button = ctk.CTkButton(self, text="Start Recording", command=self.start_recording_button_clicked, width=20)
        self.start_recording_button.pack(side='left')

        self.stop_recording_button = ctk.CTkButton(self, text="Stop Recording", command=self.stop_recording_button_clicked, width=20)
        self.stop_recording_button.pack(side='left')

    def start_recording_button_clicked(self):
        print("start recording button clicked!")

    def stop_recording_button_clicked(self):
        command_queue.get()
        print("stop recording button clicked!")



class WordFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        
        self.canvas = ctk.CTkCanvas(self)
        self.canvas.pack(side="top", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x")

        # configure the canvas to use the scrollbar
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # create another frame inside the canvas to hold the buttons
        self.button_frame = ctk.CTkFrame(self.canvas)
        # add the button frame to a window in the canvas
        self.canvas.create_window((0,0), window=self.button_frame, anchor="nw")
        
        # for i in range(20):
        #     ctk.CTkButton(self.button_frame, text=f'Button {i+1}').pack(side='left')

        self.button_frame.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # scroll to the rightmost item
        self.canvas.xview_moveto(1)

        




class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x300")
        self.title("I've heard it already!")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.side_menu = TopMenuFrame(self)
        self.side_menu.grid(row=0, column=0, sticky="new")

        self.word_frame = WordFrame(self)  
        self.word_frame.grid(row=1, column=0, sticky="nsew")

    


    def update_ui(self ):
        try:
            count=0
            
            while not command_queue.empty():
                
                if not words_queue.empty():
                    
                    word_object: Word = words_queue.get()
                    word_button = ctk.CTkButton(self.word_frame.button_frame, 
                                                text=word_object.text,
                                                width=len(word_object.text),
                                                # callback function
                                                command=lambda: word_object.save_to_database())
                    
                    word_button.pack(side='left')

                    self.word_frame.button_frame.update()
                    self.word_frame.canvas.configure(scrollregion=self.word_frame.canvas.bbox("all"))

                    # scroll to the rightmostem
                    self.word_frame.canvas.xview_moveto(1)
                    
                    # # update the scroll region
                    # self.word_frame.scrollable_frame.update()
                    # self.word_frame.canvas.configure(scrollregion=self.word_frame.canvas.bbox("all"))

                    # # pack the frame
                    # self.word_frame.scrollable_frame.pack(fill="both", expand=True)
                    count += 1
                    print(f"word added to the UI: {word_object.text}, {count} ")

                    
                # sleep(0.05) nie ma spania!
        except Exception as e: 
            print(e)



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
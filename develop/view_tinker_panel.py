from cProfile import label
from os import stat
import tkinter as tk
from tkinter import BOTTOM, ttk
from tkinter import filedialog
import tkinter.font as tkFont

from click import command
from gevent import config
from sympy import per

import configparser 
import os
import time
import shutil
import ctypes
import glob




class View_tinker:
    WORD_PRED_NUM = [1,2,3,4]
    WORD_DISP_LOC = ["Fixed", "Above last pressed key"]
    WORD_PRED_APPROACH = ["Retrieval", "Generation"]

    
    K1_BM25OKAPI = 1.5
    B_BM25OKAPI = 0.75
    EPSILON_BM25OKAPI = 0.25

    SEN_PRED_NUM = [1,2,3,4]
    SEN_ENTRY_APPROACH = ["Left to right", "Keywords"]
    SEN_PRED_APPROACH = ["Retrieval", "Generation"]
    SEN_RETRIEVAL_METHOD = ["Textual similarity", "Semantic similarity"]
    SEN_RETRI_SEMAN_MODEL = ["all-mpnet-base-v2", "multi-qa-mpnet-base-dot-v1", "all-distilroberta-v1", "all-MiniLM-L12-v2", "multi-qa-distilbert-cos-v1", "all-MiniLM-L6-v2", "multi-qa-MiniLM-L6-cos-v1", "paraphrase-multilingual-mpnet-base-v2", "paraphrase-albert-small-v2", "paraphrase-multilingual-MiniLM-L12-v2", "paraphrase-MiniLM-L3-v2", "distiluse-base-multilingual-cased-v1", "distiluse-base-multilingual-cased-v2", "Please input..."]
    SEN_GEN_METHOD = ["ChatGPT"] 

    CHATGPT_TEMPERATURE_OPT = ["0.1 (conservative)", "0.3", "0.5 (neutral)", "0.7", "0.9 (imaginative)"]

    SEN_INTERATION_SCENARIO = ["Dialogue", "Narrative"]

    WORD_PRED_TASK = ""
    SENTENCE_PRED_TASK = ""

    BOOL_WORD_TINKERED = False
    BOOL_SENTENCE_TINKERED = False

    def __init__(self, controller):
        # self.comboboxStyle = ttk.Style()
        # self.comboboxStyle.configure('W.TCombobox', arrowsize = 20)


        self.controller = controller
        self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        self.config.sections()

        
        
    def _close(self):
        self.root.destroy()

    def _save_word_pred_settings(self):
        self.config.set('PREDICTION_TASK', 'word_pred', str(self.WORD_PRED_TASK))
        self.config.set('WORD_PREDICTION', 'max_pred_num', self.maxWordPredNum.get())
        self.config.set('WORD_PREDICTION', 'display_location', self.wordDisplayLocation.get())
        self.config.set('WORD_PREDICTION', 'method', self.wordPredApproach.get())
        
        if self.WORD_PRED_TASK == "WORD_BM25OKAPI":
            self.config.set('WORD_BM25OKAPI', 'k1', str(self.K1_BM25OKAPI)) # self.k1BM25Okapi_wordPred.get()
            self.config.set('WORD_BM25OKAPI', 'b', str(self.B_BM25OKAPI))
            self.config.set('WORD_BM25OKAPI', 'epsilon', str(self.EPSILON_BM25OKAPI))
        elif self.WORD_PRED_TASK == "WORD_CHATGPT":
            temperature = 0.5
            if "0.1" in self.wordChatGPTTemperature.get(): 
                temperature = 0.1
            elif "0.3" in self.wordChatGPTTemperature.get():
                temperature = 0.3
            elif "0.5" in self.wordChatGPTTemperature.get():
                temperature = 0.5
            elif "0.7" in self.wordChatGPTTemperature.get():
                temperature = 0.7
            elif "0.9" in self.wordChatGPTTemperature.get():
                temperature = 0.9
            self.config.set('WORD_CHATGPT', 'temperature', str(temperature))

    def _save_sentence_pred_settings(self):
        self.config.set('PREDICTION_TASK', 'sentence_pred', str(self.SENTENCE_PRED_TASK))
        self.config.set('SENTENCE_PREDICTION', 'max_pred_num', self.maxSenPredNum.get())
        self.config.set('SENTENCE_PREDICTION', 'sentence_entry_approach', self.senEntryApproach.get())
        self.config.set('SENTENCE_PREDICTION', 'prediction_approach', self.senPredApproach.get())

        if self.senPredApproach.get() == "Retrieval":
            self.config.set('SENTENCE_RETRIEVAL', 'method', self.senRetrievalMethod.get())
            if "Textual" in self.senRetrievalMethod.get():
                self.config.set('SENTENCE_BM25OKAPI', 'k1', str(self.K1_BM25OKAPI))
                self.config.set('SENTENCE_BM25OKAPI', 'b', str(self.B_BM25OKAPI))
                self.config.set('SENTENCE_BM25OKAPI', 'epsilon', str(self.EPSILON_BM25OKAPI))
                self.config.set('SENTENCE_TEXT_SIMILARITY', 'retri_method', "SENTENCE_BM25OKAPI")
            elif "Semantic" in self.senRetrievalMethod.get():
                self.config.set('SENTENCE_SEMANTIC_SIMILARITY', 'sen_retri_seman_model', str(self.SEN_RETRI_SEMAN_MODEL[0]))
        elif self.senPredApproach.get() == "Generation":
            self.config.set('SENTENCE_GENERATION', 'method', self.senGenMethod.get())
            if self.senGenMethod.get() == "ChatGPT":
                temperature = 0.5
                if "0.1" in self.senChatGPTTemperature.get(): 
                    temperature = 0.1
                elif "0.3" in self.senChatGPTTemperature.get():
                    temperature = 0.3
                elif "0.5" in self.senChatGPTTemperature.get():
                    temperature = 0.5
                elif "0.7" in self.senChatGPTTemperature.get():
                    temperature = 0.7
                elif "0.9" in self.senChatGPTTemperature.get():
                    temperature = 0.9
                self.config.set('SENTENCE_CHATGPT', 'temperature', str(temperature))
                self.config.set('SENTENCE_CHATGPT', 'scenario', self.senChatGPTInterationMethod.get())


    def _save(self):
        if self.SENTENCE_PRED_TASK == "SENTENCE_SEMANTIC_SIMILARITY":
            self._pop_up_model_loading_notification()

        if self.BOOL_WORD_TINKERED:
            self._save_word_pred_settings()
        if self.BOOL_SENTENCE_TINKERED:
            self._save_sentence_pred_settings()
        
        if self.BOOL_WORD_TINKERED or self.BOOL_SENTENCE_TINKERED:
            self.config.write(open(self.file,'w'))
            self.controller.get_tinker_data()
            self.save_setting()

        

        self.root.destroy()
        
        self.BOOL_WORD_TINKERED = False
        self.BOOL_SENTENCE_TINKERED = False

        

    def save_setting(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        tinkerFileName = "./analysis/prediction_setting/tinker_"+str(timestr)+".ini"
        # copy current .ini file
        shutil.copyfile('tinker.ini', tinkerFileName)

    def load_setting(self):
        saved_file = filedialog.askopenfilename(initialdir="/",title="Select a File", filetypes=(("Configuration files", "*.ini"),))
        shutil.copyfile(saved_file, 'tinker.ini')
        self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        self.config.sections()
        self.controller.get_tinker_data()



    def auto_load_the_latest_setting(self):   
        # If no previous setting (i.e. folder is empty), load a basic one
        if not os.listdir('./analysis/prediction_setting/'):
            self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
            self.config = configparser.ConfigParser()
            self.config.read(self.file)
            self.config.sections()
            self.controller.get_tinker_data()
        # else, load the last one
        else:
            fileList = glob.glob('./analysis/prediction_setting/*.ini')
            latestFile = max(fileList, key=os.path.getctime)
            self.config = configparser.ConfigParser()
            self.config.read(latestFile)
            self.config.sections()
            self.controller.get_tinker_data()
            

    def pop_up_prediction_settings_saved_notification(self):
        ctypes.windll.user32.MessageBoxW(0, "Current prediction settings have been saved.", "Info", 0)

    def default_setting(self):
        self.config.set('PREDICTION_TASK', 'word_pred', "WORD_BM25OKAPI")
        self.config.set('WORD_PREDICTION', 'max_pred_num', "4")
        self.config.set('WORD_PREDICTION', 'display_location', "Fixed")
        self.config.set('WORD_PREDICTION', 'method', "Retrieval")
        self.config.set('WORD_BM25OKAPI', 'k1', str(self.K1_BM25OKAPI))
        self.config.set('WORD_BM25OKAPI', 'b', str(self.B_BM25OKAPI))
        self.config.set('WORD_BM25OKAPI', 'epsilon', str(self.EPSILON_BM25OKAPI))

        self.config.set('PREDICTION_TASK', 'sentence_pred', "SENTENCE_BM25OKAPI")
        self.config.set('SENTENCE_PREDICTION', 'max_pred_num', "4")
        self.config.set('SENTENCE_PREDICTION', 'sentence_entry_approach', "Left to right")
        self.config.set('SENTENCE_PREDICTION', 'prediction_approach', "Retrieval")
        self.config.set('SENTENCE_RETRIEVAL', 'method', "Textual similarity")
        self.config.set('SENTENCE_TEXT_SIMILARITY', 'retri_method', "SENTENCE_BM25OKAPI")
        self.config.set('SENTENCE_BM25OKAPI', 'k1', str(self.K1_BM25OKAPI))
        self.config.set('SENTENCE_BM25OKAPI', 'b', str(self.B_BM25OKAPI))
        self.config.set('SENTENCE_BM25OKAPI', 'epsilon', str(self.EPSILON_BM25OKAPI))

        self.config.write(open(self.file,'w'))
        self.controller.get_tinker_data()


        
        

    def run(self):
        
        self.root = tk.Tk()
        self.root.title("Prediction Setting Panel")

        bigFont = tkFont.Font(family='Arial', size=20)
        self.root.option_add("*Font", bigFont)

        baseFrame = ttk.Frame(self.root)
        baseFrame.pack(padx=5, pady=5)
        
        # style = ttk.Style()
        # style.configure('TNotebook.Tab', font=("Arial", 50))

        tabControl = ttk.Notebook(baseFrame)
        
        
        tabWordPredFrame = ttk.Frame(tabControl)
        # tabWordPredFrame.option_add("*Font", bigFont)
        tabSenPredFrame = ttk.Frame(tabControl)
        # tabSenPredFrame.option_add("*Font", bigFont)
        
        
        tabControl.add(tabWordPredFrame)
        tabControl.add(tabSenPredFrame)

        tabControl.tab(0, text ='      Word Prediction      ')
        tabControl.tab(1, text ='      Sentence Prediction      ')

        tabControl.pack(expand = True, fill ="both")
        
        


        cancelBtn = ttk.Button(baseFrame, text="Cancel", command=self._close)
        cancelBtn.pack(ipadx=10, ipady=10, side=tk.RIGHT)

        confirmBtn = ttk.Button(baseFrame, text="Confirm", command=self._save) # style="Big.TButton",
        confirmBtn.pack(ipadx=10, ipady=10, side=tk.RIGHT)


        self._word_pred_panel(self.root, tabWordPredFrame)
        self._sentence_prediction_panel(self.root, tabSenPredFrame)

        self.root.mainloop() 


    def _word_pred_approach(self, event, frame):
        if self.wordPredApproach.get() == 'Generation':
            self.WORD_PRED_TASK = "WORD_CHATGPT"
            # row 4
            ttk.Label(frame, text="Creativity", font=('bold')).grid(sticky="E", column=0, row=4)
            self.wordChatGPTTemperature = ttk.Combobox(frame, values=self.CHATGPT_TEMPERATURE_OPT, state="readonly")
            self.wordChatGPTTemperature.current(2)
            self.wordChatGPTTemperature.grid(sticky="W", column=1, row=4)

        else: 
            self.WORD_PRED_TASK = "WORD_BM25OKAPI"
            # row 4
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=4)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=4)
        self.BOOL_WORD_TINKERED = True

    def _word_pred_panel(self, root, frame):
        # row 0
        ttk.Label(frame, text ="Word Prediction", font=('bold')).grid(sticky="E", column=0, row=0)

        # row 1
        ttk.Label(frame, text ="Max Prediction Number").grid(sticky="E", column=0, row=1)
        self.maxWordPredNum = ttk.Combobox(frame, values=self.WORD_PRED_NUM, state="readonly")
        # maxWordPredNumStringVar = tk.StringVar(frame, value=4)
        # maxWordPredNum = ttk.Spinbox(frame, from_=1, to=4, textvariable=maxWordPredNumStringVar, wrap=False)
        self.maxWordPredNum.grid(sticky="W", column=1, row=1)
        self.maxWordPredNum.current(3)

        # row 2
        ttk.Label(frame, text ="Display Location").grid(sticky="E", column=0, row=2)
        self.wordDisplayLocation = ttk.Combobox(frame, values=self.WORD_DISP_LOC, state="readonly")
        self.wordDisplayLocation.grid(sticky="W", column=1, row=2)
        self.wordDisplayLocation.current(1)

        # row 3
        ttk.Label(frame, text ="Prediction Approach").grid(sticky="E", column=0, row=3)
        self.wordPredApproach = ttk.Combobox(frame, values=self.WORD_PRED_APPROACH, state="readonly")
        self.wordPredApproach.grid(sticky="W", column=1, row=3)
        # self.wordPredApproach.current(0)
        self.wordPredApproach.bind("<<ComboboxSelected>>", lambda event: self._word_pred_approach(event, frame)) 

        # row 4
        ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=4)
        ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=4)


        

    """ Sentence Prediction Below """
    def _pop_up_model_loading_notification(self):
        ctypes.windll.user32.MessageBoxW(0, "Please wait a few minutes for downloading the model. You may close this window after the Prediction Setting Panel is automatically closed.", "Info", 0)

    def _sen_retrieval_method_combobox(self, event, frame): 
        if 'Semantic' in self.senRetrievalMethod.get():
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_SEMANTIC_SIMILARITY"
            self.BOOL_SENTENCE_TINKERED = True

        else:
            # Assign task self.senRetrievalMethod.get() == "Textual similarity"
            self.SENTENCE_PRED_TASK = "SENTENCE_BM25OKAPI"
            self.BOOL_SENTENCE_TINKERED = True

    


    def _sen_gen_method_combobox(self, event, frame):
        
        if self.senGenMethod.get() == "ChatGPT":
            # row 2
            # self.senEntryApproach.current(0)
            # self.senEntryApproach.state(["!disabled"])

            # row 5
            ttk.Label(frame, text="Interaction Scenario").grid(sticky="E", column=0, row=5)
            self.senChatGPTInterationMethod = ttk.Combobox(frame, values=self.SEN_INTERATION_SCENARIO, state="readonly")
            self.senChatGPTInterationMethod.current(0)
            self.senChatGPTInterationMethod.grid(sticky="W", column=1, row=5)
       
            # row 6
            ttk.Label(frame, text="      Creativity").grid(sticky="E", column=0, row=6)
            # ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=5)
            # senChatGPTTemperatureString = tk.StringVar()
            self.senChatGPTTemperature = ttk.Combobox(frame, values=self.CHATGPT_TEMPERATURE_OPT, state="readonly")
            self.senChatGPTTemperature.current(2)
            self.senChatGPTTemperature.grid(sticky="W", column=1, row=6)

            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_CHATGPT"
            self.BOOL_SENTENCE_TINKERED = True


    def _sen_pred_approach_combobox(self, event, frame):
        
        if self.senPredApproach.get() == "Retrieval":
            # row 2
            self.senEntryApproach.state(["!disabled"])
            # row 4
            ttk.Label(frame, text="       Retrieval Method").grid(sticky="E", column=0, row=4)
            self.senRetrievalMethod = ttk.Combobox(frame, values=self.SEN_RETRIEVAL_METHOD, state="readonly")
            self.senRetrievalMethod.grid(sticky="W", column=1, row=4)
            # self.senRetrievalMethod.current(0)
            self.senRetrievalMethod.bind("<<ComboboxSelected>>", lambda event: self._sen_retrieval_method_combobox(event, frame)) 
            # row 5
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=5)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=6)
            
        elif self.senPredApproach.get() == "Generation":
            # row 2
            self.senEntryApproach.state(["!disabled"])
            # row 4
            ttk.Label(frame, text="       Generation Method").grid(sticky="E", column=0, row=4)
            self.senGenMethod = ttk.Combobox(frame, values=self.SEN_GEN_METHOD, state="readonly")
            self.senGenMethod.grid(sticky="W", column=1, row=4)
            # self.senGenMethod.current(0)
            self.senGenMethod.bind("<<ComboboxSelected>>", lambda event: self._sen_gen_method_combobox(event, frame))
            
            self._sen_gen_method_combobox(event,frame)
            

            

    def _sentence_prediction_panel(self, root, frame):
        # row 0
        ttk.Label(frame, text ="Sentence Prediction", font=('bold')).grid(sticky="E", column = 0, row = 0)

        # row 1
        ttk.Label(frame, text ="Max Prediction Number").grid(sticky="E", column=0, row=1)
        self.maxSenPredNum = ttk.Combobox(frame, values=self.SEN_PRED_NUM, state="readonly")
        self.maxSenPredNum.grid(sticky="W", column=1, row=1)
        self.maxSenPredNum.current(3)
        

        # row 2
        ttk.Label(frame, text ="Sentence Entry Approach").grid(sticky="E", column=0, row=2)
        self.senEntryApproach = ttk.Combobox(frame, values=self.SEN_ENTRY_APPROACH, state="readonly")
        self.senEntryApproach.grid(sticky="W", column=1, row=2)
        self.senEntryApproach.current(0)

        # row 3
        ttk.Label(frame, text="Prediction Approach").grid(sticky="E", column=0, row=3)
        self.senPredApproach = ttk.Combobox(frame, values=self.SEN_PRED_APPROACH, state="readonly")
        self.senPredApproach.grid(sticky="W", column=1, row=3)
        # self.senPredApproach.current(0)
        self.senPredApproach.bind("<<ComboboxSelected>>", lambda event: self._sen_pred_approach_combobox(event, frame))

        
if __name__ == '__main__':
    panel = View_tinker()
    panel.run()

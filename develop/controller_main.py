from pyexpat import model
from develop.view_trace_analysis import View_trace_analysis
from develop.model_trace_analysis import Model_Trace_Analysis
from develop.model_log_data import Model_Log_Data
from develop.model_main import Model_main
from develop.view_main import View_main, View_menu, View_text_box, View_keypad, View_logging_indicator
from develop.view_tinker_panel import View_tinker
from develop.view_text_entry import View_text_edit
from develop.view_key_size import View_key_size
import pyttsx3
# from gtts import gTTS

import configparser 
import os
import sys



class Controller_main():
    
    def __init__(self):
        self.modelMain = Model_main()
        self.modelTraceAnalysis = Model_Trace_Analysis()
        self.modelLogData = Model_Log_Data()
        
        self.viewMain = View_main(self)
        
        self.viewEntry = View_text_box(self, self.viewMain)
        self.viewKeypad = View_keypad(self, self.viewMain, self.viewEntry)
        self.viewMenu = View_menu(self, self.viewMain)
        self.viewTextEdit = View_text_edit(self)
        self.viewTinker = View_tinker(self)
        self.viewTraceAnalysis = View_trace_analysis(self)
        self.viewLoggingIndicator = View_logging_indicator(self, self.viewMain)
        self.viewKeySize = View_key_size(self, self.viewKeypad)

        self.speakEngine = pyttsx3.init()
        # voice = self.speakEngine.getProperty('voice')
        # self.speakEngine.setProperty('voice', voice[0].id)
        self.speakEngine.setProperty('rate', 150)
        self.speakEngine.setProperty('volume', 1.2)

        self.traceLogFile = ""

        self.currentPressedKey = ""
        self.sentence_pred_PREDICTION_TASK = ""

        self.boolDrag = False
        
        self.boolTrace = False # set to True for experiment mode 

        self.boolBm25 = False
        self.boolRoberta = False
        self.boolGpt2 = False
        self.boolSenRetrieval = True
        self.boolSemantic = True

        self.boolWordPredDisplay = False
        self.boolWordPredOnPressedKey = False
        self.boolSentencePredDisplay = False

        self.currentFilledWords = []
        self.bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.file = os.path.abspath(os.path.join(self.bundle_dir, 'tinker.ini'))

        # self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        self.config.sections()
        
        self._experiment_mode()

    def main(self):
        self.viewMain.mainloop()


    def _experiment_mode(self):
        self.boolTrace = True
        # self.set_auto_trace()
        self.auto_load_the_latest_prediction_settings()
        self.auto_load_the_latest_ui_settings()
        

    def on_log_mode_button_click(self, textLoggingIndicator):
        if textLoggingIndicator == 'Logging typing':
            textLoggingIndicator = 'Logging stopped'
        else:
            textLoggingIndicator = 'Logging typing'
        self.viewLoggingIndicator.update_logging_indicator(textLoggingIndicator)



    def get_tinker_data(self):
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.file = os.path.abspath(os.path.join(bundle_dir, 'tinker.ini'))
        # self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        self.config.sections()
        # f = open(self.file, "r")
        # print("EXE>>>>>>>>>>\n"+f.read())
        # print("EXE>>>>>>>>>> File path: "+self.file)

        self.word_pred_PREDICTION_TASK          = self.config['PREDICTION_TASK']['word_pred']
        if self.word_pred_PREDICTION_TASK == '':
            self.boolWordPredDisplay = False
            # print(f"word pred task is empty")
        else:
            self.boolWordPredDisplay = True
            # print(f"word pred task: {self.word_pred_PREDICTION_TASK}")
        
        self.sentence_pred_PREDICTION_TASK      = self.config['PREDICTION_TASK']['sentence_pred']
        if self.sentence_pred_PREDICTION_TASK == '':
            self.boolSentencePredDisplay = False
            # print(f"sen pred task is empty")
        else:
            self.boolSentencePredDisplay = True
            # print(f"sen pred task: {self.sentence_pred_PREDICTION_TASK}")

        self.max_pred_num_WORD_PREDICTION       = int(self.config['WORD_PREDICTION']['max_pred_num'])
        self.display_location_WORD_PREDICTION   = str(self.config['WORD_PREDICTION']['display_location'])
        self.type_WORD_PREDICTION               = str(self.config['WORD_PREDICTION']['type'])
        self.method_WORD_PREDICTION             = str(self.config['WORD_PREDICTION']['method'])
        
        self.k1_WORD_BM25OKAPI           = float(self.config['WORD_BM25OKAPI']['k1'])
        self.b_WORD_BM25OKAPI            = float(self.config['WORD_BM25OKAPI']['b'])
        self.epsilon_WORD_BM25OKAPI      = float(self.config['WORD_BM25OKAPI']['epsilon'])

        self.temperature_WORD_CHATGPT   = float(self.config['WORD_CHATGPT']['temperature'])
        
        # self.b_WORD_BM25L               = float(self.config['WORD_BM25L']['b'])
        # self.delta_WORD_BM25L           = float(self.config['WORD_BM25L']['delta'])

        # self.k1_WORD_BM25PLUS           = float(self.config['WORD_BM25PLUS']['k1'])
        # self.b_WORD_BM25PLUS            = float(self.config['WORD_BM25PLUS']['b'])
        # self.delta_WORD_BM25PLUS        = float(self.config['WORD_BM25PLUS']['delta'])

        # self.model_WORD_GPT2            = str(self.config['WORD_GPT2']['model'])
        # self.seed_WORD_GPT2             = int(self.config['WORD_GPT2']['seed'])

        # self.model_WORD_ROBERTA         = str(self.config['WORD_ROBERTA']['model'])

        self.max_pred_num_SENTENCE_PREDICTION               = int(self.config['SENTENCE_PREDICTION']['max_pred_num'])
        self.sentence_entry_approach_SENTENCE_PREDICTION    = str(self.config['SENTENCE_PREDICTION']['sentence_entry_approach'])
        self.prediction_approach_SENTENCE_PREDICTION        = str(self.config['SENTENCE_PREDICTION']['prediction_approach'])
        self.similarity_SENTENCE_RETRIEVAL                  = str(self.config['SENTENCE_RETRIEVAL']['method'])
        self.retri_method_SENTENCE_TEXT_SIMILARITY          = str(self.config['SENTENCE_TEXT_SIMILARITY']['retri_method'])

        self.k1_SENTENCE_BM25OKAPI       = float(self.config['SENTENCE_BM25OKAPI']['k1'])
        self.b_SENTENCE_BM25OKAPI        = float(self.config['SENTENCE_BM25OKAPI']['b'])
        self.epsilon_SENTENCE_BM25OKAPI  = float(self.config['SENTENCE_BM25OKAPI']['epsilon'])


        self.sen_retri_seman_model_SENTENCE_SEMANTIC_SIMILARITY = str(self.config['SENTENCE_SEMANTIC_SIMILARITY']['sen_retri_seman_model'])
        self.method_SENTENCE_GENERATION                         = str(self.config['SENTENCE_GENERATION']['method'])

        self.temperature_SENTENCE_CHATGPT             = float(self.config['SENTENCE_CHATGPT']['temperature'])
        self.interaction_scenario_SENTENCE_CHATGPT    = str(self.config['SENTENCE_CHATGPT']['scenario'])

        self.assign_task()

    """ Tinker Panel responses below """

    def _word_prediction_settings(self):
        # link to view: show pred
        if self.word_pred_PREDICTION_TASK == '':
            self.viewKeypad.clear_placed_words()
        else:
            # make the first prediction based on current input
            if self.type_WORD_PREDICTION == 'Current and Next Word':
                self.modelMain.load_fill_word()
                entry = self.viewEntry.entry.get()
                if entry == "":
                    """ First word """
                    # self._make_word_fill(entry)
                    pass
                elif entry[-1] == " ":
                    """ Finished a word """
                    self._make_word_prediction(entry)
                    """ Log the word level text entry """
                    if self.boolTrace:
                        self.modelLogData.record_word_level_input(wordPredAlgo=self.word_pred_PREDICTION_TASK, sentencePredAlgo=self.sentence_pred_PREDICTION_TASK, sentenceEntryApproach=self.sentence_entry_approach_SENTENCE_PREDICTION, scenario=self.interaction_scenario_SENTENCE_CHATGPT, currentSen = entry)

                else:
                    """ Typing a word """
                    self._make_word_fill(entry)
            else: # 'Current Word'
                self.modelMain.load_fill_word()
                entry = self.viewEntry.entry.get()
                if entry == "":
                    pass
                elif entry[-1] == " ":
                    self.viewKeypad.clear_placed_words()
                else:
                    self._make_word_fill(entry)
                

        # link to view: show pred loaction
        if self.display_location_WORD_PREDICTION == 'Above last pressed key':
            self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = True
        elif self.display_location_WORD_PREDICTION == 'Fixed':
            self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = False

        # link to view: word pred num
        self.viewKeypad.WORD_PRED_NUM = self.max_pred_num_WORD_PREDICTION

        # link to model: word pred method
        self.modelMain.WORD_PRED_METHOD = self.word_pred_PREDICTION_TASK
        if self.word_pred_PREDICTION_TASK == "WORD_BM25OKAPI": # "BM25L", "BM25Plus", "GPT-2", "RoBERTa"
            option = "BM25OKAPI"
            self.modelMain.load_bm25_word(option, self.k1_WORD_BM25OKAPI, self.b_WORD_BM25OKAPI, epsilon=self.epsilon_WORD_BM25OKAPI)
        elif self.word_pred_PREDICTION_TASK == "WORD_CHATGPT":
            option = "CHATGPT"
            self.modelMain.load_chatgpt_word(option, self.temperature_SENTENCE_CHATGPT) 


    def _sentence_prediction_settings(self):
        # link to view: show pred
        
        # link to view: sentence pred num
        self.viewKeypad.SENT_PRED_NUM = self.max_pred_num_SENTENCE_PREDICTION

        # link to view and model: entry approach
        # TODO add the actual features for view and model
        if self.sentence_entry_approach_SENTENCE_PREDICTION == 'Keywords':
            self.viewKeypad.BOOL_ENTRY_BY_KEYWORDS = True
            self.viewTextEdit.BOOL_ENTRY_BY_KEYWORDS = True
            self.modelMain.BOOL_ENTRY_BY_KEYWORDS = True
        elif self.sentence_entry_approach_SENTENCE_PREDICTION == 'Left to right':
            self.viewKeypad.BOOL_ENTRY_BY_KEYWORDS = False
            self.viewTextEdit.BOOL_ENTRY_BY_KEYWORDS = False
            self.modelMain.BOOL_ENTRY_BY_KEYWORDS = False

        # link to model: sentence pred method
        self.modelMain.SENT_PRED_METHOD = self.sentence_pred_PREDICTION_TASK
        self.modelMain.prediction_approach_SENTENCE_PREDICTION = self.prediction_approach_SENTENCE_PREDICTION
        if self.sentence_pred_PREDICTION_TASK == 'SENTENCE_BM25OKAPI':
            option = 'BM25OKAPI'
            self.modelMain.load_bm25_sentence(option, self.k1_SENTENCE_BM25OKAPI, self.b_SENTENCE_BM25OKAPI, epsilon=self.epsilon_SENTENCE_BM25OKAPI)
        # elif self.sentence_pred_PREDICTION_TASK == 'SENTENCE_SEMANTIC_SIMILARITY':
        #     option = 'SENTENCE_SEMANTIC_SIMILARITY'
        #     self.modelMain.load_semantic_sen_retrieval_sentence(model=self.sen_retri_seman_model_SENTENCE_SEMANTIC_SIMILARITY)
        elif self.sentence_pred_PREDICTION_TASK == 'SENTENCE_CHATGPT':
            option = 'CHATGPT'
            self.modelMain.load_chatgpt_sentence(option, self.sentence_entry_approach_SENTENCE_PREDICTION, self.interaction_scenario_SENTENCE_CHATGPT, self.temperature_SENTENCE_CHATGPT) 

        # make the initial pred if there is entered text
        if self.sentence_pred_PREDICTION_TASK == '':
            self.viewKeypad.clear_placed_sentences()
            self.viewEntry.entry = ''
        else:
            entry = self.viewEntry.entry.get()
            if entry != '':
                predictedSentence = self._make_sentence_prediction(entry)
                self.viewKeypad.place_predicted_sentences(predSentence=predictedSentence) # TODO set different for KWickChat


    def assign_task(self):
        self._word_prediction_settings()
        self._sentence_prediction_settings()

    """ Tinker Panel responses above """
    
    """ ChatGPT interaction below """

    def pop_up_conv_partner_window_chatgpt(self):
        # view: pop up a new dialogue window
        # press button to recognise speech, or type text directly.
        # add sentence to historyKwickchat. 
        self.viewTextEdit.pop_up_conv_partner_window_chatgpt()
        
    def recognize_speech(self):
        partnerInput = self.modelMain.conv_partner_speech_recognition_chatgpt()
        self.viewTextEdit.show_conversation_partner_input_chatgpt(partnerInput)
        # record 
                
    def add_conv_partner_input_to_history(self, editedPartnerInput):
        self.modelMain.add_conv_partner_input_to_history_for_dialogue(editedPartnerInput)
        """ record conversation partner input """
        if self.boolTrace:
            self.modelLogData.record_conversation_partner_input(editedPartnerInput)

    def add_user_input_to_history_for_chatgpt(self, editedUserInput):
        # when 'Speak' btn is clicked
        self.modelMain.add_user_input_to_history_for_chatgpt(editedUserInput)
        
    
    def add_user_input_to_history_for_retrieval(self, userInput):
        self.modelMain.add_user_input_to_history_for_retrieval(userInput)
    
    """ ChatGPT interaction above """

   

        


    """ On button click below """


    def on_key_button_click(self, caption): # , boolWordPred, boolSenPred
        if self.boolDrag: 
            pass
        else:
            self.currentPressedKey = caption
            text = self.viewTextEdit.edit_text_letter(caption) 
            self.viewMain.textBox.set(text)
            if caption == "Clear All" or caption == "Speak":
                self.viewKeypad.clear_placed_words()
                self.viewKeypad.clear_placed_sentences()

        predWords = []
        predSentences = []

        entry = self.viewEntry.entry.get()
        if entry == "":
            """ Initial input """   
            if self.boolWordPredDisplay:      
                # set fill initial word  
                # predWords = self._make_word_fill(entry)
                pass
            else:
                self.viewKeypad.clear_placed_words()
            if self.boolSentencePredDisplay:
                # set sentence pred display

                # TODO set different cases, get predicted word
                predSentences = self._make_sentence_prediction_with_pred_words(entry, predWords)
            else:
                self.viewKeypad.clear_placed_sentences()

        elif entry[-1] == " ":
            """ Finished a word """
            if self.boolWordPredDisplay:      
                # set fill initial word  
                # self._make_word_fill(entry)
                predWords = self._make_word_prediction(entry)
                """ Log the word level text entry """
                if self.boolTrace:
                    self.modelLogData.record_word_level_input(wordPredAlgo=self.word_pred_PREDICTION_TASK, sentencePredAlgo=self.sentence_pred_PREDICTION_TASK, sentenceEntryApproach=self.sentence_entry_approach_SENTENCE_PREDICTION, scenario=self.interaction_scenario_SENTENCE_CHATGPT, currentSen = entry)

            else:
                self.viewKeypad.clear_placed_words()
            if  self.boolSentencePredDisplay:
                # set sentence pred display
                # print(f"In controller_main, key_button_click, current entry is: '{entry}'")
                predSentences = self._make_sentence_prediction(entry)
            else:
                self.viewKeypad.clear_placed_sentences()

        else:
            """ Typing a word """
            if self.boolWordPredDisplay:      
                # set fill initial word  
                predWords = self._make_word_fill(entry)
            else:
                self.viewKeypad.clear_placed_words()

            if  self.boolSentencePredDisplay:
                # set sentence pred display

                predSentences = self._make_sentence_prediction_with_pred_words(entry, predWords)

            else:
                self.viewKeypad.clear_placed_sentences()
  
        # Trace record
        if self.boolTrace == True:
            self.modelTraceAnalysis.record_pressed_button(caption='key: '+caption, wordPred=predWords, senPred=predSentences, currentSen=entry)
    
    def on_speak_button_click(self, entry):
        # Collcet user input as conversation history for ChatGPT
        if self.sentence_pred_PREDICTION_TASK == 'SENTENCE_CHATGPT':
            if entry != '':
                self.add_user_input_to_history_for_chatgpt(entry) 
                if self.interaction_scenario_SENTENCE_CHATGPT == 'Dialogue':
                    self.pop_up_conv_partner_window_chatgpt()
                # self.modelLogData.recored_sentence_level_input(wordPredAlgo=self.word_pred_PREDICTION_TASK, sentencePredAlgo=self.sentence_pred_PREDICTION_TASK, finishedSen=entry)
        else:
            if entry != '':
                self.add_user_input_to_history_for_retrieval(entry)
        # reload retrieval function
        if self.word_pred_PREDICTION_TASK == "WORD_BM25OKAPI": # "BM25L", "BM25Plus", "GPT-2", "RoBERTa"
            option = "BM25OKAPI"
            self.modelMain.load_bm25_word(option, self.k1_WORD_BM25OKAPI, self.b_WORD_BM25OKAPI, epsilon=self.epsilon_WORD_BM25OKAPI)
        # if self.word_pred_PREDICTION_TASK == "WORD_CHATGPT": 
        #     option = "WORD_CHATGPT"
        #     self.modelMain.load_chatgpt_word(option, self.temperature_WORD_CHATGPT)


        if self.sentence_pred_PREDICTION_TASK == 'SENTENCE_BM25OKAPI':
            option = 'BM25OKAPI'
            self.modelMain.load_bm25_sentence(option, self.k1_SENTENCE_BM25OKAPI, self.b_SENTENCE_BM25OKAPI, epsilon=self.epsilon_SENTENCE_BM25OKAPI)
        # elif self.sentence_pred_PREDICTION_TASK == 'SENTENCE_SEMANTIC_SIMILARITY':
        #  Do not load, it takes agoes. 
        #     option = 'SEMANTIC_SIMILARITY'
        #     self.modelMain.load_semantic_sen_retrieval_sentence(model=self.sen_retri_seman_model_SENTENCE_SEMANTIC_SIMILARITY)
        
        # elif self.sentence_pred_PREDICTION_TASK == 'SENTENCE_CHATGPT':
        #     option = 'SENTENCE_CHATGPT'
        #     self.modelMain.load_chatgpt_sentence(option, self.sentence_entry_approach_SENTENCE_PREDICTION, self.interaction_scenario_SENTENCE_CHATGPT, self.temperature_SENTENCE_CHATGPT)

            
    def on_predicted_word_button_click(self, entry):
        """ Present selected pred word on textbox """
        predictedWord = self.viewTextEdit.edit_text_word(entry)
        self.viewMain.textBox.set(predictedWord)

        predWords = []
        predSentences = []

        # """ Update the word prediction when operate the menu during the usage """
        # word pred control
        if self.boolWordPredDisplay:
            predWords = self._set_word_pred_place(self.boolWordPredOnPressedKey)
        else:
            self.viewKeypad.clear_placed_words()

        # sentence pred control
        if self.boolSentencePredDisplay:
            predSentences = self._make_sentence_prediction(self.viewEntry.entry.get())
        else:
            self.viewKeypad.clear_placed_sentences()
        
        # Trace record
        if self.boolTrace == True:
            currentSen = self.viewMain.textBox.get()
            self.modelTraceAnalysis.record_pressed_button(caption='word: '+entry, wordPred=predWords, senPred=predSentences, currentSen=currentSen)
        

    def on_predicted_sentence_button_click(self, entry):
        """ Present selected pred sentence on textbox """
        predictedSentence = self.viewTextEdit.edit_text_sentence(entry)
        # self._set_sentence_pred_place(predictedSentence)
        self.viewMain.textBox.set(predictedSentence)

        # word pred control
        if self.boolWordPredDisplay:
            predWords = self._set_word_pred_place(self.boolWordPredOnPressedKey)
        else:
            self.viewKeypad.clear_placed_words()

        # sentence pred control
        if self.boolSentencePredDisplay:
            predSentences = self._make_sentence_prediction(self.viewEntry.entry.get())
        else:
            self.viewKeypad.clear_placed_sentences()

        if self.boolTrace == True:
            self.modelTraceAnalysis.record_pressed_button(caption='sentence: '+predictedSentence, wordPred=predWords, senPred=predSentences, currentSen=entry)
        

    """ On button click above """

    """ Word and Sentence Prediction Below """
    # # done
    # def set_word_pred_num(self, num):
    #     self.viewKeypad.WORD_PRED_NUM = self.modelMain.set_word_pred_num(num)
    # # done
    # def set_sentence_pred_num(self, num):
    #     self.viewKeypad.SENT_PRED_NUM = self.modelMain.set_sentence_pred_num(num)

        

    def _make_word_fill(self, entry): 
        currentWords = self.modelMain.make_initail_word_and_word_fill(entry)
        self.currentFilledWords = currentWords
        self.viewKeypad.clear_placed_words()
        self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=currentWords)
        return currentWords

    def _make_word_prediction(self, entry):
        predictedWords = []
        # if self.prediction_approach_SENTENCE_PREDICTION == 'Retrieval':
        predictedWords = self.modelMain.make_word_prediction(entry)
        self.viewKeypad.clear_placed_words()
        self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=predictedWords)
        return predictedWords


    def _make_sentence_prediction(self, entry):
        predictedSentences = self.modelMain.make_sentence_prediction(entry)
        self.viewKeypad.clear_placed_sentences()
        self.viewKeypad.place_predicted_sentences(predSentence=predictedSentences)
        return predictedSentences
        # show word pred


    def _make_sentence_prediction_with_pred_words(self, entry, predWords):
        """ Show 2 sentence predictions for [the entry + first word], 1 sentence prediction for [the entry + second word] and [the entry + third word] """
        predictedSentences = []
        predSenTemp1 = []
        predSenTemp2 = []
        predSenTemp3 = []
        predSenTemp4 = []

        i = 0
        for word in predWords:
            if entry == "":
                entryWithPredWord = entry + word
            elif entry[-1] == " ":
                entryWithPredWord = entry + word
            else: 
                listOfWords = entry.split()
                lastWord = listOfWords[-1]
                indexOfLastWord = entry.rfind(lastWord)
                entryWithPredWord = entry[0:indexOfLastWord] + word
            # print(f"entryWithPredWord is {entryWithPredWord}.")
            predSen = self.modelMain.make_sentence_prediction(entryWithPredWord)
            
            if len(predSen) > 0:
                if i == 0:
                    predSenTemp1 = predSen
                elif i == 1:
                    predSenTemp2 = predSen
                elif i == 2: 
                    predSenTemp3 = predSen
                else:
                    predSenTemp4 = predSen
            i += 1

        if len(predSenTemp1) >= 2:
            for n in range(2):
                predictedSentences.append(predSenTemp1[n])
            if len(predSenTemp2) >= 1:
                predictedSentences.append(predSenTemp2[0]) 
                if len(predSenTemp3) >= 1:
                    """ ideal, all have pred -> 1,1,2,3 """
                    predictedSentences.append(predSenTemp3[0])
                else:
                    if len(predSenTemp4) >= 1:
                        """ temp3 == 0 && temp4 == 1 -> 1,1,2,4 """
                        predictedSentences.append(predSenTemp4[0])
                    else:
                        """ temp3 == 0 && temp4 == 0 -> 1,1,2 """
                        pass
            else:
                """ temp2 == 0 """
                if len(predSenTemp3) >= 1:
                    predictedSentences.append(predSenTemp3[0])
                    if len(predSenTemp4) >= 1:
                        """ -> 1,1,3,4 """
                        predictedSentences.append(predSenTemp4[0])
                    else:
                        """ temp4 == 0 """
                        if len(predSenTemp3) >= 2:
                            """ -> 1,1,3,3 """
                            predictedSentences.append(predSenTemp3[1])
                        else:
                            if len(predSenTemp1) >= 3: 
                                """ -> 1,1,1,3 """
                                predictedSentences[2] = predSenTemp1[2]
                                predictedSentences.append(predSenTemp3[0])
        
        if len(predictedSentences) < 4 and predSenTemp1 == 4:
            """ -> 1,1,1,1 """
            predictedSentences = []
            for sen in predSenTemp1:
                predictedSentences.append(sen)


        predictedSentencesWithoutNone = []
        for sen in predictedSentences:
            if sen != "":
                predictedSentencesWithoutNone.append(sen)
        self.viewKeypad.clear_placed_sentences()
        self.viewKeypad.place_predicted_sentences(predSentence=predictedSentencesWithoutNone)

        return predictedSentences


    def _set_word_pred_place(self, boolWordPlaceOnLastPressedKey):
        """ Link to view_main menu """
        """ self.boolWordPredDisplay is True """
        self.modelMain.load_fill_word()

        predWords = []
        # self.boolWordPredOnPressedKey = boolWordPlaceOnLastPressedKey
        
        # self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = self.modelMain.set_word_pred_on_last_pressed_key(self.boolWordPredOnPressedKey)

        if self.display_location_WORD_PREDICTION == 'Above last pressed key':
            self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = True
        elif self.display_location_WORD_PREDICTION == 'Fixed':
            self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = False

        entry = self.viewEntry.entry.get()
        if self.type_WORD_PREDICTION == "Current and Next Word":
            if entry == "":
                """ First word """
                # predWords = self._make_word_fill(entry)
                pass
            elif entry[-1] == " ":
                """ Finished a word """
                predWords = self._make_word_prediction(entry)
                """ Log the word level text entry """
                if self.boolTrace:
                    self.modelLogData.record_word_level_input(wordPredAlgo=self.word_pred_PREDICTION_TASK, sentencePredAlgo=self.sentence_pred_PREDICTION_TASK, sentenceEntryApproach=self.sentence_entry_approach_SENTENCE_PREDICTION, scenario=self.interaction_scenario_SENTENCE_CHATGPT, currentSen = entry)
            else:
                """ Typing a word """
                predWords = self._make_word_fill(entry)
        else: # "Current Word"
            if entry == "":
                pass
            elif entry[-1] == " ":
                self.viewKeypad.clear_placed_words()
            else:
                """ Typing a word """
                predWords = self._make_word_fill(entry)

        return predWords



    def _set_sentence_pred_place(self, predictedSentence):
        """ For menu setting """
        
        entry = self.viewEntry.entry.get()
        # print(f"In controller_main, current entry is: '{entry}'")
        predictedSentence = self._make_sentence_prediction(entry)
        # set button place method
        # self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = self.modelMain.set_word_pred_on_last_pressed_key(self.boolWordPredOnPressedKey)
        if self.display_location_WORD_PREDICTION == 'Above last pressed key':
            self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = True
        elif self.display_location_WORD_PREDICTION == 'Fixed':
            self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = False

        self.viewKeypad.clear_placed_sentences()
        
        if self.boolSentencePredDisplay:
            self.viewKeypad.place_predicted_sentences(predSentence=predictedSentence)


    """ Word and Sentence Prediction Above """


    """ UI control below """
    
    def set_drag(self, boolDrag):
        self.boolDrag = boolDrag
        if boolDrag == True:
            # disable text entry
            pass
        else:
            # enable text entry and save positions
            self.save_current_keyboard_layout()
        self.viewKeypad.KEY_DRAGABLE = self.modelMain.set_drag(boolDrag)
        self.viewKeypad.record_button_position_size()
        self.viewKeypad.refresh(self, self.viewMain, self.viewEntry)

    def set_key_size(self):
        self.viewKeySize.run()
        keySizeDict = self.viewKeySize.get_key_size_dict()
        

    """ UI control above """

    """ Save current prediction settings below """
    def save_current_prediction_settings(self):
        self.viewTinker.save_setting()
        self.viewTinker.pop_up_prediction_settings_saved_notification()
    """ Save current prediction settings above """


    """ Load previous prediction settings below """
    def load_previous_prediction_settings(self):
        self.viewTinker.load_setting()
    """ Load previous prediction settings above """

    """ Auto load the latest prediction settings below """
    def auto_load_the_latest_prediction_settings(self):
        self.viewTinker.auto_load_the_latest_setting()
    """ Auto load the latest prediction settings above """

    """ Load default layout below """
    def load_default_layout(self):
        self.viewKeypad.make_letterpad()



    """ Save current keyboard layout below """
    def save_current_keyboard_layout(self):
        self.viewKeypad.write_button_position_size()
        self.viewKeypad.pop_up_layout_saved_notification()
    """ Save current keyboard layout above """


    """ Load previous keyboard layout below """
    def load_previous_keyboard_layout(self):
        self.viewKeypad.browse_button_position_files()
    """ Load previous keyboard layout above """

    """ Auto load previous keyboard layout below """
    def auto_load_the_latest_ui_settings(self):
        self.viewKeypad.auto_load_the_latest_button_position()



    """ Set trace below """

    def set_trace(self, boolTrace):
        # self.boolTrace = boolTrace
        self.boolTrace = self.modelTraceAnalysis.set_trace(boolTrace)
        # self.modelTraceAnalysis.record_pressed_button(caption)

    """ Set trace above """

    def set_auto_trace(self):
        self.boolTrace = self.modelTraceAnalysis.set_trace(True)

    """ Set trace analysis below """

    def run_trace_analyse(self):
        # traceLogFile = self.viewTraceAnalysis.filePath
        T_interrupt_threshold = 5.0
        self.modelTraceAnalysis.run_trace_analyse(self.traceLogFile, T_interrupt_threshold)

    """ Set trace analysis above """

    """ Speak below """
    # a sentence is finished
    def speak_text(self, text):
        """ log word and sentence level entry """
        if self.boolTrace:
            self.modelLogData.record_word_level_input(wordPredAlgo=self.word_pred_PREDICTION_TASK, sentencePredAlgo=self.sentence_pred_PREDICTION_TASK, sentenceEntryApproach=self.sentence_entry_approach_SENTENCE_PREDICTION, scenario=self.interaction_scenario_SENTENCE_CHATGPT, currentSen = text)
            self.modelLogData.record_sentence_level_input(wordPredAlgo=self.word_pred_PREDICTION_TASK, sentencePredAlgo=self.sentence_pred_PREDICTION_TASK, sentenceEntryApproach=self.sentence_entry_approach_SENTENCE_PREDICTION, scenario=self.interaction_scenario_SENTENCE_CHATGPT, finishedSen=text)
        # self.text_to_speech(text)
        self.speakEngine.say(text)
        self.speakEngine.runAndWait()
        # self.speakEngine.stop()
    """ Speak above """

if __name__ == '__main__':
    keyboard = Controller_main()
    keyboard.main()

    # tinkerPanel = View_tinker(keyboard)
    # tinkerPanel.run()

import threading
from os import system
import os
from model_fill_word import Model_Fill_Word
from model_bm25 import Model_Bm25
from model_semantic_sentence_retrieval import Model_Semantic_Sentence_Retrieval
# from model_kwickchat.model_kwickchat import Model_Kwickchat
from model_speech_recognition import Model_Speech_Recognition
from model_trace_analysis import Model_Trace_Analysis
from model_chatgpt import Model_ChatGPT


class Model_main:
    
    sentence_pred_PREDICTION_TASK = ''
    prediction_approach_SENTENCE_PREDICTION = ''
    BOOL_ENTRY_BY_KEYWORDS = False
    WORD_PRED_METHOD = '' # exact task option
    SENT_PRED_METHOD = '' # exact task option

    SENT_ENTRY_APPROACH = 'Left to right' 
    
    # historyKwickchat = []    
    conversation_history = []

    # Don't change
    wordPredNum = 4 
    sentencePredNum = 4

    def __init__(self):
        self.previousEntry = ''
        self.entry = ''
        self.prediction = ''

    """ Word abd sentence prediction below """

    def set_drag(self, boolDrag):
        return boolDrag
    

    def set_bool_word_pred(self, bool):
        return bool

    def set_bool_sentence_pred(self, bool):
        return bool
        
    def set_word_pred_num(self, num):
        self.wordPredNum = num
        return num

    def set_sentence_pred_num(self, num):
        self.sentencePredNum = num
        return num

    def set_word_pred_on_last_pressed_key(self, bool):
        return bool
    
    """ Word and sentence prediction above """
    """ Word prediction method below """

    def load_fill_word(self):
        self.fillWord = Model_Fill_Word()


    def load_bm25_word(self, option, k1, b, epsilon=None, delta=None):
        self.bm25Word = Model_Bm25(option, k1, b, epsilon, delta)

    
    def load_chatgpt_word(self, option, temperature):
        self.chatgptWord = Model_ChatGPT(option, None, "WORD_PRED", temperature)


    def load_bm25_sentence(self, option, k1, b, epsilon=None, delta=None):
        self.bm25Sentence = Model_Bm25(option, k1, b, epsilon, delta, boolEntryByKeywords=self.BOOL_ENTRY_BY_KEYWORDS)

    def load_semantic_sen_retrieval_sentence(self, model):
        self.semanticSenRetriSentence = Model_Semantic_Sentence_Retrieval(model, boolEntryByKeywords=self.BOOL_ENTRY_BY_KEYWORDS)
    

    def load_chatgpt_sentence(self, option, sentence_entry_approach, interaction_scenario, temperature):
        self.chatgptSentence = Model_ChatGPT(option, sentence_entry_approach, interaction_scenario, temperature)
        self.partnerSpeech = Model_Speech_Recognition()


    def conv_partner_speech_recognition_chatgpt(self):
        partnerInput = self.partnerSpeech.partnerSpeechInputRecognition()
        return partnerInput

    def add_conv_partner_input_to_history_for_dialogue(self, partnerInput):
        partnerInputGPT = f"B: {partnerInput}"
        self.chatgptSentence.record_conversation_history(partnerInputGPT)
        # self.conversation_history.append(partnerInput)
        # TODO: Add to word prediction dataset
        partnerInput = partnerInput + '\n'
        txt_path = './Dataset/sent_train_aac.txt'
        txt_path = os.path.join(os.path.dirname(__file__), txt_path)
        with open(txt_path, 'a') as file:
            file.write(partnerInput)
        file.close()

    
    def add_user_input_to_history_for_chatgpt(self, userInput):
        # when "Speak" button is clicked in KwickChat/chatgpt mode
        userInput = userInput.strip()
        userInputGPT = f"A: {userInput}"
        self.chatgptSentence.record_conversation_history(userInputGPT)
        
        # Add to word prediction dataset
        userInput = userInput + '\n'
        txt_path = './Dataset/sent_train_aac.txt'
        txt_path = os.path.join(os.path.dirname(__file__), txt_path)
        with open(txt_path, 'a') as file:
            file.write(userInput)
        file.close()

    def add_user_input_to_history_for_retrieval(self, userInput):
        # when "Speak" button is clicked, except chatgpt mode
        userInput = userInput.strip()
        userInput = userInput + '\n'
        txt_path = './Dataset/sent_train_aac.txt'
        txt_path = os.path.join(os.path.dirname(__file__), txt_path)
        with open(txt_path, 'a') as file:
            file.write(userInput)
        file.close()


    def make_word_prediction(self, entry):
        """ link to controller_main """
        predWords = []
        if 'WORD_BM25' in self.WORD_PRED_METHOD:
            predWords = self.bm25Word.predict_words(entry)
        elif 'WORD_CHATGPT' in self.WORD_PRED_METHOD:
            predWords = self.chatgptWord.generate_words(history=self.conversation_history, message=entry)

        predWordsInNum = self._get_required_num_of_pred(predWords, self.wordPredNum)
        print(f"pred method: {self.WORD_PRED_METHOD}, pred words: {predWordsInNum}")

        return predWordsInNum

    def make_initail_word_and_word_fill(self, entry):
        """ link to controller_main """
        filledWords = self.fillWord.predict_current_word(entry)
        predFilledWordsInNum = self._get_required_num_of_pred(filledWords, self.wordPredNum)
        return predFilledWordsInNum
    
    def _get_required_num_of_pred(self, predictions, num):
        predictionsInNum = []
        if len(predictions) > num:
            for i in range(num):
                predictionsInNum.append(predictions[i])
        else:
            for pred in predictions:
                predictionsInNum.append(pred)
        return predictionsInNum


    """ Word prediction method above """

    def make_sentence_prediction(self, entry):
        """ link to controller_main """
        predSentences = []
        if self.prediction_approach_SENTENCE_PREDICTION == 'Retrieval':
            # retrieve sentence every time the entry is updated. 
            if self.SENT_PRED_METHOD == 'SENTENCE_BM25OKAPI':
                predSentences = self.bm25Sentence.retrieve_sentences(entry)
            elif self.SENT_PRED_METHOD == 'SENTENCE_SEMANTIC_SIMILARITY':
                predSentences = self.semanticSenRetriSentence.retrieve_sentences(entry)
        elif self.prediction_approach_SENTENCE_PREDICTION == 'Generation':
            # generate sentence every time a word is typed. 
            if entry != '':
                if entry[-1] == ' ':
                    if self.SENT_PRED_METHOD == 'SENTENCE_CHATGPT':
                        # self.historyKwickchat = self.kwickchatSentence.adjust_history_size(self.historyKwickchat)
                        self.conversation_history = self.chatgptSentence.get_conversation_history()
                        predSentences = self.chatgptSentence.generate_sentences(history=self.conversation_history, message=entry)
        


        predSetencesInNum = self._get_required_num_of_pred(predSentences, self.sentencePredNum)
        
        print(f"pred method: {self.SENT_PRED_METHOD}, pred sentence: {predSetencesInNum}")
        
        return predSetencesInNum

    """ Sentence prediction method above """





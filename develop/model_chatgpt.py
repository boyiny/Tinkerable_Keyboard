import openai
import re
import ctypes

class Model_ChatGPT:

    def __init__(self, option, sentence_entry_approach, interaction_scenario, temperature) -> None:
        # print(f"ChatGPT option: {option}, sentence_entry_approach: {sentence_entry_approach}, interaction_scenario: {interaction_scenario}, temperature: {temperature}")
        openai.api_key = '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'
        self.OPTION = option
        self.SENTENCE_ENTRY_APPROACH = sentence_entry_approach
        self.INTERACTION_SCENARIO = interaction_scenario
        self.TEMPERATURE = temperature
        self.HISTORY_LENGTH = 60
        self.history = []
        # prompt = ""
        if sentence_entry_approach == "Left to right" and interaction_scenario == "Dialogue":
            self._assign_task_left_to_right_dialogue()
        elif sentence_entry_approach == "Left to right" and interaction_scenario == "Narrative":
            self._assign_task_left_to_right_narrative()
        elif sentence_entry_approach == "Keywords" and interaction_scenario == "Dialogue":
            self._assign_task_keywords_dialogue() 
        elif sentence_entry_approach == "Keywords" and interaction_scenario == "Narrative": 
            self._assign_task_keywords_narrative()
        elif interaction_scenario == "WORD_PRED":
            self._assign_task_word_pred()
        else:
            print("Please specify the sentence entry approach and interaction scenario") 

    def _assign_task_word_pred(self):
        history = ""
        message = ""
        prompt = f"Predict the next word based on the entry and conversation history. Example: System input: ['A: How are you doing today? ', 'B: Good. What about you?']. Sentence that replies to B to be complete: 'I am'. System output: 'great'."
        text = self.generate_words(history, message, prompt)
        # print("AI: "+ text[0])


    def _assign_task_left_to_right_dialogue(self):
        # prompt = "You are helping a non-speaking user with motor disabilities, to generate sentences in a conversation. The user will construct a sentence by typing words from left to right, indicated by 'A: '. The conversation partner will reply, indicated by 'B: '. Then the conversation continues. You are helping me to complete the sentence indicated by 'B: ' based on the words I have typed, as well as the conversation history. These sentence predictions need to follow the social rules and make sense in the whole conversation. ### Example: I type 'A: How are'. You are expected to compplese this sentence, for example, 'A: How are you?'. The conversation partner may reply 'B: I am good. How are you?'. I will type 'A: I am good. I am'. You need to complete this sentence. For example, 'A: I am good. I am using AI to help me type.'. Try to make the conversation continue.' ### Please reply 'yes' if you understand this task."
        history = ""
        message = ""
        prompt = f"Complete the sentence based on the conversation history. Example: System input: History: ['A: How are you doing today?', 'B: Good. How about you?']. Sentence that replies to B to be completed: 'I am'. System output: 'I am doing well, thank you.'"
        text = self.generate_sentences(history, message, prompt)
        # print("AI: "+text[0])

    def _assign_task_left_to_right_narrative(self):
        history = ""
        message = ""
        prompt = f"Complete the sentence based on the conversation history. Example: System input: History: ['A: I am a researcher at university.']. Sentence to be completed: 'My research'. System output: 'My research focuses on human-AI interaction.'"
        text = self.generate_sentences(history, message, prompt)
        # print("AI: "+text[0])

    def _assign_task_keywords_dialogue(self):
        history = ""
        message = ""
        prompt = "Generate a sentence based on the conversation history and the given keywords. Example: System input: History: ['A: Do you have plans after work today?', 'B: I don't have plans yet. What about you?']. Keywords for replying B: ['movies', 'tonight', 'join']. System out put: 'I am going to watch movies tonight. Do you wanna join me?'"
        text = self.generate_sentences(history, message, prompt)
        # print("AI: "+text[0])

    def _assign_task_keywords_narrative(self):
        history = ""
        message = ""
        prompt = f"Infer a sentence based on the conversation history and the given keywords. Example: System input: History: ['A: I am not feeling well.'] Keywords for generating the sentence: ['stomachache', 'morning']. System output: 'I have had a stomachache since this morning.'"
        text = self.generate_sentences(history, message, prompt)
        # print("AI: "+text[0])

    # def _assign_task(self, prompt):
    #     # self.dialogue = Model_ChatGPT()
    #     history = ""
    #     prompt = "You are helping a non-speaking individual with motor disabilities to generate sentences in a conversation. The conversation partner will send a message, indicated by 'A: ', then I will type keywords, indicated by 'B: '. Generate a full response using the keywords indicated by 'B: '. These sentence predictions need to follow the social rules and make sense in the whole conversation. ### Example: 'A: what do you do?' 'B: student medical cambridge' You are expected to generate 'I am a medical student in Cambridge.' ### Please reply 'yes' if you understand this task."

    #     text = self.generate_sentence_keyword_based(prompt)
    #     print("Developer talking to AI: "+prompt)
    #     print("AI: "+text.choices[0].text.strip())

    def record_conversation_history(self, new_message):
        self.history.append(new_message)
        return self.history
    
    def get_conversation_history(self):
        return self.history

    def clean_generated_sentence_list(self, old_list, message):
        new_list = []
        for sen in old_list:
            if '\n' in sen:
                sen = sen[0:sen.find('\n')]
            if sen.startswith('A:') or sen.startswith('B:'):
                sen = sen[2:].strip()
            if 'B:' in sen and sen.startswith('B:') == False:
                sen = sen[0:sen.find('B:')]
            sen = sen.translate({ord('_'):None})
            sen = sen.translate({ord('"'):None})
            if len(new_list) == 0:
                new_list.append(sen)
            elif len(new_list)>0 and len(new_list)<4:
                if sen in new_list:
                    pass
                else:
                    new_list.append(sen)
        
        if self.SENTENCE_ENTRY_APPROACH == "Left to right":
            temp_list = new_list
            new_list = []
            for sentence in temp_list:
                message = message.strip()
                if message.lower() != sentence[0:len(message)].lower():
                    sentence = message + ' ' + sentence
                    sentence = re.sub(' +', ' ', sentence)
                    new_list.append(sentence)
        return new_list
    
    def clean_generated_word_list(self, old_string):
        if old_string.count('\n') > 1:
            old_list = old_string.split('\n')
        else: 
            old_list = old_string.split(', ')
        new_list = []

        for word in old_list:
            # word = re.sub('\W+', '', word)
            word = word.translate({ord('_'):None})
            word = word.translate({ord('"'):None})
            word = word.translate({ord(','):None})
            word = word.translate({ord('.'):None})
            word = word.lower()
            word = re.sub(r'[\d]+', '', word).strip()

            if len(new_list) == 0:
                new_list.append(word)
            elif len(new_list)>0 and len(new_list)<7:
                if word in new_list:
                    pass
                else:
                    new_list.append(word)
        return new_list

    def pop_up_chatgpt_error_notification(self):
        ctypes.windll.user32.MessageBoxW(0, "ChatGPT server has reached the capacity, please try this function later.", "Info", 0)

    def generate_sentences(self, history, message, prompt=None):
        message = re.sub(' +', ' ', message)
        # print(message)
        if prompt == None:
            if self.SENTENCE_ENTRY_APPROACH == "Left to right" and self.INTERACTION_SCENARIO == "Dialogue":
                prompt = f"Complete the sentence based on the conversation history: {history}. Sentence to be completed: '{message}'. Continue the sentence and do not repeat '{message}'."
            elif self.SENTENCE_ENTRY_APPROACH == "Left to right" and self.INTERACTION_SCENARIO == "Narrative":
                prompt = f"Complete the sentence based on the text input history: {history}. Sentence to be completed: '{message}'. Continue the sentence and do not repeat '{message}'."
            elif self.SENTENCE_ENTRY_APPROACH == "Keywords" and self.INTERACTION_SCENARIO == "Dialogue":
                prompt = f"Generate a sentence based on the conversation history: {history}. Keywords for generating the sentence: {message}. Do not repeat history infomation in the new sentence. Keep the new sentence simple."
            else:
                # self.SENTENCE_ENTRY_APPROACH == "Keywords" and self.INTERACTION_SCENARIO == "Narrative":
                prompt = f"Infer the next sentence based on the narrative history: {history}. Keywords for generating the sentence: {message}. Do not repeat history infomation in the new sentence. Keep the new sentence simple."
        
        genSentenceList = []
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                n=8,
                stop=None,
                temperature=self.TEMPERATURE,
                max_tokens=200
            )

            i = 0
            
            for choice in response.choices:
                # print("AI - "+ str(i) + ": " + choice.text.strip())
                genSentenceList.append(choice.text.strip())
                i+=1
            genSentenceList = self.clean_generated_sentence_list(genSentenceList, message)

            



        except openai.error.RateLimitError:
            response = openai.Completion.create(
                engine='text-davinci-001',
                prompt=prompt,
                n=8,
                stop=None,
                temperature=self.TEMPERATURE,
                max_tokens=200
            )

            i = 0
            for choice in response.choices:
                # print("AI - "+ str(i) + ": " + choice.text.strip())
                genSentenceList.append(choice.text.strip())
                i+=1
            genSentenceList = self.clean_generated_sentence_list(genSentenceList)

        except openai.error.RateLimitError:
            self.pop_up_chatgpt_error_notification()

        return genSentenceList
    

    def generate_words(self, history, message, prompt=None):
        
        prompt = f"Predict the next word based on the conversation history: {history}. Sentence to be complete: {message}. Make six next word predictions. Each prediction contains one word: "
        
        genWordList = []
        try: 
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                n=1,
                stop=None,
                temperature=self.TEMPERATURE,
                max_tokens=100
            )
            i = 0
            
            if len(response.choices) > 0:
                genWordList = self.clean_generated_word_list(response.choices[0].text.strip())
            else:
                # print("No word predictions")
                pass
            # print(genWordList)

        except openai.error.RateLimitError:
            response = openai.Completion.create(
                engine='text-davinci-001',
                prompt=prompt,
                n=1,
                stop=None,
                temperature=self.TEMPERATURE,
                max_tokens=200
            )
            i = 0
            if len(response.choices) > 0:
                genWordList = self.clean_generated_word_list(response.choices[0].text.strip())
            else:
                # print("No word predictions")
                pass
            # print(genWordList)

        except openai.error.RateLimitError:
            self.pop_up_chatgpt_error_notification()

        
        return genWordList


if __name__ == '__main__':
    # dialogue = Model_ChatGPT(option="WORD_CHATGPT", sentence_entry_approach="Left to right", interaction_scenario="WORD_PRED", temperature=0.9)
    dialogue = Model_ChatGPT(option="WORD_CHATGPT", sentence_entry_approach="Left to right", interaction_scenario="Narrative", temperature=0.5)

    history = []
    l2r = True
    
    # Word pred
    # while True:
    #     a_message = ""
    #     while True:
    #         temp = input(f"A: {a_message}")
    #         a_message = a_message + temp + " "
    #         print(a_message)
    #         if a_message.lower() == 'exit':
    #             break
    #         genWordList = dialogue.generate_words(history, a_message)
    #         i = 0
    #         for word in genWordList:
    #             print("AI - "+ str(i) + ": " + word)
    #             i+=1
    #         select = int(input("Select: "))
    #         if select > 3:
    #             continue
    #         else: 
    #             selectResponce = genWordList[select]
    #             print("Selected: "+selectResponce)
    #             history.append(f"A: {a_message + ' ' + selectResponce}")
    #             break

    #     b_message = input("B: ")
    #     history.append(f"B: {b_message}")
    #     print("History: ")
    #     print(history)
    #     if len(history) > 60: # self.HISTORY_LENGTH
    #         history.pop(0)



    # # Dialogue
    # while True:
    #     a_message = ""
    #     while True: 
    #         temp = input(f"A: {a_message}")
    #         a_message = a_message + temp + " "
    #         print(a_message)
    #         if a_message.lower() == 'exit':
    #             break
            
    #         genSentenceList = dialogue.generate_sentences(history, a_message) 
    #         i = 0
    #         for sen in genSentenceList:
    #             print("AI - "+ str(i) + ": " + sen)
    #             i+=1
    #         select = int(input("Select: "))
    #         if select > 3:
    #             continue
    #         else: 
    #             selectResponce = genSentenceList[select]
    #             print("Selected: "+selectResponce)
    #             history.append(f"A: {selectResponce}")
    #             break

    #     b_message = input("B: ")
    #     history.append(f"B: {b_message}")
    #     if len(history) > 5: # self.HISTORY_LENGTH
    #         history.pop(0)



    # Narrative
    while True:
        message = ""
        while True: 
            temp = input(f"Keywords: {message}")
            message = message + temp + " "
            print(message)
            if message.lower() == 'exit':
                break
            # prompt = f"Complete the sentence based on the conversation history: {history}. Sentence to be completed: {a_message}. "
            
            genSentenceList = dialogue.generate_sentences(history, message) 
            i = 0
            for sen in genSentenceList:
                print("AI - "+ str(i) + ": " + sen)
                i+=1
            select = input("Select: ")
            if select.isdigit():
                select = int(select)
            else:
                break
            if select > 3:
                continue
            else: 
                selectResponce = genSentenceList[select]
                print("Selected: "+selectResponce)
                history.append(f"{selectResponce}")
                break

        if len(history) > 5: # self.HISTORY_LENGTH
            history.pop(0)




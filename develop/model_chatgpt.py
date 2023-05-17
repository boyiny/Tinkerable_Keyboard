import openai

class Model_ChatGPT:

    def __init__(self) -> None:
        openai.api_key = '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'
        self._assign_task()
        
    def _assign_task(self):
        self.dialogue = Model_ChatGPT()
        prompt = "You are helping a non-speaking individual with motor disabilities to generate sentences in a conversation. The conversation partner will send a message, indicated by 'A: ', then I will type keywords, indicated by 'B: '. Generate a full response using the keywords indicated by 'B: '. These sentence predictions need to follow the social rules and make sense in the whole conversation. ### Example: 'A: what do you do?' 'B: student medical cambridge' You are expected to generate 'I am a medical student in Cambridge.' ### Please reply 'yes' if you understand this task."
        text = dialogue.generate_sentence_keyword_based(prompt)
        print("AI: "+text.choices[0].text.strip())

    def generate_sentence_keyword_based(self, prompt):
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            n=4,
            stop=None,
            temperature=0.5,
            max_tokens=40
        )
        return response

if __name__ == '__main__':
    dialogue = Model_ChatGPT()
    prompt = "You are helping a non-speaking individual with motor disabilities to generate sentences in a conversation. The conversation partner will send a message, indicated by 'A: ', then I will type keywords, indicated by 'B: '. Generate a full response using the keywords indicated by 'B: '. These sentence predictions need to follow the social rules and make sense in the whole conversation. ### Example: 'A: what do you do?' 'B: student medical cambridge' You are expected to generate 'I am a medical student in Cambridge.' ### Please reply 'yes' if you understand this task."
    text = dialogue.generate_sentence_keyword_based(prompt)
    print("AI: "+text.choices[0].text.strip())

    while True:
        a_message = input("A: ")
        if a_message.lower() == 'exit':
            break
        b_message = input("B: ")
        prompt = f"{a_message} {b_message}"
        response = dialogue.generate_sentence_keyword_based(prompt)
        i = 0
        for choice in response.choices:
            print("AI - "+ str(i) + ": " + choice.text.strip())
            i+=1
        select = int(input("Select: "))
        selectResponce = response.choices[select].text.strip()
        print("Selected: "+selectResponce)



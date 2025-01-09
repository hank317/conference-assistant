import os
os.environ['API_KEY'] = 'sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # your api_key

from conference_assistant.assistant import LLMAssistant

# Assistant Settings.
firm = 'NewBie NLP' # Your company's name, suggested full name.
instruction = '' # Some custom instructions are used to optimize the reply effect of the assistant.
model = 'qwen-max'

# Conference Information.
file_path = ['./conference_assistant/data/agenda_example.xlsx'] # Replace with your file path.
        
# Create Conference Assistant.
my_assistant = LLMAssistant(firm, instruction, file_path, model)

# print(my_assistant.conference_info())

# Start a Conversation.
session_id = '2025-01-08-002'
query = 'Who will report first in the afternoon'
stream = True
rounds = 3

answer = ''
for chunk in my_assistant.chat(session_id, query, stream, rounds):
    answer += chunk
print('answer:', answer)

# Retrieve historical conversation information based on session ID.
print(my_assistant.history_info(session_id))

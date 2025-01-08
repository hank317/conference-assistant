# conference-assistant
A conference assistant based on the LLMs, which can be used for various types of conferences such as company annual meetings and academic conferences. It is very easy to use, just provide the meeting documents.

## ✨ create your exclusive conference assistant ✨ 
You need to specify the name of the company, school, or organization, and you can also add some instructions to restrict or optimize the assistant's responses.  
You need to provide additional conference documents, and the assistant will learn and answer based on the content of these documents.  
In addition, you need to specify the large language model used by the assistant. We follow the OpenAI SDK, and currently support the following models: qwen、kimi、spark. 
If there are many documents, it is recommended to use a model that supports longer context input.
Details are as follows:  
```python 
from assistant import LLMAssistant

# Assistant Settings.
firm = '中信国安实业集团有限公司' # Your company's name, suggested full name.
instruction = '' # Some custom instructions are used to optimize the reply effect of the assistant.
model = 'qwen-max'

# Conference Information.
file_path = ['./data/agenda_example.xlsx'] # Replace with your file path.
        
# Create Conference Assistant.
# 通义千问：qwen-max，qwen-plus；讯飞星火：generalv3.5；kimi：moonshot-v1-8k，moonshot-v1-32k
my_assistant = LLMAssistant(firm=firm, instruction=instrction, file_path=file_path, model=model)
```
## ✨ start chatting with your assistant ✨ 
Before starting a chat, you need to create a session ID to manage session information, as shown below:  
```python 
# Start a Chat.
session_id = '20250108001'
query = '你叫什么名字？'

answer = ''
for chunk in my_assistant.chat(session_id, query):
    answer += chunk
print('answer:', answer)

# Retrieve historical conversation information based on session ID.
print(my_assistant.history_info(session_id))
```
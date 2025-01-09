# Conference Assistant ![Static Badge](https://img.shields.io/badge/Apache-2.0-green) ![Static Badge](https://img.shields.io/badge/NewBie-NLP-blue)  
![project_logo](./images/conference_assistant_logo.png)  
[English](README.md) | [中文](./README_zh.md)
基于大语言模型（LLMs）的会议助手，适用于公司年会、学术研讨会等多种类型的会议。该助手使用非常简便，仅需提供会议相关文档即可启动服务。  
包括但不限于以下用途：
- 会议基本信息
- 具体议程安排
- 酒店与行程预订
- 其他注意事项
## 🤖 创建助手  
You need to specify the name of the company, school, or organization, and you can also add some instructions to restrict or optimize the assistant's responses.   
```python 
from assistant import LLMAssistant

# Assistant Settings.
firm = '中信国安实业集团有限公司' 
instruction = '' 
model = 'qwen-max'

# Conference Information.
file_path = ['./data/agenda_example.xlsx'] 
        
# Create Conference Assistant.
my_assistant = LLMAssistant(firm=firm, instruction=instrction, file_path=file_path, model=model)
```  
You need to specify the large language model used by the assistant. We follow the OpenAI SDK, and currently support the following models: qwen、kimi、spark. If there are many documents, it is recommended to use a model that supports longer context input.  
```python
# Add your api_key to the environment variables.
import os
os.environ['API_KEY'] = 'sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Support the following models:
# qwen: qwen-plus, qwen-max  
# kimi: moonshot-v1-8k, moonshot-v1-32k  
# spark: generalv3.5  
``` 
You need to provide additional conference documents, and the assistant will learn and answer based on the content of these documents. We currently support a variety of file formats, including *.doc*, *.docx*, *.xls*, *.xlsx*, *.txt*, *.csv*, *.tsv*, and more. However, we recommend using <mark>*.xlsx*</mark> or <mark>*.csv*</mark> formats for optimal results.   
## 💫 快速开始  
Quickly initiate chat, support streaming and non streaming, default streaming.
```python 
# Start a Chat.
query = '你叫什么名字？'
stream = False

answer = ''
for chunk in my_assistant.single_chat(query=query, stream=stream):
    answer += chunk
print('answer:', answer)
```
## 💥 对话增强  
By combining historical session information, the assistant can fully understand each query and answer more accurately.  
When chatting, you need to specify a session ID to manage session information and specify the session rounds that the assistant should consider when answering.
```python 
# Start a Chat.
query = '你叫什么名字？'
stream = True
rounds = 3

answer = ''
for chunk in my_assistant.chat(query=query, stream=stream, rounds=rounds):
    answer += chunk
print('answer:', answer)
```
Multiple rounds of session require middleware to store and manage session information. Please change your Redis configuration in the <mark>*config.py*</mark> as shown below:      
```python  
redis_config = {
    'host':'127.0.0.1',
    'port':'7001',
    'password':'xxxxxxxxx'
}
```
## 🤝 个性化定制
You can also explore additional customized developments triggered through natural language. If you have any needs in this area, please feel welcome to contact us:  
- 📬 : zhenhu317@gmail.com  
## 🏷 许可
Conference Assistant is licensed under the [Apache-2.0 License](./LICENSE). 
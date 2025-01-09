import os
os.environ['API_KEY'] = 'sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # 你的api_key

from conference_assistant.assistant import LLMAssistant

# 基本配置
firm = 'NewBie NLP' # 公司或者组织名称
instruction = '' # 个性化指令
model = 'qwen-max'

# 录入会议信息
file_path = ['./conference_assistant/data/agenda_example.xlsx'] # 替换文件路径
        
# 实例化助手
my_assistant = LLMAssistant(firm, instruction, file_path, model)

# print(my_assistant.conference_info())

# 开始对话
session_id = '2025-01-08-002'
query = '什么时候茶歇？'
stream = True
rounds = 3

answer = ''
for chunk in my_assistant.chat(session_id, query, stream, rounds):
    answer += chunk
print('answer:', answer)

# 查看会话历史
print(my_assistant.history_info(session_id))

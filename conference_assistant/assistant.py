import os
import json
from openai import OpenAI
from typing import Dict, List, Optional, Iterator

from conference_assistant.history_management import set_history, get_history
from conference_assistant.conference_loading import get_file


QUERY_PROMPT_ZH = """
## 角色
你是一名专业的问题改写专家，你需要结合用户和智能助手的历史对话信息，对用户当前的问题进行改写。

## 要求
1.改写后的问题要清晰易懂，你不能改变问题的原意。
2.你只需要重新表述用户问题，禁止生成其他内容。

## 用户的历史对话信息为：
{history_content}
当前用户的问题是：{query}，请你严格按照要求进行改写，改写后的问题为：
"""
ROLE_PROMPT_ZH = """你是{firm}的会议助手，负责根据已知的会议信息回答问题。\n"""

CONFERENCE_PROMPT_ZH = """\n\n会议信息如下：\n"""

        
class LLMAssistant():
    def __init__(self, 
                 firm:str,
                 instruction:str,  
                 file_path:list[str],
                 model:str):
        """Assistant class, used to instantiated specific conference assistants.

        Args:
            firm (str): Your firm name.
            instruction (str): Instructions to the assistant, such as requesting the format and style of the assistant's response.
            file_path (list[str]): List of file pathes containing conference information.
            model (str): The model name you want to use, please refer to the readme for details.
        """
        if not firm:
            firm = '公司'
        self.file = get_file(file_path)
        self.system_prompt = ROLE_PROMPT_ZH.format(firm=firm) + instruction + CONFERENCE_PROMPT_ZH + self.file
        self.model = model
        self.client = None
        if self.model.startswith('qwen'):
            self.client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        elif self.model.startswith('general'):
            self.client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url='https://spark-api-open.xf-yun.com/v1',
        )
        elif self.model.startswith('moonshot'):
            self.client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url='https://api.moonshot.cn/v1',
        )
        elif self.model.startswith('doubao'):
            self.client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url='https://ark.cn-beijing.volces.com/api/v3/',
        )
        
    
    def single_chat(self, query:str, stream:Optional[bool] = True):
        """Single round conversation, without using historical conversation information, fast speed.

        Args:
            query (str): User query.
            stream (Optional[bool], optional): Whether to enable streaming response. Defaults to True.
            
        """
        print('query:', query)
        messages = [
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': query}
                ]
        if stream:
            return self._chat_stream('', query, messages)
        else:
            return self._chat_no_stream('', query, messages)
           
 
    def chat(self, session_id:str, query:str, stream:Optional[bool] = True, rounds:Optional[int] = 3):
        """Conference assistant dialogue function, combined with historical conversation management and problem rewriting, to achieve replies.

        Args:
            session_id (str): ID used to manage session history.
            query (str): User query.
            stream (Optional[bool], optional): Whether to enable streaming response. Defaults to True.
            rounds (Optional[int], optional): Required historical dialogue length. Defaults to 3.

        """
        new_query = query
        if rounds > 0:
            history = get_history(session_id, rounds)
            new_query = self._query_enhance(query, history)
        print('query:', query)
        print('new_query:', new_query)
        messages = [
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': new_query}
                ]
        if stream:
            return self._chat_stream(session_id, query, messages)
        else:
            return self._chat_no_stream(session_id, query, messages)
            
    
    def _chat_stream(self, session_id:str, query:str, messages:Optional[List[Dict]] = None) -> Iterator[str]:
        """LLM streaming dialogue

        Args:
            session_id (str): ID used to manage session history.
            query (str): User query.
            messages (Optional[List[Dict]], optional): Messages list. Defaults to None.

        Yields:
            Iterator[str]: Streaming Content.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            full_content = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_content += chunk.choices[0].delta.content
                    yield chunk.choices[0].delta.content
            if session_id and full_content:
                set_history(session_id, query, full_content)
        except Exception as e:
            yield f"error: {e}"
        
    
    def _chat_no_stream(self, session_id:str, query:str, messages:Optional[List[Dict]] = None) -> Iterator[str]:
        """LLM no streaming dialogue

        Args:
            session_id (str): ID used to manage session history.
            query (str): User query.
            messages (Optional[List[Dict]], optional): Messages list. Defaults to None.

        Yields:
            Iterator[str]: No streaming Content.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            answer = completion.choices[0].message.content
            yield answer
            if session_id:
                set_history(session_id, query, answer)
        except Exception as e:
            yield f"error: {e}"
            
            
    def _query_enhance(self, query:str, history:list) -> str:
        """Rewrite the query, eliminate ambiguity, and fill in gaps.

        Args:
            query (str): User query.
            history (list): Dialogue history information.

        Returns:
            str: New query.
        """
        if not history:
            return query
        
        history_content = ''
        
        for info in history:
            info = json.loads(info)
            user_info = '用户：' + info.get('query') + '\n'
            assistant_info = '智能助手：' + info.get('answer') + '\n'
            history_content += user_info + assistant_info
        # print('session history: \n', history_content)
                
        content = QUERY_PROMPT_ZH.format(history_content=history_content, query=query)
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'user', 'content': content}
                ],
                stream=False
            )
            return completion.choices[0].message.content
        except Exception as e:
            return query
        
    
    def conference_info(self) -> str:
        """All conference information used by the assistant.

        Returns:
            str: conference information
        """
        return self.file
    
    
    def history_info(self, session_id:str) -> list[dict]:
        """Query the historical conversation information of the current session.

        Args:
            session_id (str): The ID of the session that needs to be queried.

        Returns:
            list[dict]: Recent 10 rounds of conversation information
        """
        history = get_history(session_id, 10) 
        all_info = list()
        for info in history:
            info = json.loads(info)
            all_info.append(info)
        return all_info
    
    
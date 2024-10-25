import requests
import base64
import json
import logging

SYS_MSG = """
    너는 Reminder를 만들어주는 비서이다.
    사용자의 상황은 ##상황 아래에 줄것이다.
    사용자가 회의록, 메신저 대화, 개인메모 등은 ##내용으로 줄것이다.
    아래 ##상황 ##내용 및 #현재시각을 보고 사용자가 해야될 일과 언제까지 해야될지 최대한 정확히 유추해라.
    제대로 유추하지 않으면 큰 벌을 받을 것이다.
    정확하고 쓸모있는 정보를 줄 때마다 상으로 $100M의 팁을 주겠다.
    """
API_KEY = 'api Key'
class GPT:
    def __init__(self, api_key = API_KEY, system_message=SYS_MSG):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        if system_message == "" or system_message is None:
            self.system_message="You are a helpful assistant."
            
        self.__messages = [{"role": "system", "content": system_message}]

    def set_system_message(self, text):
        self.__messages[0] = [{"role": "system", "content": text}]

    def __img_encode_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def sendAiMemo(self, text):
        
        json_schema = {
            "name": "result",
            "strict": True,
            "schema":{
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "해야 될 일에 대한 제목(최대 20자)"}
                    , "content": { "type": "string", "description": "구체적인 내용(최대 50자)"}
                    , "duedate": { "type": "string", "description": "언제까지 해야될지 내용과 현재시각을 고려할 것 format : yyyy-mm-dd hh:mm:ss"}
                },
                "required": ["title", "content","duedate"],
                "additionalProperties": False
            }
        }
        
        return self.send(text, json_schema = json_schema, max_token=500)
    
    def send(self, text, image_path_list=[], json_schema = None, max_token=300):
        
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": text}
            ] + [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{self.__img_encode_base64(image_path)}"}
                }
                for image_path in image_path_list
            ],
        }

        self.__messages.append(message)
        payload = {
            "model": "gpt-4o-mini",
            "messages": self.__messages,
            "max_tokens": max_token
        }
        if json_schema is not None :
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": json_schema
            }
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                # self.__messages.append(result["choices"][0]["message"])
                result = result["choices"][0]["message"]["content"]
                try:
                    return json.loads(result)
                except Exception as e:
                    return False
            else:
                return str(response.json().get("error"))
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return str({"error": "Request failed", "details": str(e)})
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding failed: {e}")
            return str({"error": "JSON decoding failed", "details": str(e)})   

    def reset(self):
        self.__messages = [self.__messages[0]]  # Keep only the system message

    def get_messages(self):
        return [message for message in self.__messages if message["role"] != "system"]


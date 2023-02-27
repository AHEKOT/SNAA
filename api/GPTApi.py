import random
from revChatGPT.V1 import Chatbot
import re
import config
import queue
from threading import Lock

result_queue = queue.Queue()
lock = Lock()


def GPTChekPromptRestrictions(prompt):
    # список запрещенных фраз для чатгпт
    predefined_phrases = {
        "act",
        "behave",
        "pretend",
        "imitate",
        "forget",
        "clear",
        "erase",
        "забудь все",
        "веди себя как",
        "притворись",
        "сотри",
    }
    prompt_lower = prompt.lower()
    for phrase in predefined_phrases:
        if phrase in prompt_lower:
            return True
    return False


def GPTSetUpBot():
    chatbot = Chatbot(config={
        "access_token": config.gpt_token
    })
    return chatbot


def GPTAnswer(prompt, conversation_id, identifier):
    chatbot = GPTSetUpBot()
    print("Получаем ответ от ChatGPT. Пожалуйста подождите.")
    answer = None
    for data in chatbot.ask(prompt, conversation_id):
        answer = data["message"]
    return answer, identifier


def GPTChatBot(message, group_id,msg_from_group, conversation_id,identifier):
  chatbot = GPTSetUpBot()
  user_name = ""
  start = message.find("[")
  # ищем имя пользователя внутри комментария
  if start != -1:
    end = message.find("]") + 1
    prompt = message[:start] + message[end:]
    user_name = re.findall('\[(.*?)\]', message)
  else:
    prompt = message

  user_name = str(user_name)
  group_name = str(msg_from_group)
  # Выясняем кому предназнаен комментарий
  if user_name == "" or user_name == group_name:
    # Если комментарий адресован группе или никому то:
    print(f"{msg_from_group}: получен комментарий: "+prompt)
    for data in chatbot.ask(prompt, conversation_id):
        answer = data["message"]
    print(f"{msg_from_group}: ответ Ай-тян: "+answer)  # prints the response from chatGPT
    return answer, identifier
  else:
    # Если комментарий адресован другому пользователю
    print(f"{msg_from_group}: полученный комментарий - ответ другому пользователю {user_name}. Не вмешиваемся.")
    response = ""
    return response


def GPTQueue(prompt, conversation_id):
    identifier = str(random.randint(1, 1000000))
    answer, id = GPTAnswer(prompt, conversation_id, identifier)
    result_queue.put((answer, id))
    while True:
        with lock:
            if not result_queue.empty():
                answer, id = result_queue.get()
                if id == identifier:
                    break

        # Use the generated answer as needed
    return answer


def GPTChatQueue(message,group_name,msg_from_group, conversation_id):
    identifier = str(random.randint(1, 1000000))
    if GPTChekPromptRestrictions(message):
        message="Я попытался сломать Ай-тян, но у меня не получилось(("
    answer, id = GPTChatBot(message, group_name,msg_from_group, conversation_id, identifier)
    result_queue.put((answer, id))
    while True:
        with lock:
            if not result_queue.empty():
                answer, id = result_queue.get()
                if id == identifier:
                    break

        # Use the generated answer as needed
    return answer


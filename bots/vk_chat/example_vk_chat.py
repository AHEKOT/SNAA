import os

try:
    import replit
    import sys
    import inspect
    currentdir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
    parentdir = os.path.dirname(parentdir)
    sys.path.insert(0, parentdir)
except ImportError:
    print()

from api.VKApi import VKChatBotCommentsParser, VKChatBotSetUp

bot_type = "chat_bot" #проверка типа бота. Не изменять.

#---------------------БЛОК-НАСТРОЕК------------------------------
group_id = "123456789"                          # айди группы вк
access_token = os.environ['VKChat_217691628']   # токен для longpoll сервера группы с правом писать комментарии на стене
group_name="название группы вконтакте"          # полное название группы (обязательно для работы ответов на комментарии группы)
#---------------------БЛОК-НАСТРОЕК------------------------------

print(f"ЧатБот для группы {group_name} загружен!")
club_id="club"+group_id
msg_from_group=f"['{club_id}|{group_name}']"

longpoll_server, longpoll_key, longpoll_ts = VKChatBotSetUp(group_id,group_name)
VKChatBotCommentsParser(longpoll_server, longpoll_key, longpoll_ts, access_token, group_id, msg_from_group)

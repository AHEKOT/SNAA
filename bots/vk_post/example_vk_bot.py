import os
import schedule
import time
import datetime

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

import config
from uploaders.uploadtovk import vk_upload

bot_type = "vk_bot" #проверка типа бота. Не изменять.

#---------------------------------------------БЛОК-НАСТРОЕК---------------------------------------------
img_count = 4                                               # количество картинок в посте. Не больше 10.
vk_group_id = "123456789"                                   # айди группы Вконтакте
vk_group_name = "Группа ВК"                                 # имя группы отображается в консоли и уведомлениях
vk_posting_type = "Random"                                  # метод публикации изображений ("Random" - изображения выбираются случайно из общей папки. "Subfolder" - публикуются все изображения из подкаталогов по порядку
disk_folder_id = "/папка_на_яндекс_диске"                   # папка на яндекс диске начиная с корняvk_message_prompt = "Текст поста Вконтакте. Например список тегов #Хештег1 #Хештег2" # можно оставить пустым. Если включен режим ChatGPT то работает как промпт. Например "Напиши креативное название для поста в соцсети".
vk_message_prompt = "Текст поста Вконтакте. "               # можно оставить пустым. Если включен режим ChatGPT то работает как промпт. Например "Напиши креативное название для поста в соцсети".
conversation_id = "20466e88-a7ea-4f21-8c68-14bc50b21936"    # айди диалога в ChatGPT. Можно оставить "default" тогда значение будет браться из файла config.py
notifications = True                                        # включение оповещений в личном сообщении от группы
timers = ["12:00:00", "13:00:00", "14:00:00"]               # время загрузки постов через запятую
#---------------------------------------------БЛОК-НАСТРОЕК---------------------------------------------


def run():
  print("ВК бот для паблика "+vk_group_name+" запущен по таймеру.")
  vk_upload(img_count,vk_group_id,vk_group_name,vk_posting_type,disk_folder_id,vk_message_prompt,conversation_id,notifications)
  return

for t in timers:
    timer = datetime.datetime.strptime(t, "%H:%M:%S")
    new_time = (timer + datetime.timedelta(hours=config.delta)).strftime("%H:%M:%S")
    schedule.every().day.at(new_time).do(run)

print("ВК бот для паблика "+vk_group_name+" загружен.")
print("Время запуска установлено на: "+str(timers))
#run()
while True:
  schedule.run_pending()
  time.sleep(1)

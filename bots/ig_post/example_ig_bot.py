import os
import schedule
import time
import datetime
from uploaders.uploadtoig import UploadToIG

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

bot_type = "ig_bot" #проверка типа бота. Не изменять.

#---------------------БЛОК-НАСТРОЕК------------------------------
img_count = 1                                   # количество картинок. Каждая постится отдельно
ig_name = 'ig_username'                         # имя вашего инстаграм канала
ig_password = os.environ['IG_testaichan']       # пароль инстаграм канала
disk_folder_id = "/каталог на яндекс диске"     # папка на яндекс диске начиная с корня
caption="текст поста с #хештегами"              # текст под картинкой. Можно использовать список хештегов
timers = ["12:00:00", "13:00:00", "14:00:00"]   # время загрузки постов через запятую
#---------------------БЛОК-НАСТРОЕК------------------------------

def run():
  print("Инстаграм бот для канала "+ig_name+" запущен по таймеру.")
  UploadToIG(img_count, ig_name, ig_password, disk_folder_id,caption)
  return

for t in timers:
    timer = datetime.datetime.strptime(t, "%H:%M:%S")
    new_time = (timer + datetime.timedelta(hours=config.delta)).strftime("%H:%M:%S")
    schedule.every().day.at(new_time).do(run)
run()
print("Телеграм бот для канала "+ig_name+" загружен")
print("Время запуска установлено на: "+str(timers))

while True:
  schedule.run_pending()
  time.sleep(1)

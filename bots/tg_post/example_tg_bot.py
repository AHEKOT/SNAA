import os
import schedule
import time
import asyncio
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
from uploaders.uploadtotg import tg_upload

bot_type = "tg_bot1" #проверка типа бота. Не изменять.

#---------------------БЛОК-НАСТРОЕК------------------------------
img_count = 4  #Количество картинок в посте. Не больше 10.
name = '@aichantestin'
disk_folder_id = "/Бот/Horny"  #папка на яндекс диске начиная с корня
post_text = "Текст для поста в телеграм" #можно оставить пустым
timers = ["12:00:00", "13:00:00", "14:00:00"] #время загрузки постов через запятую
#---------------------БЛОК-НАСТРОЕК------------------------------

def run():
  print("Телеграм бот для канала "+name+" запущен по таймеру.")
  asyncio.run(
    tg_upload(img_count, name, disk_folder_id, used_images,post_text))
  return

for t in timers:
    timer = datetime.datetime.strptime(t, "%H:%M:%S")
    new_time = (timer + datetime.timedelta(hours=config.delta)).strftime("%H:%M:%S")
    schedule.every().day.at(new_time).do(run)

print("Телеграм бот для канала "+name+" загружен")
print("Время запуска установлено на: "+str(timers))

while True:
  schedule.run_pending()
  time.sleep(1)

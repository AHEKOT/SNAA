import time
from StartUp import StartUpChekBots, StartUpTime, StartUpReplit
# SNAA - SocialNetworksAutoAdmin
# Version = 1.5.1
# modules - telegram, vkontakte, instagram, ChatGPT, YandexDisk

# Выводим текущее время на сервере
StartUpTime()

# Проверка запуска скрипта на Replit.com
StartUpReplit()

# Запуск ботов
StartUpChekBots()

print("Настройки заданы. Программа работает в фоновом режиме ожидания")
while True:
  time.sleep(100)

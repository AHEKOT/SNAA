from datetime import datetime
import time
import subprocess
import re
import os
import config


def StartUpTime():
    print("Скрипт запущен. Текущее время на сервере: ")
    print(str(datetime.now().time()))
    return 


def StartUpBots(path, bot_type):
  for file in os.listdir(path):
    if file.endswith(".py"):
      with open(f"{path}/{file}") as f:
        content = f.read()
        if re.search(f"bot_type = \"{bot_type}\"", content):
          subprocess.Popen(["python", f"{path}/{file}"])
          time.sleep(10)
  return


def StartUpChekBots():
    if config.use_vk_bot:
        StartUpBots(config.VK_path, "vk_bot")

    if config.use_tg_bot:
        StartUpBots(config.TG_path, "tg_bot")

    if config.use_GPT:
        if config.use_chat_bot:
            StartUpBots(config.chat_path, "chat_bot")

    if config.use_ig_bot:
        StartUpBots(config.IG_path, "ig_bot")

    return


def StartUpReplit():
    try:
        import replit
        print("Скрипт работает на серисе Replit.com")
        print("Запускам режим поддержки работоспособности")
        subprocess.Popen(["python", "ReplitMonitor.py"])
        time.sleep(5)
    except ImportError:
        return
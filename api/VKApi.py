import requests
import json
import random
import config
import time
from datetime import datetime

from api.GPTApi import GPTChatQueue


def VKNotifyNoImages(name,disk_folder_id,vk_group_id,available_images,img_count):
    # Если в каталоге недостаточно изображений для создания поста - отправляем уведомление личным сообщением
    if (len(available_images)) < img_count:
        random_id = random.randint(1, 2 ** 63 - 1)
        vk_message_text = 'Больше нечего постить. Добавьте изображения в каталог (' + disk_folder_id + ') на Яндекс диск.'
        api_url = f'https://api.vk.com/method/messages.send?access_token={config.vk_token}&group_id={vk_group_id}&user_id={config.vk_user_id}&message={vk_message_text}&random_id={random_id}&v={config.vk_api_version}'
        response = requests.get(api_url)
        print(
            name + " Больше нечего постить. Добавьте изображения в каталог (" + disk_folder_id + ") на Яндекс диск.")
        return response

def VKGetAttachments(selected_images, vk_group_id, name, vk_message_prompt ):
    attachments = []
    # Загрузка выбранных изображений на сервер ВК
    for image in selected_images:
        url = "https://api.vk.com/method/photos.getWallUploadServer"
        params = {"access_token": config.vk_token, "group_id": vk_group_id, "v": config.vk_api_version}
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        if 'response' in data:
            upload_url = data['response']['upload_url']
        else:
            print("Error: " + data['error']['error_msg'])
            return

        # Скачиваем картинки
        print(f"{name}: Скачиваю изображение с Яндекс Диска")
        image_url = image['file']
        image_data = requests.get(image_url).content

        # Формируем запрос для Вконтакте
        files = {"photo": ("image.jpg", image_data)}
        response = requests.post(upload_url, files=files)
        data = json.loads(response.text)
        photo_id = data['photo']
        server = data['server']
        hash_ = data['hash']

        # Загружаем изображения на сервек ВК
        url = "https://api.vk.com/method/photos.saveWallPhoto"
        params = {
            "access_token": config.vk_token,
            "group_id": vk_group_id,
            "photo": photo_id,
            "server": server,
            "hash": hash_,
            "message": vk_message_prompt,
            "v": config.vk_api_version
        }
        response = requests.post(url, params=params)
        data = json.loads(response.text)
        if 'response' in data:
            attachment = f"photo{data['response'][0]['owner_id']}_{data['response'][0]['id']}"
            attachments.append(attachment)
        else:
            print("Error: " + data['error']['error_msg'])
            exit()
    return attachments


def VKPostCreate(name, vk_group_id, vk_message_prompt,available_images, attachments,disk_folder_id, notifications):
    # Создаем пост в группе ВК
    print(f"{name}: Публикую пост в группу - " + vk_group_id)
    url = "https://api.vk.com/method/wall.post"
    params = {
        "access_token": config.vk_token,
        "owner_id": -int(vk_group_id),
        "attachments": ",".join(attachments),
        "message": vk_message_prompt,
        "v": config.vk_api_version
    }
    response = requests.post(url, params=params)
    data = json.loads(response.text)
    # Отправляем уведомление от имени группы ВК
    if 'response' in data:
        if notifications:
            print(f"{name}: Пост в группе был успешно опубликован.")
            print(datetime.now().time())
            random_id = random.randint(1, 2 ** 63 - 1)
            vk_message_text = f'Пост в группе был успешно опубликован. Осталось {len(available_images)} изображений. Не забудьте вовремя пополнить каталог {disk_folder_id} на Яндекс Диске.'
            api_url = f'https://api.vk.com/method/messages.send?access_token={config.vk_token}&group_id={vk_group_id}&user_id={config.vk_user_id}&message={vk_message_text}&random_id={random_id}&v={config.vk_api_version}'
            response = requests.get(api_url)
        else:
            print("Error: " + data['error']['error_msg'])
            return
    return response


def VKChatBotSetUp(group_id,group_name):
    global longpoll_server
    global longpoll_key
    global longpoll_ts
    try:
        url = "https://api.vk.com/method/groups.getLongPollServer"
        params = {"group_id": group_id, "access_token": config.vk_token, "v": config.vk_api_version}
        response = requests.get(url, params=params).json()
    except:
        print(f"{group_name}: Ошибка подключения к LongPoll Серверу. Проверьте корректность токена")
        return

    try:
        longpoll_server = response['response']['server']
        longpoll_key = response['response']['key']
        longpoll_ts = response['response']['ts']
        print(f"{group_name}: Чат бот подключен. Ожидаем комментарии")
    except:
        print(f"{group_name}: Ошибка. Убедитесь что LongPoll включен в настройках группы")
    return longpoll_server, longpoll_key, longpoll_ts


def VKChatBotCommentsParser(longpoll_server, longpoll_key, longpoll_ts,access_token, group_id, msg_from_group,conversation_id):
        while True:
            try:
                response = requests.get(
                    f"{longpoll_server}?act=a_check&key={longpoll_key}&ts={longpoll_ts}&wait=25"
                ).json()
                longpoll_ts = response['ts']
            except:
                print(f"{msg_from_group}: Ошибка подключения к Longpoll серверу. Переподключаемся..." + "\n")
                longpoll_server, longpoll_key, longpoll_ts = VKChatBotSetUp(group_id,msg_from_group)
                continue

            try:
                for update in response['updates']:
                    if update['type'] == 'wall_reply_new':
                        object_id = update['object']['id']
                        post_id = update['object']['post_id']
                        from_id = update['object']['from_id']
                        message = update['object']['text']

                        if from_id > 0:
                            print(f"{msg_from_group}: Получен новый комментарий!")
                            try:
                                answer = GPTChatQueue(message, group_id,msg_from_group, conversation_id)
                            except:
                                print(f"{msg_from_group}: Не удалось получить ответ от ChatGPT")
                                continue
                            else:
                                try:
                                    debug = requests.get(f"https://api.vk.com/method/wall.createComment",
                                                         params={
                                                             "owner_id": f"-{group_id}",
                                                             "post_id": post_id,
                                                             "from_group": 1,
                                                             "message": answer,
                                                             "reply_to_comment": object_id,
                                                             "access_token": access_token,
                                                             "v": config.vk_api_version
                                                         }).json()
                                    if 'error' in debug:
                                        print(f"{msg_from_group}: Ошибка отправки ответа бота: {debug['error']['error_msg']}")
                                    else:
                                        print(f"{msg_from_group}: Ответ бота отправлен успешно!")
                                except:
                                    print(f"{msg_from_group}: Ошибка отправки ответа бота!!!")

            except:
                print(f"{msg_from_group}: Ошибка обработки ответа сервера. Переподключаемся...")
                continue

            time.sleep(1)

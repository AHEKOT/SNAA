import random
import config
from api.GPTApi import GPTQueue
from api.VKApi import VKNotifyNoImages, VKGetAttachments, VKPostCreate
from api.YDApi import YDLoadAllImages, YDLoadImagesFromSubfolders, YDMoveFolder, YDMoveSelectedImages

def vk_upload(img_count,vk_group_id,vk_group_name,vk_posting_type,disk_folder_id,vk_message_prompt,conversation_id,notifications):

    # Загружаем список картинок из Яндекс Диска, в зависимости от выбранного метода
    available_images = []
    match vk_posting_type:
        # Функция отправки случайных изображений в группу ВК
        case "random":
            # Загружаем список изображений из каталога
            available_images = YDLoadAllImages(vk_group_name, disk_folder_id)
            # Проверяем хватит ли картинок для поста
            try:
                if (len(available_images)) < img_count:
                    if notifications:
                        VKNotifyNoImages(vk_group_name, disk_folder_id, vk_group_id, available_images, img_count)
                        return
            except:
                print(f"{vk_group_name}: Не удалось загрузить файлы с Яндекс Диска")
                print(f"{vk_group_name}: Пост не будет опубликован. Проверьте доступность Яндекс диска.")
                return
            # Выбираем случайные картинки для поста
            selected_images = random.sample(available_images, img_count)
            print(f"{vk_group_name}: Случайные изображения выбраны")
            # Генерируем текст для поста с помощью ChatGPT
            if config.use_GPT:
                if conversation_id=="default":
                    vk_message_prompt = GPTQueue(vk_message_prompt, config.gpt_conversation_id)
                else:
                    vk_message_prompt = GPTQueue(vk_message_prompt, conversation_id)

                if vk_message_prompt == "":
                    return
            # Загружаем файлы на сервер и получаем ссылки на них
            attachments = VKGetAttachments(selected_images, vk_group_id, vk_group_name, vk_message_prompt)
            # Публикуем пост в группу Вконтакте
            VKPostCreate(vk_group_name, vk_group_id, vk_message_prompt, available_images, attachments, disk_folder_id,notifications)
            # Перемещаем использованные картинки в каталог Used
            YDMoveSelectedImages(disk_folder_id, selected_images,available_images, config.disk_used_images_path)
        # Функция отправки изображений из подкаталогов в алфавитном порядке в группу ВК
        case "subfolder":
            # Загружаем список изображений из каталога
            try:
                available_images, folder, used_item_id = YDLoadImagesFromSubfolders(vk_group_name, disk_folder_id)
            except:
                print(f"{vk_group_name}: Не удалось загрузить файлы с Яндекс Диска")
                print(f"{vk_group_name}: Пост не будет опубликован. Проверьте доступность Яндекс диска.")
                return
            # Проверяем хватит ли картинок для поста

            if available_images=='':
                if notifications:
                    VKNotifyNoImages(vk_group_name, disk_folder_id, vk_group_id, available_images, img_count)
                    return

            selected_images = available_images
            # Генерируем текст для поста с помощью ChatGPT
            if config.use_GPT:
                if conversation_id == "default":
                    vk_message_prompt = GPTQueue(vk_message_prompt, config.gpt_conversation_id)
                else:
                    vk_message_prompt = GPTQueue(vk_message_prompt, conversation_id)

                if vk_message_prompt == "":
                    return
            # Загружаем файлы на сервер и получаем ссылки на них
            attachments = VKGetAttachments(selected_images, vk_group_id, vk_group_name, vk_message_prompt)
            # Публикуем пост в группу Вконтакте
            VKPostCreate(vk_group_name, vk_group_id, vk_message_prompt, available_images, attachments, disk_folder_id, notifications)
            # Перемещаем использованные картинки в каталог Used
            YDMoveFolder(vk_group_name, used_item_id, config.disk_used_images_path)
        # Если получена некорректная команда - не делать ничего
        case _:
            print(f"{vk_group_name}: Некорректный метод загрузки:  {vk_posting_type}")
            return

    return
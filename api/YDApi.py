import random
import tempfile
import telegram
from yadisk import YaDisk, exceptions
import config

# подключаем API Яндекс Диска
yd = YaDisk(token=config.disk_token)


def YDLoadAllImages(vk_group_name, disk_folder_id):
    # Загружаем список изображений из каталога на Яндекс Диске
    try:
        images_list = []
        images_list = yd.listdir(disk_folder_id)
    except exceptions.YaDiskError as e:
        print(f"{vk_group_name}: Не удалось подключиться к Яндекс Диску. {e}")
        print(f"{vk_group_name}: Проверьте корректность Яндекс токена. {e}")
        return
    except exceptions.PathNotFoundError as e:
        print(f"{vk_group_name}: каталог с изображениями {disk_folder_id} не найден. {e}")
        print(f"{vk_group_name}: Проверьте корректность пути к каталогу изображений в настройках бота"
              )
        return
    # Проверяем что все полученные файлы - изображения
    #try:
    available_images = [i for i in images_list if i['type'] == 'file' and i['mime_type'].startswith('image/')]

    print(f"{vk_group_name}: {len(available_images)} изображений в каталоге.")
    return available_images
    #except:
    #    print(f"{vk_group_name} Ошибка работы Яндекс Диска")
    #    return


def YDLoadImagesFromSubfolders(vk_group_name, disk_folder_id):
    # Загружаем список подкаталогов из главного каталога на Яндекс Диске
    try:
        folders_list = yd.listdir(disk_folder_id)
    except exceptions.YaDiskError as e:
        print(f"{vk_group_name}: Не удалось подключиться к Яндекс Диску. {e}")
        print(f"{vk_group_name}: Проверьте корректность Яндекс токена. {e}")
        return
    except exceptions.PathNotFoundError as e:
        print(f"{vk_group_name}: каталог с изображениями {disk_folder_id} не найден. {e}")
        print(f"{vk_group_name}: Проверьте корректность пути к каталогу изображений в настройках бота")
        return

    # Проверка существования подкаталогов в главном каталоге
    try:
        unuploaded_folders = [folder for folder in folders_list if
                          folder['type'] == 'dir' and folder['name']]
    except:
        print(f"{vk_group_name}: Ошибка работы Яндекс Диска")
        return
    if not unuploaded_folders:
        print(f"{vk_group_name}: Все папки уже были загружены.")
        available_images = ''
        folder_name = ''
        used_item_id = ''
        return available_images, folder_name, used_item_id

    # Загружаем изображения из первого подкаталога
    unuploaded_folder = unuploaded_folders[0]
    try:
        images_list = yd.listdir(unuploaded_folder['path'])
    except exceptions.YaDiskError as e:
        print(f"{vk_group_name}: Не удалось подключиться к Яндекс Диску. {e}")
        print(f"{vk_group_name}: Проверьте корректность Яндекс токена. {e}")
        return
    except exceptions.PathNotFoundError as e:
        print(f"{vk_group_name}: каталог с изображениями {unuploaded_folder['path']} не найден. {e}")
        print(f"{vk_group_name}: Проверьте корректность пути к каталогу изображений в настройках бота")
        return
    # обрабатываем список полученных изображений в алфавитном порядке
    images_list = [i for i in sorted(images_list, key=lambda x: int(x['name'].split('.')[0])) if
                   i['type'] == 'file' and i['mime_type'].startswith('image/')]
    print(f"{vk_group_name}: {len(images_list)} изображений в каталоге {unuploaded_folder['path']}.")

    # Обрабатываем имя и путь каталога
    folder_name=unuploaded_folder['name']
    used_item_id = unuploaded_folder['path']
    # Форматируем список изображений
    available_images = [image for image in images_list if image['name']]
    return available_images, folder_name, used_item_id


def YDDownloadImages(random_images,post_text):
    media_objects = []
    # Загружаем изображения с диска во временный файл
    for image in random_images:
        with tempfile.NamedTemporaryFile() as temp_file:
            image_path = temp_file.name
            try:
                # скачиваем файл
                yd.download(src_path=image['path'], path_or_file=image_path)
            except exceptions.PathNotFoundError as e:
                print(e)
            with open(image_path, 'rb') as f:
                media_bytes = f.read()
            # Добавляем файл в список для дальнейшей публикации
            media_objects.append(
                telegram.InputMediaPhoto(media=media_bytes, caption=post_text))
    return media_objects

def YDDownloadToIG(selected_images,name):
    file_paths = []
    # Загружаем изображения с диска во временный файл
    for image in selected_images:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            image_path = temp_file.name
            try:
                # скачиваем файл
                yd.download(src_path=image['path'], path_or_file=image_path)
                file_paths.append(image_path)
            except exceptions.PathNotFoundError as e:
                print(e)
                continue
    return file_paths

def YDMoveFolder(vk_group_name, source_folder_id, destination_folder_id):
    try:
        # Получаем информацию о каталоге
        source_folder_info = yd.get_meta(source_folder_id)

        # Создаем новый каталог с тем же именем в пути назначения
        try:
            new_folder_path = destination_folder_id + '/' + source_folder_info['name']
            yd.mkdir(new_folder_path)
        except:
            # Если каталог уже существует - генерируем случайное число и добавляем его к имени
            print(f"{vk_group_name}: Каталог {new_folder_path} уже существует.")
            rnd = random.randint(1, 2 ** 63 - 1)
            new_folder_path = new_folder_path+"_duplicate_"+str(rnd)
            print(f"{vk_group_name}: Создаем новый каталог {new_folder_path}")
            yd.mkdir(new_folder_path)

        # Копируем информацию из старого каталога в новый
        try:
            for file in yd.listdir(source_folder_id):
                if file['type'] == 'file':
                    file_path = source_folder_id + '/' + file['name']
                    new_file_path = new_folder_path + '/' + file['name']
                    yd.copy(file_path, new_file_path, overwrite=True)
        except exceptions.YaDiskError as e:
            print(f"{vk_group_name}: Ошибка перемещения каталога: {e}")
            return False
        try:
            # Удаляем старый каталог
            yd.remove(source_folder_id)
        except exceptions.YaDiskError as e:
            print(f"{vk_group_name}: Ошибка удаления старого каталога: {e}")
            return False

        print(f"{vk_group_name}: Каталог {source_folder_info['name']} был перемещен в {new_folder_path}")
        return True

    except exceptions.YaDiskError as e:
        print(f"{vk_group_name}: Ошибка перемещения каталога: {e}")
        return False


def YDMoveSelectedImages(source_folder_id, selected_images,available_images, destination_folder_id):
    try:
        # Получаем информацию о каталоге
        source_folder_info = yd.get_meta(source_folder_id)

        # Если каталога не существует - создаем новый
        try:
            new_folder_path = destination_folder_id + '/' + source_folder_info['name']
            yd.mkdir(new_folder_path)
        except:
            print()

        # Перемещаем файлы в новый каталог для использованных изображений
        for image in selected_images:
            for file in available_images:
                #print(f"Processing file {file['name']}")
                if file['name'] == image['name']:
                    file_path = source_folder_id + '/' + file['name']
                    new_file_path = new_folder_path + '/' + file['name']
                    yd.move(file_path, new_file_path, overwrite=True)
        return True

    except exceptions.YaDiskError as e:
        print(f"Ошибка перемещения файла: {e}")
        return False
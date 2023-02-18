import random
import config
from api.TGApi import TGNoImages, TGSendPost
from api.YDApi import YDDownloadImages, YDMoveSelectedImages, YDLoadAllImages


async def tg_upload(img_count, name, disk_folder_id, used_images, post_text):
  available_images = []
  # Загружаем список картинок на Яндекс Диске
  available_images=YDLoadAllImages(name, disk_folder_id, used_images)
  # Проверяем хватит ли картинок для поста
  if (len(available_images)) < img_count:
    await TGNoImages(available_images, img_count, name, disk_folder_id)
  # Выбираем случайные картинки для поста
  selected_images = random.sample(available_images, img_count)
  print(name + " случайные изображения выбраны")
  # Подготавливаем картинки к загрузке
  media_objects = YDDownloadImages(selected_images,post_text)
  # Публикуем пост в группу
  await TGSendPost(name, media_objects, selected_images, disk_folder_id)
  # Добавляем использованные картинки в список
  YDMoveSelectedImages(disk_folder_id, selected_images, available_images, config.disk_used_images_path)
import random
import config
from api.IGApi import IGUploadImage
from api.YDApi import YDLoadAllImages, YDMoveSelectedImages, YDDownloadToIG


def UploadToIG(img_count, ig_name, ig_password, disk_folder_id, caption):
    available_images = YDLoadAllImages(ig_name, disk_folder_id)
    if (len(available_images)) < img_count:
        return
    selected_images = random.sample(available_images, img_count)
    print(f"{ig_name}: случайные изображения выбраны")
    # Подготавливаем картинки к загрузке
    file_paths = YDDownloadToIG(selected_images, ig_password)
    try:
        IGUploadImage(file_paths, caption, ig_name, ig_password)
        print(f"{ig_name}: Изображения успешно опубликованы")
    except:
        return
    YDMoveSelectedImages(disk_folder_id, selected_images,available_images, config.disk_used_images_path)
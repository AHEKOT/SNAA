import telegram
import config

# Подключаем бота Telegram
bot = telegram.Bot(token=config.tg_token)


async def TGNoImages(available_images, img_count, name,disk_folder_id):
    # Если в каталоге недостаточно изображений для создания поста - отправляем уведомление личным сообщением
    if (len(available_images)) < img_count:
        print(name + " Больше нечего постить. Добавьте изображений в каталог (" +
              disk_folder_id + ") на Яндекс диск.")
        try:
            await bot.send_message(
                name=config.user_id,
                text="В группу " + name +
                     " больше нечего постить. Добавьте изображения в каталог (" +
                     disk_folder_id + ") на Яндекс диск.")
        except Exception as e:
            print(name + " Бот не может отправить вам сообщение: ", e)
            print(name + " Начните чат со своим ботом чтобы разрешить ему отправлять вам уведомления"
                  )
    return


async def TGSendPost(name, media_objects, disk_folder_id,available_images,post_text):
    tg_images=[]
    for media in media_objects:
        tg_images.append(telegram.InputMediaPhoto(media=media, caption=post_text))
    # Отправляем сообщение с изображениями в канал Telegram
    try:
        await bot.send_media_group(name, tg_images)
        print(f"{name}: Изображения успешно опубликованы")
        await bot.send_message(
            chat_id=config.user_id,
            text=f'Пост в группу {name} успешно опубликован. Осталось {len(available_images)} изображений доступных для публикации. Не забудьте вовремя пополнить каталог {disk_folder_id} на Яндекс Диске.')

    except Exception as e:
        print(f"{name}: Не удалось опубликовать изображения: ", e)
    return

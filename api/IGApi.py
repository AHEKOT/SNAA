from instagrapi import Client, exceptions


def IGUploadImage(file_paths, caption, ig_name, ig_password):
    cl = Client()
    cl.login(ig_name, ig_password, relogin=True)
    try:
        for path in file_paths:
            cl.photo_upload(path, caption)
    except exceptions as e:
        print(e)
    return
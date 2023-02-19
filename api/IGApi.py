from instagrapi import Client



def IGUploadImage(file_paths,caption,ig_name, ig_password):
    cl = Client()
    cl.login(ig_name, ig_password)
    for path in file_paths:
        cl.photo_upload(path, caption)
    return
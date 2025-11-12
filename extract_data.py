from PIL import Image
def get_date_taken(path):
    exif = Image.open(path)._getexif()
    if not exif:
        raise Exception('Image {0} does not have EXIF data.'.format(path))
    return exif[36867]
print(get_date_taken(r"C:\Users\Steve\Documents\hackathon 2\IMG_20251112_172633188.jpg"))
from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    pass
    # ext = os.path.splitext(value.name)[1]   #cover-image.jpg
    # print(ext)
    
    # valied_extentions = ['.jpg', '.png', '.jpeg',]
    # if not ext.lower() in valied_extentions:
    #     raise ValidationError('Unsupported file extention. Allowed extentions:' +str(valied_extentions))


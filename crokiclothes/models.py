from django.db import models

# Create your models here.

def upload_path(instance, filename):
    return '/'.join(["coverimages", str(instance.title), filename])

def converting_images_path(instance, filename):
    return '/'.join(["convertingimages", str(instance.title), filename])

def upload_models_path(instance, filename):
    return '/'.join(["AugModels", str(instance.title), filename])


def upload_path_2(instance, filename):
    return '/'.join(["coverimages", str(instance.cloth.title), filename])

def converting_images_path_2(instance, filename):
    return '/'.join(["convertingimages", str(instance.aug_model.cloth.title), filename])


def textures_images(instance, filename):
    return '/'.join(["texture_images", str(instance.aug_model.cloth.title), filename])

def upload_models_path_2(instance, filename):
    return '/'.join(["AugModels", str(instance.cloth.title), filename])

def upload_texture_path_2(instance, filename):
    return '/'.join(["Textures", str(instance.cloth.title), filename])

class Clothes(models.Model):
    title=models.CharField(max_length=150)
    description = models.CharField(max_length=500, blank=True)
    coverimages = models.ImageField(upload_to=upload_path, blank=True)
    convertingimages = models.ImageField(upload_to=converting_images_path, blank=True)
    aug_model = models.FileField(upload_to=upload_models_path, default="Storage/AugModels/texturedMesh.obj", blank=True)

    # string representation of the class
    def __str__(self):
        #it will return the title
        return self.title
    
    
class WearablePart(models.TextChoices):
    TOP = 'TOP', ('Top')
    BOTTOM = 'BM', ('Bottom')
    FULL = 'FL', ('Full')

class Clothes_V2(models.Model):
    title=models.CharField(max_length=150)
    description = models.CharField(max_length=500, blank=True)
    wearable_part = models.CharField(
        max_length=3,
        choices=WearablePart.choices,
        default=WearablePart.TOP,
    )
    # string representation of the class
    def __str__(self):
        #it will return the title
        return self.title
    

    
class CoverImage(models.Model):
    coverimages = models.ImageField(upload_to=upload_path_2, blank=True)
    cloth = models.ForeignKey(Clothes_V2, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        #it will return the title
        return self.cloth.title + "Cover_Images"
    

class ArObject(models.Model):
    
    aug_model = models.FileField(upload_to=upload_models_path_2, blank=True)
    cloth = models.ForeignKey(Clothes_V2, on_delete=models.CASCADE, blank=True, null=True)
    texture = models.ImageField(upload_to=upload_texture_path_2, blank=True) ## Should be multiple
    # mesh_textures = pass
    
    def __str__(self):
        #it will return the title
        return self.cloth.title + "Augmented_Objects"
    
class ImagesToConvert(models.Model):
    convertingimages = models.ImageField(upload_to=converting_images_path_2, blank=True)
    aug_model = models.ForeignKey(ArObject, on_delete=models.CASCADE, blank=True, null=True)
    
    
    def __str__(self):
        #it will return the title
        return self.aug_model.cloth.title + "Images_To_Convert "


class TextureImages(models.Model):
    texture_images = models.ImageField(upload_to=textures_images, blank=True)
    aug_model = models.ForeignKey(ArObject, on_delete=models.CASCADE, blank=True, null=True)
    
    
    def __str__(self):
        #it will return the title
        return self.aug_model.cloth.title + "Texture_Images"
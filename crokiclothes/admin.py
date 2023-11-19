from django.contrib import admin
from .models import Clothes, Clothes_V2, CoverImage, ImagesToConvert, ArObject, TextureImages
# Register your models here.

class TextureInline(admin.TabularInline):
    model = TextureImages

class CoverImageInline(admin.TabularInline):
    model = CoverImage
    
class ImagesToConvertInline(admin.TabularInline):
    model = ImagesToConvert
    
class Ar_objectInline(admin.TabularInline):
    model = ArObject
    inlines =[
        ImagesToConvertInline
    ]
    
class ArObjectAdmin(admin.ModelAdmin):
    list_display = ("id","aug_model","texture")
    inlines =[
        ImagesToConvertInline,
        TextureInline
    ]
    
class ClothesAdminV2(admin.ModelAdmin):
    list_display = ("id","title","description", 'wearable_part')
    # list_display ="__all__"
    inlines=[
        CoverImageInline,
        Ar_objectInline,
        # WearablePartInline
    ]
    
class ClothesAdmin(admin.ModelAdmin):
    list_display = ("title","description","coverimages")
    
    

admin.site.register(Clothes,ClothesAdmin)
admin.site.register(ArObject, ArObjectAdmin)
admin.site.register(Clothes_V2, ClothesAdminV2)

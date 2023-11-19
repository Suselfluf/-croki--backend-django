from rest_framework import serializers
from .models import Clothes, CoverImage, Clothes_V2, ImagesToConvert, ArObject, TextureImages

class TextureImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextureImages
        fields = ("__all__")

class ClothesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clothes
        fields = ('__all__')
        
class CoverImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverImage
        fields = ("__all__")

class ConvertingImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesToConvert
        fields = ("__all__")
           
class ArObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArObject
        fields = ("__all__")
        
class ClothV2CreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Clothes_V2
        fields = ("__all__")

class AugModelSerializer(serializers.ModelSerializer):
    converting_images = serializers.SerializerMethodField()

    class Meta:
        model = ArObject
        fields = ("__all__")
        
    def get_converting_images(self, obj):
        aug_model_instances = ImagesToConvert.objects.all().filter(aug_model_id=obj.id)
        if aug_model_instances.exists():
            return ConvertingImagesSerializer(aug_model_instances, many=True).data
        else:
            return None
        
 
    


class ClothesV2Serializer(serializers.ModelSerializer):
    aug_model = serializers.SerializerMethodField()
    cover_images = serializers.SerializerMethodField()
    
    class Meta:
        model = Clothes_V2
        fields = ('__all__')
        
    def get_aug_model(self, obj):
        try:
            aug_model_instance = ArObject.objects.get(cloth=obj.id)
        except ArObject.DoesNotExist:
            return []
        return AugModelSerializer(aug_model_instance).data
    
    def get_cover_images(self, obj):
        try:
            cover_images = CoverImage.objects.all().filter(cloth=obj.id)
        except CoverImage.DoesNotExist:
            return []
        return CoverImagesSerializer(cover_images, many=True).data
        

class ImagesToConvertSerializer(serializers.ModelSerializer):
    aug_model_id = serializers.ReadOnlyField(source="aug_model.id")
    class Meta:
        model = ImagesToConvert
        fields = (['id','convertingimages','aug_model_id'])
        
class ClothesCoverInfoSerializer(serializers.ModelSerializer):
    cover_images = serializers.SerializerMethodField()
    def get_cover_images(self, obj):
        cover_images = CoverImage.objects.all().filter(cloth=obj.id)
        if cover_images.exists():
            return CoverImagesSerializer(cover_images, many=True).data
        else:
            return None
    
    class Meta:
        model = Clothes_V2
        fields = ('__all__')
        
class AugmentedObjectFolderSerializer(serializers.Serializer):
    aug_model = serializers.SerializerMethodField()
    textures = serializers.SerializerMethodField()
    class Meta:
        model = Clothes_V2
        fields = (['id','title','aug_model', 'textures'])
        
    def get_aug_model(self, obj):
        try:
            aug_model_instance = ArObject.objects.get(cloth=obj.id)
        except ArObject.DoesNotExist:
            return []
        return AugModelSerializer(aug_model_instance).data
    
    
    def get_textures(self, obj):
        try:
            aug_model_instance = ArObject.objects.get(cloth=obj.id)
        except  ArObject.DoesNotExist:
            return None 
        else:
            try:
                textures_instances = TextureImages.objects.all().filter(aug_model=aug_model_instance.id)
            except TextureImages.DoesNotExist:
                return None
        return TextureImagesSerializer(textures_instances, many=True).data
    
    # def get_converting_images(self, obj):
    #     try:    
    #         aug_model_instances = ImagesToConvert.objects.all().filter(aug_model_id=obj.id)
    #         if aug_model_instances.exists():
    #             return ConvertingImagesSerializer(aug_model_instances, many=True).data
    #         else:
    #             return None
    #     except ImagesToConvert.DoesNotExist:
    #         return []
    
class WorkshopSerializer(serializers.ModelSerializer):
    aug_model = serializers.SerializerMethodField()
    texture = serializers.SerializerMethodField()
    
    class Meta:
        model = Clothes_V2
        fields = (['id','title','aug_model', 'texture' ])
        
    def get_aug_model(self, obj):
        try:
            aug_model_instance = ArObject.objects.get(cloth=obj.id)
        except ArObject.DoesNotExist:
            return []
        return AugModelSerializer(aug_model_instance).data
    
    def get_texture(self, obj):
        try:
            aug_model_instance = ArObject.objects.get(cloth=obj.id)
        except  ArObject.DoesNotExist:
            return None 
        else:
            try:
                textures_instance = TextureImages.objects.all().filter(aug_model=aug_model_instance.id)
            except TextureImages.DoesNotExist:
                return None
        return TextureImagesSerializer(textures_instance, many=True).data
    
    
    
class ConvertingImagesToConvertSerializer(serializers.Serializer):
    # aug_model = serializers.SerializerMethodField()
    convertingimages = serializers.SerializerMethodField()
    class Meta:
        model = Clothes_V2
        fields = (['convertingimages'])
        
    # def get_aug_model(self, obj):
    #     try:
    #         aug_model_instance = ArObject.objects.get(cloth=obj.id)
    #     except ArObject.DoesNotExist:
    #         return []
    #     return AugModelSerializer(aug_model_instance).data
    
    def get_convertingimages(self, obj):
        converting_images_instance = ImagesToConvert.objects.all().filter(aug_model_id=obj.id)
        if converting_images_instance.exists():
            return ConvertingImagesSerializer(converting_images_instance, many=True).data
        else:
            return None
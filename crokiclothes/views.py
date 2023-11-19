
from django.shortcuts import render
import requests
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import *



from .serializers import *
from .models import Clothes, Clothes_V2, CoverImage, ImagesToConvert, ArObject
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from django.http import FileResponse



class ClothesModelView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticatedOrReadOnly)
    
    def get(self, request):
        
        clothes = Clothes.objects.all()
        serializer = ClothesSerializer(clothes,many=True)
        
        return Response(serializer.data)
          
    def post(self, request):
        serializer = ClothesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

 
class ClothesView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, pk=None):
        clothes = Clothes.objects.get(id=pk)
        serializer = ClothesSerializer(clothes)
        return Response(serializer.data)
    
    def put(self, request, pk=None):
        clothes = Clothes.objects.get(id=pk)
        serializer = ClothesSerializer(instance=clothes, data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        clothes = Clothes.objects.get(id=pk)
        clothes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ClothManagement(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, pk=None):

        cloth = Clothes_V2.objects.get(id=pk)
        serializer = ClothesV2Serializer(cloth,many=False)
        
        return Response(serializer.data)      
    
    def put(self, request, pk=None):
        cloth = Clothes_V2.objects.get(id=pk)
        serializer = ClothesV2Serializer(instance=cloth, data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, pk=None):
        # serializer = ClothesSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer = ClothesV2Serializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        clothes = Clothes.objects.get(id=pk)
        clothes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ClothesModelViewV2(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAdminUser, )
    # permission_classes = (IsAuthenticatedOrReadOnly, )
    # permission_classes = (IsAuthenticated, )
    
    def get(self, request, pk=None):
        clothes = Clothes_V2.objects.all()
        serializer = ClothesCoverInfoSerializer(clothes,many=True)
        
        return Response(serializer.data)
    
    def put(self, request, pk=None):
        cloth = Clothes_V2.objects.all()
        serializer = ClothesV2Serializer(cloth,many=True)
        
        return Response(serializer.data)
    
    def post(self, request, pk=None):
        
        serializer = ClothV2CreateSerializer(data = request.data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def delete(self, request, pk=None):
        clothes = Clothes.objects.get(id=pk)
        clothes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CoverImagesForCloth(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, pk=None):

        cover_images = CoverImage.objects.all().filter(cloth=pk)
        serializer = CoverImagesSerializer(cover_images,many=True)
        
        return Response(serializer.data)
    
    def post(self, request, pk=None):
    
        serializer = CoverImagesSerializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
            cover_images = CoverImage.objects.all().filter(cloth=pk)
            response_cover_images = CoverImagesSerializer(cover_images,many=True)
            return Response(response_cover_images.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):  ## Needs to be reworked (wrong url formation)
        
        cloth_id = request.data.get('cloth')
        cover_image_id = request.data.get('id')
        cover_image = CoverImage.objects.get(id=cover_image_id)
        cover_image.delete()
        cover_images = CoverImage.objects.all().filter(cloth=cloth_id)
        serializer = CoverImagesSerializer(cover_images,many=True)
        
        return Response(serializer.data)
        
class ConvertingImagesForAugObject(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, pk=None):
        try: 
            # cloth = Clothes_V2.objects.get(id=pk)
            # aug_object_serialized = AugmentedObjectFolderSerializer(cloth,many=False)
            # return Response(aug_object_serialized.data, status=status.HTTP_200_OK)
        
            converting_images = ImagesToConvert.objects.all().filter(aug_model=pk)
            response_converting_images = ConvertingImagesSerializer(converting_images,many=True)
            return Response(response_converting_images.data, status=status.HTTP_200_OK)
        except ImagesToConvert.DoesNotExist:
            return None
        # except Clothes_V2.DoesNotExist:
        #     return None
        
    def put(self, request, pk=None):
        # folder_name = request.data.get('folder-name')
        aug_model_pn, converting_images_pn = request.data 
        aug_model_id = request.data.get('aug_model')
        cloth_id = pk
        if(aug_model_id == "undefined"):
            cloth_data = {"cloth":cloth_id }
            serializer = ArObjectSerializer(data=cloth_data)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                
                aug_model_id = serializer.data.get('id')
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        for file in request.FILES.getlist('convertingimages'):
            # print({aug_model_pn:aug_model_id, converting_images_pn:file})
            req = {aug_model_pn:aug_model_id, converting_images_pn:file}
            serializer = ConvertingImagesSerializer(data=req)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        converting_images = ImagesToConvert.objects.all().filter(aug_model=aug_model_id)
        response_converting_images = ConvertingImagesSerializer(converting_images,many=True)
        return Response(response_converting_images.data, status=status.HTTP_201_CREATED)
    
    def post(self, request, pk=None):
        # folder_name = request.data.get('folder-name')
        aug_model_pn, converting_images_pn = request.data 
        aug_model_id = request.data.get('aug_model')
        cloth_id = pk
        if(aug_model_id == "undefined"):
            cloth_data = {"cloth":cloth_id }
            serializer = ArObjectSerializer(data=cloth_data)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                created_aug_object = ArObject.objects.get(cloth=cloth_id)
                # cloth = Clothes_V2.objects.get(id=pk)
                # cloth_serializer = ClothesV2Serializer(instance=cloth, data=request.data)
                # print(created_aug_object.id)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        for file in request.FILES.getlist('convertingimages'):
           
            req = {aug_model_pn:aug_model_id, converting_images_pn:file}
            serializer = ConvertingImagesSerializer(data=req)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        converting_images = ImagesToConvert.objects.all().filter(aug_model=aug_model_id)
        response_converting_images = ConvertingImagesSerializer(converting_images,many=True)
        return Response(response_converting_images.data, status=status.HTTP_201_CREATED)
            
    def delete(self, request, pk=None): 
        aug_model_id = request.data.get('aug_model')
        convering_image_id = request.data.get('id')
        converting_image = ImagesToConvert.objects.get(id=convering_image_id)
        converting_image.delete()
        rest_converting_images = ImagesToConvert.objects.all().filter(aug_model=aug_model_id)
        serializer = ConvertingImagesSerializer(rest_converting_images,many=True)
        
        return Response(serializer.data)

class AugmentedObjView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, pk=None):
        try:
            cloth = Clothes_V2.objects.get(id=pk)
            aug_object_serialized = AugmentedObjectFolderSerializer(cloth,many=False)
            return Response(aug_object_serialized.data, status=status.HTTP_200_OK)
        except Clothes_V2.DoesNotExist:
            return None

        # aug_object = ArObject.objects.all().filter(cloth=pk)
        # aug_object_serialized = ArObjectSerializer(aug_object,many=True)
        # return Response(aug_object_serialized.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None):
        folder_name = request.data.get('folder_name')
        # publish(folder_name)

        # aug_object = ArObject.objects.all().filter(cloth=pk)
        # aug_object_serialized = ArObjectSerializer(aug_object,many=True)
        # return Response(aug_object_serialized.data, status=status.HTTP_200_OK)
        return Response("None")
    
    def post (self, request, pk=None):
        print("Has recieved smth")
        mesh_obj = request.data.get("texturedMesh.obj")
        texture = request.data.get("texture_1001.png")
        cloth_id = request.data.get("cloth")
        print(mesh_obj)
        print(cloth_id)
        print(texture)

        cloth_data = {"cloth":cloth_id, "aug_model":mesh_obj, "texture":texture }
        ar_object = ArObject.objects.get(cloth=cloth_id)
        serializer = ArObjectSerializer(instance=ar_object, data=cloth_data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
            print("saved")
        else:
            print("Failed to serialize")
    
        return Response("Recieved")
    

    
   
        
class ClothesAugView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, pk=None):
        clothes = Clothes.objects.get(id=pk)
        response = clothes
        return FileResponse(response, content_type='image/png')
    
  
class WorkshopView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def get(self, request, pk=None):
        wearable_part = request.data.get('wearable_part')
        aug_object = Clothes_V2.objects.all().filter(wearable_part=wearable_part)
        aug_object_serialized = WorkshopSerializer(aug_object,many=True)
        
        return Response(aug_object_serialized.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None):
        wearable_part = request.data.get('wearable_part')
        aug_object = Clothes_V2.objects.all().filter(wearable_part=wearable_part)
        aug_object_serialized = WorkshopSerializer(aug_object,many=True)
        
        return Response(aug_object_serialized.data, status=status.HTTP_200_OK)
        
    
# class WorkshopBottomView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     permission_classes = (IsAuthenticatedOrReadOnly, )
    
#     def get(self, request, pk=None):
#         pass
    
# class WorkshopFullView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     permission_classes = (IsAuthenticatedOrReadOnly, )
    
#     def get(self, request, pk=None):
#         pass
class ConvertingView(APIView):  ## Sending images to MEshroom server 
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAdminUser, )
    
    def post(self, request, pk=None):
        folder_name = request.data.get('folder_name')
        folder_name = request.data.get('cloth_id')

        # try:
        #     aug_model = ArObject.objects.get(cloth=pk)
        #     print(aug_model.id)
        #     try:
        #         images_to_convert = ImagesToConvert.objects.all().filter(aug_model=aug_model.id)
        #         image_files = []
        #         for img in images_to_convert:
        #             image_files.append(('files', (img.convertingimages.name, img.convertingimages.file)))

                
        #         url = 'http://192.168.0.108:5000/bulkUpload'
        #         form_data = {'foldername':folder_name}
        #         server = requests.post(url, data=form_data, files=image_files)
        #         output = server.text
        #         print(output)
                
        #         return Response(output, status=status.HTTP_200_OK)
            
        #     except ImagesToConvert.DoesNotExist:
        #         return Response("There is no images to converty")
        # except ArObject.DoesNotExist:
        #     return Response("There is no such aug model")
        print(request.data)
        return Response("Recieved")
    
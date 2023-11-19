"""augworkshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from crokiclothes import views
from rest_framework import routers


urlpatterns = [
    path('clothes/', views.ClothesModelView.as_view()),
    path('clothes/<str:pk>', views.ClothesView.as_view()),
    path('clothes/AugModel/<str:pk>', views.ClothesAugView.as_view()),
    path('workshop/', views.WorkshopView.as_view()),
    # path('workshop/bottom_part_meshes', views.WorkshopBottomView.as_view()),
    # path('workshop/full_part_meshes', views.WorkshopFullView.as_view()),
    path('clothes-admin', views.ClothesModelViewV2.as_view()),
    path('clothes-admin/<str:pk>', views.ClothManagement.as_view()),
    path('clothes-admin/<str:pk>/coverimages', views.CoverImagesForCloth.as_view()),
    path('clothes-admin/<str:pk>/converting-images', views.ConvertingImagesForAugObject.as_view()),
    path('clothes-admin/<str:pk>/augmented-clothes', views.AugmentedObjView.as_view()),
    path('clothes-admin/<str:pk>/augmented-clothes/<str:mpk>/textures', views.AugmentedObjView.as_view()),
    path('aug-convert/<str:pk>', views.ConvertingView.as_view())
]
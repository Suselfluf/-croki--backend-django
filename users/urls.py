from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, IdentifyUser

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('identify/', IdentifyUser.as_view(), name="identify_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
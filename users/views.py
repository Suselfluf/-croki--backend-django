from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import NewUser
from .serializers import CustomUserSerializer, UserSerializaer
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from django.conf import settings
import jwt


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                serializer_res = serializer.data 
                return Response(serializer_res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class IdentifyUser(APIView):
    permission_classes = [AllowAny,]
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, pk=None):
        # print(request.headers.get('Authorization'))
        token = request.headers.get('Authorization').split(' ')[1]
        # print(token.split(' ')[1])
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        user = NewUser.objects.get(id=user_id)
        serializer = UserSerializaer(instance=user)
        
        # clothes = Clothes.objects.all()
        # serializer = ClothesSerializer(clothes,many=True)
        
        return Response(serializer.data)
          
    # def post(self, request):
    #     serializer = ClothesSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

import datetime 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

#------------------产生 token-------------------------

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        data = super().validate(attrs)
        data['message'] = 'success' 
        data['now'] = time 
        data['username'] = self.user.username
    
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer 

#------------------刷新 token-------------------------

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        data = super().validate(attrs)
        data['code'] = 'token_valid' 
        data['now'] = time 
        # data['username'] = self.user.username
        return data

class MyTokenRefreshView(TokenRefreshView):
    serializer_class =  MyTokenRefreshSerializer

#------------------验证 token-------------------------

class MyTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        super().validate(attrs)
        return {'code': 'token_valid'}

class MyTokenVerifyView(TokenVerifyView):
    serializer_class = MyTokenVerifySerializer
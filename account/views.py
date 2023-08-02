from rest_framework.views import APIView
from .serializers import RegisterSerializer, ActivationSerializer, UserSerializer
from rest_framework.response import Response
from .send_email import send_confirmation_email
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = permissions.AllowAny,

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirmation_email(user.email, 'http://127.0.0.1:8000/api/account/activate/?u='+str(user.activation_code))
            except:
                return Response({'message': 'Зарегистрирован, но не смог отправить код активации',
                                 'data': serializer.data}, status=201)

        return Response(serializer.data, status=201)


# class ActivationView(generics.GenericAPIView):
#     serializer_class = ActivationSerializer
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('Successfully activated', status=200)


class ActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User,  activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Успешно активирован', status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = permissions.IsAdminUser,


class LogoutView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response('Вы вышли из системы', status=205)
        except:
            return Response('Что-то пошло не так', status=400)






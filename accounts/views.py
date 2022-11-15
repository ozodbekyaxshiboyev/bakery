from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, GenericAPIView,CreateAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, status, generics, response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer, UserChangePasswordSerializer
from .models import User
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken



class UserListMixinGenericAPIView(GenericAPIView, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data, context={'nimadir': 'biron_nima'})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, context={'nimadir':'biron_nima'})
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_200_OK)



class LoginAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserChangePasswordView(UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    model = User
    permission_classes = []

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


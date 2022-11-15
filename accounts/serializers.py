from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.forms import model_to_dict
from rest_framework_simplejwt.tokens import RefreshToken
from .enums import UserRoles
from rest_framework.exceptions import ValidationError

class UserChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)


    def validate(self, attrs):
        new = attrs.get('new_password')
        new1 = attrs.get('new_password1')
        if new1 == new:
            raise serializers.ValidationError("Xatolik! Yangi parollar ikki xil kiritildi!")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


    def create(self, validated_data):
        role = validated_data.get('role')
        if role is not None and role != UserRoles.client.value:
            raise ValidationError({'Xatolik':'Xaridor roledan boshqa rol yaratib bo`lmaydi'})

        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()
    token_class = RefreshToken
    # self.fields["password"] = PasswordField()

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def validate(self, attrs):
        authenticate_kwargs = {
            'phone_number': attrs['phone_number'],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        user = authenticate(**authenticate_kwargs)
        refresh = self.get_token(user)

        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        # attrs['user_id'] = user.id

        del attrs['phone_number'], attrs['password']

        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)

        return attrs

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = RefreshToken(attrs['refresh'])
        print(dir(token))
        try:
            token.blacklist()
        except AttributeError:
            pass
        return {}

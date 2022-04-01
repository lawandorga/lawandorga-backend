from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import ParseError, ValidationError
from config.authentication import RefreshPrivateKeyToken
from apps.api.serializers import RlcSerializer
from apps.api.models import RlcUser, UserProfile
from rest_framework import serializers
from django.db import transaction


###
# UserProfile
###
class RlcUserCreateSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "password",
            "password_confirm",
            "email",
            "name",
            "rlc",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise ValidationError('Both passwords must be equal.')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        user = UserProfile(**validated_data)
        user.set_password(password)
        with transaction.atomic():
            user.save()
            rlc_user = RlcUser(user=user, email_confirmed=False)
            rlc_user.save()
            rlc_user.send_email_confirmation_email()
        return user


###
# RlcUser
###
class RlcUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    email = serializers.SerializerMethodField('get_email')

    class Meta:
        model = RlcUser
        fields = '__all__'

    def get_name(self, obj):
        return obj.user.name

    def get_email(self, obj):
        return obj.user.email


class RlcUserUpdateSerializer(RlcUserSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = RlcUser
        fields = ['name', 'phone_number', 'birthday', 'street', 'city', 'postal_code', 'is_active', 'note']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if (
            'is_active' in attrs and
            self.instance.pk == self.context['request'].user.rlc_user.pk and
            attrs['is_active'] is False
        ):
            raise ParseError('You can not deactivate yourself.')
        return attrs

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if 'name' in validated_data:
            instance.user.name = validated_data['name']
            instance.user.save()
        return instance


class RlcUserForeignSerializer(RlcUserSerializer):
    class Meta:
        model = RlcUser
        fields = ["user", "id", "phone_number", 'name', 'email']


###
# JWT
###
class RlcUserJWTSerializer(TokenObtainSerializer):
    token_class = RefreshPrivateKeyToken

    def get_token(self, user):
        return self.token_class.for_user(user, password_user=self.initial_data['password'])

    def validate(self, attrs):
        data = super().validate(attrs)

        if not hasattr(self.user, 'rlc_user'):
            raise ValidationError("You don't have the necessary role to be able to login here.")

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data['user'] = RlcUserSerializer(self.user.rlc_user).data
        data['rlc'] = RlcSerializer(self.user.rlc).data
        data['permissions'] = self.user.get_all_user_permissions()

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


###
# Other
###
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserPasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()
    new_password_confirm = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise ValidationError('The passwords do not match.')
        return attrs

# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import serializers

from .services import get_user_photo_url, get_user_big_photo_url
from .gravatar import get_user_gravatar_id
from .models import User

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re

######################################################
# User
######################################################

class UserSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    big_photo = serializers.SerializerMethodField()
    gravatar_id = serializers.SerializerMethodField()
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email','full_name', 'bio',
         'is_active','photo', 'big_photo', 'gravatar_id',)

    def get_photo(self, user):
        return get_user_photo_url(user)

    def get_big_photo(self, user):
        return get_user_big_photo_url(user)

    def get_gravatar_id(self, user):
        return get_user_gravatar_id(user)

class UserAdminSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('email', )

class UserPhotoValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('photo',)


class RecoveryValidator(serializers.Serializer):
    token = serializers.CharField(max_length=200)
    password = serializers.CharField(min_length=6)


class ChangeEmailValidator(serializers.Serializer):
    email_token = serializers.CharField(max_length=200)


class CancelAccountValidator(serializers.Serializer):
    cancel_token = serializers.CharField(max_length=200)

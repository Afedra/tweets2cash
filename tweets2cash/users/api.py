# -*- coding: utf-8 -*-

import uuid

from django.apps import apps
from django.utils.translation import ugettext as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

from rest_framework import exceptions as exc
from rest_framework import filters
from rest_framework import response
from tweets2cash.auth.tokens import get_user_for_token
from tweets2cash.base.mails import mail_builder
from tweets2cash.auth.services import send_register_email
from rest_framework.decorators import list_route, detail_route
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from .services import get_user_by_username_or_email
from easy_thumbnails.source_generators import pil_image
from rest_framework.permissions import IsAuthenticated, AllowAny

from . import models
from . import serializers
from . import permissions
from . import services
from . import filters
from .signals import user_cancel_account as user_cancel_account_signal
from .signals import user_change_email as user_change_email_signal
from .throttling import UserDetailRateThrottle, UserUpdateRateThrottle
import string
import random

class UsersViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,permissions.IsTheSameUser,)
    admin_serializer_class = serializers.UserAdminSerializer
    serializer_class = serializers.UserSerializer
    filter_backends = (filters.UserFilterBackend,)
    throttle_classes = (UserDetailRateThrottle, UserUpdateRateThrottle)
    model = models.User

    def get_serializer_class(self):

        if self.action in ["partial_update",]:
            return serializers.UserSerializer

        if self.action in ["update","by_username", "retrieve",]:
            if self.request.user.is_superuser:
                return self.admin_serializer_class

        if self.action in ["change_avatar",]:
            return serializers.UserPhotoValidator

        return self.serializer_class

    def get_queryset(self):
        if self.queryset is not None:
            qs = self.queryset._clone()
        elif self.model is not None:
            qs = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(("'%s' must define 'queryset' or 'model'" % self.__class__.__name__))

        return qs

    def get_permissions(self):
        if self.action in ["password_recovery","by_username",]:
            self.permission_classes = (AllowAny,)

        return super(self.__class__, self).get_permissions()

    def create(self, *args, **kwargs):
        raise exc.NotSupported()

    def list(self, request, *args, **kwargs):
        self.object_list = filters.UserFilterBackend().filter_queryset(request,
                                                                  self.get_queryset(),
                                                                  self)
        page = self.paginate_queryset(self.object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)
        return response.Ok(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        self.object_list = filters.UserFilterBackend().filter_queryset(request,
                                                                  self.get_queryset(),
                                                                  self)
        self.object = get_object_or_404(self.object_list, **kwargs)
        serializer = self.get_serializer(self.object)
        return response.Ok(serializer.data)

    def validate_user_email_allowed_domains(self, value):

        domain_name = value.split("@")[1]

        if settings.USER_EMAIL_ALLOWED_DOMAINS and domain_name not in settings.USER_EMAIL_ALLOWED_DOMAINS:
            raise ValidationError(_("You email domain is not allowed"))

    # TODO: commit_on_success
    def partial_update(self, request, *args, **kwargs):
        """
        We must detect if the user is trying to change his email so we can
        save that value and generate a token that allows him to validate it in
        the new email account
        """

        new_email = request.data.pop('email', None)

        if new_email is not None:
            valid_new_email = True
            duplicated_email = models.User.objects.filter(email=new_email).exists()

            try:
                validate_email(new_email)
                self.validate_user_email_allowed_domains(new_email)
            except ValidationError:
                valid_new_email = False

            valid_new_email = valid_new_email and new_email != request.user.email

            if duplicated_email:
                raise exc.WrongArguments(_("Duplicated email"))
            elif not valid_new_email:
                raise exc.WrongArguments(_("Not valid email"))

            # We need to generate a token for the email
            request.user.email_token = str(uuid.uuid1())
            request.user.new_email = new_email
            request.user.save(update_fields=["email_token", "new_email"])
            email = mail_builder.change_email(
                request.user.new_email,
                {
                    "user": request.user
                }
            )
            email.send()

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        user = self.get_object()
        stream = request.stream
        request_data = stream is not None and stream.GET or None
        user_cancel_account_signal.send(sender=user.__class__, user=user, request_data=request_data)
        user.cancel()
        return response.NoContent()


    @list_route(methods=["GET"])
    def by_username(self, request, *args, **kwargs):
        username = request.query_params.get("username", None)
        return self.retrieve(request, username=username)

    @list_route(methods=["POST"])
    def password_recovery(self, request, pk=None):
        username_or_email = request.data.get('username', None)


        if not username_or_email:
            raise exc.WrongArguments(_("Invalid username or email"))

        user = get_user_by_username_or_email(username_or_email)
        user.token = str(uuid.uuid1())
        user.save(update_fields=["token"])

        email = mail_builder.password_recovery(user, {"user": user})
        email.send()

        return response.Ok({"detail": _("A Mail has been sent to you successful!")})

    @list_route(methods=["POST"])
    def change_password_from_recovery(self, request, pk=None):
        """
        Change password with token (from password recovery step).
        """
        validator = serializers.RecoveryValidator(data=request.data, many=False)

        if not validator.is_valid():
            raise exc.WrongArguments(_("Token is invalid"))

        try:
            user = models.User.objects.get(token=validator.data["token"])
        except models.User.DoesNotExist:
            raise exc.WrongArguments(_("Token is invalid"))

        user.set_password(validator.data["password"])
        user.token = None
        user.save(update_fields=["password", "token"])

        return response.NoContent()

    @list_route(methods=["POST"])
    def change_password(self, request, pk=None):
        """
        Change password to current logged user.
        """

        current_password = request.data.get("current_password")
        password = request.data.get("password")

        if not current_password:
            raise exc.WrongArguments(_("Current password parameter needed"))

        if not password:
            raise exc.WrongArguments(_("New password parameter needed"))

        if len(password) < 6:
            raise exc.WrongArguments(_("Invalid password length at least 6 charaters needed"))

        if current_password and not request.user.check_password(current_password):
            raise exc.WrongArguments(_("Invalid current password"))

        request.user.set_password(password)
        request.user.save(update_fields=["password"])
        return response.NoContent()

    @list_route(methods=["POST"])
    def change_avatar(self, request):
        """
        Change avatar to current logged user.
        """
        avatar = request.FILES.get('avatar', None)
        id = request.data.get('id', None)
        if not avatar:
            raise exc.WrongArguments(_("Incomplete arguments"))

        try:
            pil_image(avatar)
        except Exception:
            raise exc.WrongArguments(_("Invalid image format"))

        if id is None:
            request.user.photo = avatar
            request.user.save(update_fields=["photo"])
            user_data = self.admin_serializer_class(request.user).data
        else:
            user = get_object_or_404(models.User, id=id)
            user.photo = avatar
            user.save(update_fields=["photo"])
            user_data = self.admin_serializer_class(user).data

        return response.Ok(user_data)

    @list_route(methods=["POST"])
    def remove_avatar(self, request):
        """
        Remove the avatar of current logged user.
        """
        request.user.photo = None
        request.user.save(update_fields=["photo"])
        user_data = self.admin_serializer_class(request.user).data
        return response.Ok(user_data)

    @list_route(methods=["POST"])
    def change_email(self, request, pk=None):
        """
        Verify the email change to current logged user.
        """
        validator = serializers.ChangeEmailValidator(data=request.data, many=False)
        if not validator.is_valid():
            raise exc.WrongArguments(_("Invalid, are you sure the token is correct and you "
                                       "didn't use it before?"))

        try:
            user = models.User.objects.get(email_token=validator.data["email_token"])
        except models.User.DoesNotExist:
            raise exc.WrongArguments(_("Invalid, are you sure the token is correct and you "
                                       "didn't use it before?"))


        old_email = user.email
        new_email = user.new_email

        user.email = new_email
        user.new_email = None
        user.email_token = None
        user.save(update_fields=["email", "new_email", "email_token"])

        user_change_email_signal.send(sender=user.__class__,
                                      user=user,
                                      old_email=old_email,
                                      new_email=new_email)

        return response.NoContent()

    @list_route(methods=["GET"])
    def me(self, request, pk=None):
        """
        Get me.
        """
        user_data = self.admin_serializer_class(request.user).data
        return response.Ok(user_data)

    @list_route(methods=["POST"])
    def cancel(self, request, pk=None):
        """
        Cancel an account via token
        """
        validator = serializers.CancelAccountValidator(data=request.data, many=False)
        if not validator.is_valid():
            raise exc.WrongArguments(_("Invalid, are you sure the token is correct?"))

        try:
            max_age_cancel_account = getattr(settings, "MAX_AGE_CANCEL_ACCOUNT", None)
            user = get_user_for_token(validator.data["cancel_token"], "cancel_account",
                                      max_age=max_age_cancel_account)

        except exc.NotAuthenticated:
            raise exc.WrongArguments(_("Invalid, are you sure the token is correct?"))

        if not user.is_active:
            raise exc.WrongArguments(_("Invalid, are you sure the token is correct?"))

        user.cancel()
        return response.NoContent()

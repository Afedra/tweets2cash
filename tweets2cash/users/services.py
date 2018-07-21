# -*- coding: utf-8 -*-
"""
This model contains a domain logic for users application.
"""

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext as _
from django.apps import apps

from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError

from rest_framework import exceptions as exc
from tweets2cash.base.utils.urls import get_absolute_url


def get_user_by_username_or_email(username_or_email):
    user_model = get_user_model()
    qs = user_model.objects.filter(Q(username__iexact=username_or_email) |
                                   Q(email__iexact=username_or_email))

    if len(qs) > 1:
        qs = qs.filter(Q(username=username_or_email) |
                       Q(email=username_or_email))

    if len(qs) == 0:
        raise exc.WrongArguments(_("Username or password does not match user."))

    user = qs[0]
    return user


def get_and_validate_user(*, username: str, password: str) -> bool:
    """
    Check if user with username/email exists and specified
    password matchs well with existing user password.

    if user is valid,  user is returned else, corresponding
    exception is raised.
    """

    user = get_user_by_username_or_email(username)
    if not user.check_password(password):
        raise exc.WrongArguments(_("Username or password does not match user."))

    return user


def get_photo_url(photo):
    """Get a photo absolute url and the photo automatically cropped."""
    if not photo:
        return None
    try:
        url = get_thumbnailer(photo)[settings.THN_AVATAR_SMALL].url
        return get_absolute_url(url)
    except InvalidImageFormatError as e:
        return None


def get_user_photo_url(user):
    """Get the user's photo url."""
    if not user:
        return None
    return get_photo_url(user.photo)


def get_big_photo_url(photo):
    """Get a big photo absolute url and the photo automatically cropped."""
    if not photo:
        return None
    try:
        url = get_thumbnailer(photo)[settings.THN_AVATAR_BIG].url
        return get_absolute_url(url)
    except InvalidImageFormatError as e:
        return None


def get_user_big_photo_url(user):
    """Get the user's big photo url."""
    if not user:
        return None
    return get_big_photo_url(user.photo)


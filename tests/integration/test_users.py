# -*- coding: utf-8 -*-

import pytest
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.files import File
from django.core.cache import cache as default_cache

from .. import factories as f
from ..utils import DUMMY_BMP_DATA

from tweets2cash.base.utils import json
from tweets2cash.base.utils.thumbnails import get_thumbnail_url
from tweets2cash.base.utils.dicts import into_namedtuple
from tweets2cash.users import models
from tweets2cash.auth.tokens import get_token_for_user

from easy_thumbnails.files import generate_all_aliases, get_thumbnailer

import os

pytestmark = pytest.mark.django_db


##############################
## Create user
##############################

def test_users_create_through_standard_api(client):
    user = f.UserFactory.create(is_superuser=True)

    url = reverse('users-list')
    data = {}

    response = client.post(url, json.dumps(data), content_type="application/json")
    assert response.status_code == 401

    client.login(user)

    response = client.post(url, json.dumps(data), content_type="application/json")
    assert response.status_code == 405


##############################
## Change email
##############################

def test_update_user_with_same_email(client):
    user = f.UserFactory.create(email="same@email.com")
    url = reverse('users-detail', kwargs={"pk": user.pk})
    data = {"email": "same@email.com"}

    client.login(user)
    response = client.patch(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 400
    assert response.data['_error_message'] == 'Duplicated email'

    user.refresh_from_db()
    assert user.email == "same@email.com"


def test_update_user_with_duplicated_email(client):
    f.UserFactory.create(email="one@email.com")
    user = f.UserFactory.create(email="two@email.com")
    url = reverse('users-detail', kwargs={"pk": user.pk})
    data = {"email": "one@email.com"}

    client.login(user)
    response = client.patch(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 400
    assert response.data['_error_message'] == 'Duplicated email'

    user.refresh_from_db()
    assert user.email == "two@email.com"


def test_update_user_with_invalid_email(client):
    user = f.UserFactory.create(email="my@email.com")
    url = reverse('users-detail', kwargs={"pk": user.pk})
    data = {"email": "my@email"}

    client.login(user)
    response = client.patch(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 400
    assert response.data['_error_message'] == 'Not valid email'

    user.refresh_from_db()
    assert user.email == "my@email.com"


def test_update_user_with_unallowed_domain_email(client, settings):
    settings.USER_EMAIL_ALLOWED_DOMAINS = ['email.com']
    user = f.UserFactory.create(email="my@email.com")
    url = reverse('users-detail', kwargs={"pk": user.pk})
    data = {"email": "my@invalid-email.com"}

    client.login(user)
    response = client.patch(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 400
    assert response.data['_error_message'] == 'Not valid email'

    user.refresh_from_db()
    assert user.email == "my@email.com"

def test_update_user_with_allowed_domain_email(client, settings):
    settings.USER_EMAIL_ALLOWED_DOMAINS = ['email.com']

    user = f.UserFactory.create(email="old@email.com")
    url = reverse('users-detail', kwargs={"pk": user.pk})
    data = {"email": "new@email.com"}

    client.login(user)
    response = client.patch(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 200

    user.refresh_from_db()
    assert user.email == "old@email.com"
    assert user.email_token is not None
    assert user.new_email == "new@email.com"


def test_update_user_with_valid_email(client):
    user = f.UserFactory.create(email="old@email.com")
    url = reverse('users-detail', kwargs={"pk": user.pk})
    data = {"email": "new@email.com"}

    client.login(user)
    response = client.patch(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.email == "old@email.com"
    assert user.email_token is not None
    assert user.new_email == "new@email.com"


def test_validate_requested_email_change(client):
    user = f.UserFactory.create(email="old@email.com", email_token="change_email_token", new_email="new@email.com")
    url = reverse('users-change-email')
    data = {"email_token": "change_email_token"}

    client.login(user)
    response = client.post(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 204
    user.refresh_from_db()
    assert user.email_token is None
    assert user.new_email is None
    assert user.email == "new@email.com"


def test_validate_requested_email_change_for_anonymous_user(client):
    user = f.UserFactory.create(email="old@email.com", email_token="change_email_token", new_email="new@email.com")
    url = reverse('users-change-email')
    data = {"email_token": "change_email_token"}

    client.login(user)
    response = client.post(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 204
    user.refresh_from_db()
    assert user.email_token is None
    assert user.new_email is None
    assert user.email == "new@email.com"


def test_validate_requested_email_change_without_token(client):
    user = f.UserFactory.create(email_token="change_email_token", new_email="new@email.com")
    url = reverse('users-change-email')
    data = {}

    client.login(user)
    response = client.post(url, json.dumps(data), content_type="application/json")
    assert response.status_code == 400


def test_validate_requested_email_change_with_invalid_token(client):
    user = f.UserFactory.create(email_token="change_email_token", new_email="new@email.com")
    url = reverse('users-change-email')
    data = {"email_token": "invalid_email_token"}

    client.login(user)
    response = client.post(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 400


##############################
## Delete user
##############################

def test_delete_self_user(client):
    user = f.UserFactory.create()
    url = reverse('users-detail', kwargs={"pk": user.pk})

    client.login(user)
    response = client.delete(url)

    assert response.status_code == 204
    user = models.User.objects.get(pk=user.id)
    assert user.full_name == "Deleted user"



##############################
## Cancel account
##############################

def test_cancel_self_user_with_valid_token(client):
    user = f.UserFactory.create()
    url = reverse('users-cancel')
    cancel_token = get_token_for_user(user, "cancel_account")
    data = {"cancel_token": cancel_token}
    client.login(user)
    response = client.post(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 204
    user = models.User.objects.get(pk=user.id)
    assert user.full_name == "Deleted user"


def test_cancel_self_user_with_invalid_token(client):
    user = f.UserFactory.create()
    url = reverse('users-cancel')
    data = {"cancel_token": "invalid_cancel_token"}
    client.login(user)
    response = client.post(url, json.dumps(data), content_type="application/json")

    assert response.status_code == 400


##############################
## Avatar
##############################

def test_change_avatar(client):
    url = reverse('users-change-avatar')

    user = f.UserFactory()
    client.login(user)

    with NamedTemporaryFile() as avatar:
        # Test no avatar send
        post_data = {}
        response = client.post(url, post_data)
        assert response.status_code == 400

        # Test invalid file send
        post_data = {
            'avatar': avatar
        }
        response = client.post(url, post_data)
        assert response.status_code == 400

        # Test empty valid avatar send
        avatar.write(DUMMY_BMP_DATA)
        avatar.seek(0)
        response = client.post(url, post_data)
        assert response.status_code == 200


def test_change_avatar_with_long_file_name(client):
    url = reverse('users-change-avatar')
    user = f.UserFactory()

    with NamedTemporaryFile(delete=False) as avatar:
        avatar.name=500*"x"+".bmp"
        avatar.write(DUMMY_BMP_DATA)
        avatar.seek(0)

        client.login(user)
        post_data = {'avatar': avatar}
        response = client.post(url, post_data)

        assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_change_avatar_removes_the_old_one(client):
    url = reverse('users-change-avatar')
    user = f.UserFactory()

    with NamedTemporaryFile(delete=False) as avatar:
        avatar.write(DUMMY_BMP_DATA)
        avatar.seek(0)
        user.photo = File(avatar)
        user.save()
        generate_all_aliases(user.photo, include_global=True)

    with NamedTemporaryFile(delete=False) as avatar:
        thumbnailer = get_thumbnailer(user.photo)
        original_photo_paths = [user.photo.path]
        original_photo_paths += [th.path for th in thumbnailer.get_thumbnails()]
        assert all(list(map(os.path.exists, original_photo_paths)))

        client.login(user)
        avatar.write(DUMMY_BMP_DATA)
        avatar.seek(0)
        post_data = {'avatar': avatar}
        response = client.post(url, post_data)

        assert response.status_code == 200
        assert not any(list(map(os.path.exists, original_photo_paths)))


@pytest.mark.django_db(transaction=True)
def test_remove_avatar(client):
    url = reverse('users-remove-avatar')
    user = f.UserFactory()

    with NamedTemporaryFile(delete=False) as avatar:
        avatar.write(DUMMY_BMP_DATA)
        avatar.seek(0)
        user.photo = File(avatar)
        user.save()
        generate_all_aliases(user.photo, include_global=True)

    thumbnailer = get_thumbnailer(user.photo)
    original_photo_paths = [user.photo.path]
    original_photo_paths += [th.path for th in thumbnailer.get_thumbnails()]
    assert all(list(map(os.path.exists, original_photo_paths)))

    client.login(user)
    response = client.post(url)

    assert response.status_code == 200
    assert not any(list(map(os.path.exists, original_photo_paths)))

##############################
## Mail permissions
##############################

def test_mail_permissions(client):
    user_1 = f.UserFactory.create(is_superuser=True)
    user_2 = f.UserFactory.create()

    url1 = reverse('users-detail', kwargs={"pk": user_1.pk})
    url2 = reverse('users-detail', kwargs={"pk": user_2.pk})

    # Anonymous user
    response = client.json.get(url1)
    assert response.status_code == 401
    assert "email" not in response.data

    client.login(user_1)

    # Superuser
    response = client.json.get(url1)
    assert response.status_code == 200
    assert "email" in response.data

    response = client.json.get(url2)
    assert response.status_code == 200
    assert "email" in response.data

    # Normal user
    client.login(user_2)

    response = client.json.get(url1)
    assert response.status_code == 404

    response = client.json.get(url2)
    assert response.status_code == 200
    assert "email" in response.data



##############################
## Retrieve user
##############################

def test_users_retrieve_throttling_api(client):
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user-detail"] = "1/minute"

    user = f.UserFactory.create()

    url = reverse('users-detail', kwargs={"pk": user.pk})
    data = {}

    client.login(user)
    response = client.get(url, content_type="application/json")
    assert response.status_code == 200

    response = client.get(url, content_type="application/json")
    assert response.status_code == 429
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user-detail"] = None
    default_cache.clear()


def test_users_by_username_throttling_api(client):
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user-detail"] = "1/minute"
    user = f.UserFactory.create(username="test-user-detail")

    url = reverse('users-by-username')

    client.login(user)
    response = client.get(url, {"username": user.username}, content_type="application/json")
    assert response.status_code == 200

    response = client.get(url, {"username": user.username}, content_type="application/json")
    assert response.status_code == 429
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user-detail"] = None
    default_cache.clear()

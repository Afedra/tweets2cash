# -*- coding: utf-8 -*-

import pytest

from django.core.urlresolvers import reverse
from django.core import mail

from .. import factories

pytestmark = pytest.mark.django_db


@pytest.fixture
def register_form():
    return {"username": "username",
            "password": "password",
            "full_name": "fname",
            "email": "user@email.com",
            "type": "public"}


def test_respond_201_when_public_registration_is_enabled(client, settings, register_form):
    settings.PUBLIC_REGISTER_ENABLED = True
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 201


def test_respond_400_when_public_registration_is_disabled(client, register_form, settings):
    settings.PUBLIC_REGISTER_ENABLED = False
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 400


def test_respond_400_when_the_email_domain_isnt_in_allowed_domains(client, register_form, settings):
    settings.PUBLIC_REGISTER_ENABLED = True
    settings.USER_EMAIL_ALLOWED_DOMAINS = ['other-domain.com']
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 400


def test_respond_201_when_the_email_domain_is_in_allowed_domains(client, settings, register_form):
    settings.PUBLIC_REGISTER_ENABLED = True
    settings.USER_EMAIL_ALLOWED_DOMAINS = ['email.com']
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 201


def test_response_200_in_public_registration(client, settings):
    settings.PUBLIC_REGISTER_ENABLED = True
    form = {
        "type": "public",
        "username": "mmcfly",
        "full_name": "martin seamus mcfly",
        "email": "mmcfly@bttf.com",
        "password": "password",
    }

    response = client.post(reverse("auth-register"), form)
    assert response.status_code == 201
    assert response.data["username"] == "mmcfly"
    assert response.data["email"] == "mmcfly@bttf.com"
    assert response.data["full_name"] == "martin seamus mcfly"
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "Welcome to Tweets2Cash!"


def test_respond_400_if_username_is_invalid(client, settings, register_form):
    settings.PUBLIC_REGISTER_ENABLED = True

    register_form.update({"username": "User Examp:/e"})
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 400

    register_form.update({"username": 300*"a"})
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 400


def test_respond_400_if_username_or_email_is_duplicate(client, settings, register_form):
    settings.PUBLIC_REGISTER_ENABLED = True

    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 201

    register_form["username"] = "username"
    register_form["email"] = "ff@dd.com"
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 400


def test_auth_uppercase_ignore(client, settings):
    settings.PUBLIC_REGISTER_ENABLED = True

    register_form = {"username": "Username",
                     "password": "password",
                     "full_name": "fname",
                     "email": "User@email.com",
                     "type": "public"}
    response = client.post(reverse("auth-register"), register_form)

    #Only exists one user with the same lowercase version of username/password
    login_form = {"type": "normal",
                  "username": "Username",
                  "password": "password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 200

    login_form = {"type": "normal",
                  "username": "User@email.com",
                  "password": "password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 200

    #Now we have two users with the same lowercase version of username/password
    # 1.- The capitalized version works
    register_form = {"username": "username",
                     "password": "password",
                     "full_name": "fname",
                     "email": "user@email.com",
                     "type": "public"}
    response = client.post(reverse("auth-register"), register_form)

    login_form = {"type": "normal",
                  "username": "Username",
                  "password": "password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 200

    login_form = {"type": "normal",
                  "username": "User@email.com",
                  "password": "password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 200

    # 2.- If we capitalize
    login_form = {"type": "normal",
                  "username": "uSername",
                  "password": "password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 200

    login_form = {"type": "normal",
                  "username": "uSer@email.com",
                  "password": "password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 200


def test_login_fail_throttling(client, settings):
    settings.PUBLIC_REGISTER_ENABLED = True
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["login-fail"] = "1/minute"

    register_form = {"username": "valid_username_login_fail",
                     "password": "valid_password",
                     "full_name": "fullname",
                     "email": "valid_username_login_fail@email.com",
                     "type": "public"}
    response = client.post(reverse("auth-register"), register_form)

    login_form = {"type": "normal",
                  "username": "valid_username_login_fail",
                  "password": "valid_password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 200

    login_form = {"type": "normal",
                  "username": "invalid_username_login_fail",
                  "password": "invalid_password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 400

    login_form = {"type": "normal",
                  "username": "invalid_username_login_fail",
                  "password": "invalid_password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 429

    login_form = {"type": "normal",
                  "username": "valid_username_login_fail",
                  "password": "valid_password"}

    response = client.post(reverse("auth-list"), login_form)
    assert response.status_code == 429

    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["login-fail"] = None

def test_register_success_throttling(client, settings):
    settings.PUBLIC_REGISTER_ENABLED = True
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["register-success"] = "1/minute"

    register_form = {"username": "valid_username_register_success",
                     "password": "valid_password",
                     "full_name": "fullname",
                     "email": "",
                     "type": "public"}
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 400

    register_form = {"username": "valid_username_register_success",
                     "password": "valid_password",
                     "full_name": "fullname",
                     "email": "valid_username_register_success@email.com",
                     "type": "public"}
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 201

    register_form = {"username": "valid_username_register_success2",
                     "password": "valid_password2",
                     "full_name": "fullname",
                     "email": "valid_username_register_success2@email.com",
                     "type": "public"}
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 429

    register_form = {"username": "valid_username_register_success2",
                     "password": "valid_password2",
                     "full_name": "fullname",
                     "email": "",
                     "type": "public"}
    response = client.post(reverse("auth-register"), register_form)
    assert response.status_code == 429

    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["register-success"] = None

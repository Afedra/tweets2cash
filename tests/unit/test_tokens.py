# -*- coding: utf-8 -*-

import pytest

from .. import factories as f

from rest_framework import exceptions as exc
from tweets2cash.auth.tokens import get_token_for_user, get_user_for_token


pytestmark = pytest.mark.django_db


def test_valid_token():
    user = f.UserFactory.create(email="old@email.com")
    token = get_token_for_user(user, "testing_scope")
    user_from_token = get_user_for_token(token, "testing_scope")
    assert user.id == user_from_token.id


@pytest.mark.xfail(raises=exc.NotAuthenticated)
def test_invalid_token():
    f.UserFactory.create(email="old@email.com")
    get_user_for_token("testing_invalid_token", "testing_scope")


@pytest.mark.xfail(raises=exc.NotAuthenticated)
def test_invalid_token_expiration():
    user = f.UserFactory.create(email="old@email.com")
    token = get_token_for_user(user, "testing_scope")
    get_user_for_token(token, "testing_scope", max_age=1)


@pytest.mark.xfail(raises=exc.NotAuthenticated)
def test_invalid_token_scope():
    user = f.UserFactory.create(email="old@email.com")
    token = get_token_for_user(user, "testing_scope")
    get_user_for_token(token, "testing_invalid_scope")

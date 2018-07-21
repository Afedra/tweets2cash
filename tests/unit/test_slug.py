# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from tweets2cash.base.utils.slug import slugify

import pytest
pytestmark = pytest.mark.django_db


def test_slugify_1():
    assert slugify("漢字") == "han-zi"


def test_slugify_2():
    assert slugify("TestExamplePage") == "testexamplepage"


def test_slugify_3():
    assert slugify(None) == ""

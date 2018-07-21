# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from sampledatahelper.helper import SampleDataHelper

from tweets2cash.users.models import *

BASE_USERS = getattr(settings, "SAMPLE_DATA_BASE_USERS", {})
NUM_USERS = getattr(settings, "SAMPLE_DATA_NUM_USERS", 10)
NUM_APPLICATIONS = getattr(settings, "SAMPLE_DATA_NUM_APPLICATIONS", (1, 3))
NUM_APPLICATIONS_TOKENS = getattr(settings, "SAMPLE_DATA_NUM_APPLICATIONS_TOKENS", (1, 3))


class Command(BaseCommand):
    sd = SampleDataHelper(seed=12345678901)

    @transaction.atomic
    def handle(self, *args, **options):

        self.users = [User.objects.get(is_superuser=True)]

        # create users
        if BASE_USERS:
            for username, full_name, email in BASE_USERS:
                self.users.append(self.create_user(username=username, full_name=full_name, email=email))
        else:
            for x in range(NUM_USERS):
                self.users.append(self.create_user(counter=x))


    def create_user(self, counter=None, username=None, full_name=None, email=None):
        counter = counter or self.sd.int()
        username = username or "user{0}".format(counter)
        full_name = full_name or "{} {}".format(self.sd.name('es'), self.sd.surname('es', number=1))
        email = email or "user{0}@tweets2cash.demo".format(counter)

        user = User.objects.create(username=username,
                                   full_name=full_name,
                                   email=email,
                                   token=self.sd.hex_chars(10,10)))

        user.set_password('123123')
        user.save()

        return user

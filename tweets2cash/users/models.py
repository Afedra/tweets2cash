# -*- coding: utf-8 -*-

from importlib import import_module

from django.apps import apps
from django.apps.config import MODELS_MODULE_NAME
from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractBaseUser
from django.core.exceptions import AppRegistryNotReady
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.contrib.postgres.fields import ArrayField

from tweets2cash.base.db.models.fields import JSONField
from django_pglocks import advisory_lock
from tweets2cash.base.utils.slug import slugify_uniquely_for_queryset
from tweets2cash.base.utils.colors import generate_random_hex_color
from tweets2cash.base.utils.slug import slugify_uniquely
from tweets2cash.base.utils.files import get_file_path
from tweets2cash.base.utils.time import timestamp_ms
from tweets2cash.auth.tokens import get_token_for_user
from django.core.exceptions import ValidationError


def get_user_model_safe():
    """
    Fetches the user model using the app registry.
    This doesn't require that an app with the given app label exists,
    which makes it safe to call when the registry is being populated.
    All other methods to access models might raise an exception about the
    registry not being ready yet.
    Raises LookupError if model isn't found.

    Based on: https://github.com/django-oscar/django-oscar/blob/1.0/oscar/core/loading.py#L310-L340
    Ongoing Django issue: https://code.djangoproject.com/ticket/22872
    """
    user_app, user_model = settings.AUTH_USER_MODEL.split('.')

    try:
        return apps.get_model(user_app, user_model)
    except AppRegistryNotReady:
        if apps.apps_ready and not apps.models_ready:
            # If this function is called while `apps.populate()` is
            # loading models, ensure that the module that defines the
            # target model has been imported and try looking the model up
            # in the app registry. This effectively emulates
            # `from path.to.app.models import Model` where we use
            # `Model = get_model('app', 'Model')` instead.
            app_config = apps.get_app_config(user_app)
            # `app_config.import_models()` cannot be used here because it
            # would interfere with `apps.populate()`.
            import_module('%s.%s' % (app_config.name, MODELS_MODULE_NAME))
            # In order to account for case-insensitivity of model_name,
            # look up the model through a private API of the app registry.
            return apps.get_registered_model(user_app, user_model)
        else:
            # This must be a different case (e.g. the model really doesn't
            # exist). We just re-raise the exception.
            raise


def get_user_file_path(instance, filename):
    return get_file_path(instance, filename, "user")


class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django"s Permission model using the ModelBackend.
    """
    is_superuser = models.BooleanField(_("superuser status"), default=False,
        help_text=_("Designates that this user has all permissions without "
                    "explicitly assigning them."))

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), max_length=255, blank=True, unique=True)
    is_active = models.BooleanField(_("active"), default=True,
        help_text=_("Designates whether this user should be treated as "
                    "active. Unselect this instead of deleting accounts."))

    full_name = models.CharField(_("full name"), max_length=256, blank=True)
    bio = models.TextField(null=False, blank=True, default="", verbose_name=_("biography"))
    photo = models.FileField(upload_to=get_user_file_path,
                             max_length=500, null=True, blank=True,
                             verbose_name=_("photo"))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    date_of_birth = models.DateTimeField(null=True, blank=True,
                                        verbose_name=_("date of birth"))
    gender = models.CharField(max_length=100, null=True, blank=True, default="",
                            verbose_name=_("gender"))
    token = models.CharField(max_length=200, null=True, blank=True, default=None,
                             verbose_name=_("token"))
    email_token = models.CharField(max_length=200, null=True, blank=True, default=None,
                         verbose_name=_("email token"))
    new_email = models.EmailField(_("new email address"), null=True, blank=True)
    is_system = models.BooleanField(null=False, blank=False, default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.username

    def get_full_name(self):
        return self.full_name or self.username or self.email

    def save(self, *args, **kwargs):
        get_token_for_user(self, "cancel_account")
        if not self.email:
            self.email = self.username + "@tweets2cash.com"
        super().save(*args, **kwargs)

    def cancel(self):
        with advisory_lock("delete-user"):
            deleted_user_prefix = "deleted-user-{}".format(timestamp_ms())
            self.username = slugify_uniquely(deleted_user_prefix, User, slugfield="username")
            self.email = "{}@tweets2cash.com".format(self.username)
            self.is_active = False
            self.full_name = "Deleted user"
            self.bio = ""
            self.token = None
            self.set_unusable_password()
            self.photo = None
            self.save()

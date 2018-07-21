# -*- coding: utf-8 -*-

from functools import partial

from django.utils.translation import ugettext as _
from django.conf import settings

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework import exceptions as exc
from rest_framework import response

from .validators import PublicRegisterValidator

from .services import public_register
from .services import make_auth_response_data
from .services import get_auth_plugins

from rest_framework.permissions import AllowAny
from .throttling import LoginFailRateThrottle, RegisterSuccessRateThrottle


def _parse_data(data:dict, *, cls):
    """
    Generic function for parse user data using
    specified validator on `cls` keyword parameter.

    Raises: RequestValidationError exception if
    some errors found when data is validated.

    Returns the parsed data.
    """

    validator = cls(data=data)
    if not validator.is_valid():
        raise exc.RequestValidationError(validator.errors)
    return validator.data

# Parse public register data
parse_public_register_data = partial(_parse_data, cls=PublicRegisterValidator)

class AuthViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    throttle_classes = (LoginFailRateThrottle, RegisterSuccessRateThrottle)
    response = None

    def get_permissions(self):
        if self.action in ["create", "register"]:
            self.permission_classes = [AllowAny,]

        return super(self.__class__, self).get_permissions()

    def _public_register(self, request):
        if not settings.PUBLIC_REGISTER_ENABLED:
            raise exc.BadRequest(_("Public register is disabled."))

        try:
            data = parse_public_register_data(request.data)
            user = public_register(**data)
        except exc.IntegrityError as e:
            raise exc.BadRequest(e.detail)

        data = make_auth_response_data(user)
        return response.Created(data)

    @list_route(methods=["POST"])
    def register(self, request, **kwargs):

        if request.data.get("type", None) == "public":
            return self._public_register(request)
        raise exc.BadRequest(_("invalid register type"))


    # Login view: /api/v1/auth
    def create(self, request, **kwargs):
        auth_plugins = get_auth_plugins()

        login_type = request.data.get("type", None)

        if login_type in auth_plugins:
            data = auth_plugins[login_type]['login_func'](request)
            return response.Ok(data)

        raise exc.BadRequest(_("invalid login type"))

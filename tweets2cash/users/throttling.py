# -*- coding: utf-8 -*-

from rest_framework import throttling


class UserDetailRateThrottle(throttling.GlobalThrottlingMixin, throttling.ThrottleByActionMixin, throttling.SimpleRateThrottle):
    scope = "user-detail"
    throttled_actions = ["by_username", "retrieve"]


class UserUpdateRateThrottle(throttling.UserRateThrottle, throttling.ThrottleByActionMixin):
    scope = "user-update"
    throttled_actions = ["update", "partial_update"]

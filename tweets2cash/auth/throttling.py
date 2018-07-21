# -*- coding: utf-8 -*-

from rest_framework import throttling


class LoginFailRateThrottle(throttling.GlobalThrottlingMixin, throttling.ThrottleByActionMixin, throttling.SimpleRateThrottle):
    scope = "login-fail"
    throttled_actions = ["create"]

    def throttle_success(self, response):
        if response is not None and response.status_code == 400:
            self.history.insert(0, self.now)
            self.cache.set(self.key, self.history, self.duration)
        return True


class RegisterSuccessRateThrottle(throttling.GlobalThrottlingMixin, throttling.ThrottleByActionMixin, throttling.SimpleRateThrottle):
    scope = "register-success"
    throttled_actions = ["register"]

    def throttle_success(self, response):
        if response is not None and response.status_code == 201:
            self.history.insert(0, self.now)
            self.cache.set(self.key, self.history, self.duration)
        return True

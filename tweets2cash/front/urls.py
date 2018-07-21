# -*- coding: utf-8 -*-

urls = {
    "home": "/",
    "login": "/login",
    "register": "/register",
    "forgot-password": "/forgot-password",

    "change-password": "/change-password/{0}", # user.token
    "change-email": "/change-email/{0}", # user.email_token
    "cancel-account": "/cancel-account/{0}", # auth.token.get_token_for_user(user)

}

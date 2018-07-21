# -*- coding: utf-8 -*-

from django_jinja import library
from django_sites import get_by_id as get_site_by_id

from tweets2cash.front.urls import urls


@library.global_function(name="resolve_front_url")
def resolve(type, *args):
    site = get_site_by_id("website")
    url_tmpl = "{scheme}//{domain}{url}"

    scheme = site.scheme and "{0}:".format(site.scheme) or ""
    url = urls[type].format(*args)
    return url_tmpl.format(scheme=scheme, domain=site.domain, url=url)

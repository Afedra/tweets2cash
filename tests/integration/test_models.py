# -*- coding: utf-8 -*-

import pytest

from .. import factories as f
from ..utils import disconnect_signals, reconnect_signals


def setup_module():
    disconnect_signals()


def teardown_module():
    reconnect_signals()


pytestmark = pytest.mark.django_db

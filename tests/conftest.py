import shutil

import pytest
from rest_framework.test import APIClient

pytest_plugins = [
    'tests.fixtures',
]


@pytest.fixture
def api_client():
    return APIClient()


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree('static/', ignore_errors=True)

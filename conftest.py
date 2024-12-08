import pytest
from jala.app import PyTempFrameApp


@pytest.fixture
def app():
    return PyTempFrameApp()


@pytest.fixture
def test_client(app):
    return app.test_session()

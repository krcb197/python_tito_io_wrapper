
import pytest
from pytito import AdminAPI


@pytest.fixture(scope='session', name='admin_api')
def admin_api_implementation():
    """
    A fixture that make a connection to the real Tito server with the API key in the environment
    variables
    """
    yield AdminAPI()


@pytest.fixture(scope='function', name='pytito_account')
def pytito_account_implementation(admin_api):
    """
    A test fixture that provides an mocked AdminAPI with mocked data
    """
    yield admin_api.accounts['pytito']


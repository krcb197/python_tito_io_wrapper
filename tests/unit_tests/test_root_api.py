import os

import requests

from pytito import AdminAPI


def test_local_api_key_connection(mocked_requests):
    """
    Check that if there is an API key provided it does not use the one from the environment
    variables
    """
    connection = AdminAPI(api_key='fake_api_key')
    requests.get.assert_called_once_with(url="https://api.tito.io/v3/hello",
                                         timeout=10.0,
                                         headers={"Accept": "application/json",
                                                  "Authorization": "Token token=fake_api_key"})


def test_environment_api_key_connection(mocked_requests):
    """
    Check that the default behaviour is to use the environment variable
    """
    connection = AdminAPI()
    requests.get.assert_called_once_with(
        url="https://api.tito.io/v3/hello",
        timeout=10.0,
        headers={"Accept": "application/json",
                 "Authorization": "Token token=fake_enviroment_var_api_key"})

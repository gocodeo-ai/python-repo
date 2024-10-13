import pytest
from unittest import mock
import jwt
import time
from app.core.auth import generate_jwt

@pytest.fixture
def mock_private_key():
    with mock.patch("builtins.open", mock.mock_open(read_data="private_key_data")):
        yield

@pytest.fixture
def mock_time():
    with mock.patch("time.time", return_value=1000000000):
        yield

@pytest.fixture
def mock_jwt_encode():
    with mock.patch("jwt.encode", return_value="mocked_jwt_token") as mock_encode:
        yield mock_encode

@pytest.fixture
def setup_generate_jwt(mock_private_key, mock_time, mock_jwt_encode):
    app_id = '961019'
    private_key_path = 'gocodeo-dev-agent.2024-08-13.private-key.pem'
    return app_id, private_key_path


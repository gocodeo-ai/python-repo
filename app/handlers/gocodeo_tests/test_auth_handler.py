import pytest
from unittest import mock
from app.handlers.auth_handler import GithubHandler
from app.core.exceptions import NotFoundError, UnauthorizedError, GCException
from app.repositories.user_repository import UserDB
from app.repositories.org_repository import OrgDB
import httpx
import jwt

@pytest.fixture
def mock_user_db():
    with mock.patch('app.repositories.user_repository.UserDB') as mock_db:
        yield mock_db

@pytest.fixture
def mock_org_db():
    with mock.patch('app.repositories.org_repository.OrgDB') as mock_db:
        yield mock_db

@pytest.fixture
def mock_httpx_async_client():
    with mock.patch('httpx.AsyncClient') as mock_client:
        yield mock_client

@pytest.fixture
def mock_jwt_encode():
    with mock.patch('jwt.encode') as mock_encode:
        yield mock_encode

@pytest.fixture
def mock_decrypt_string():
    with mock.patch('app.core.utils.decrypt_string') as mock_decrypt:
        yield mock_decrypt

@pytest.fixture
def mock_encrypt_string():
    with mock.patch('app.core.utils.encrypt_string') as mock_encrypt:
        yield mock_encrypt

@pytest.fixture
def mock_requests_post():
    with mock.patch('requests.post') as mock_post:
        yield mock_post

@pytest.fixture
def github_handler(mock_user_db, mock_org_db):
    return GithubHandler(gc_user_id='12345', org_id='54321', user_id='67890')

@pytest.fixture
def mock_settings():
    with mock.patch('app.core.config.settings') as mock_settings:
        mock_settings.GITHUB_APP_ID = 'test_github_app_id'
        mock_settings.GITHUB_CLIENT_ID = 'test_client_id'
        mock_settings.GITHUB_CLIENT_SECRET = 'test_client_secret'
        mock_settings.GITHUB_INSTALLATION_CLIENT_ID = 'test_installation_client_id'
        mock_settings.GITHUB_INSTALLATION_CLIENT_SECRET = 'test_installation_client_secret'
        mock_settings.PRIVATE_KEY_PATH = 'path/to/private/key'
        yield mock_settings


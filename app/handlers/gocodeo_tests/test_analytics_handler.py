import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.repositories import UserDB, RepoDB, TestRunDB
from app.handlers.analytics_handler import AnalyticsHandler
from app.core.utils import convert_timestamp_to_string, generate_unique_id
from app.handlers.notification_handler import EmailHandler
import pandas as pd
import os

@pytest.fixture
def analytics_handler():
    with patch('app.repositories.UserDB', new_callable=AsyncMock) as mock_user_db, \
         patch('app.repositories.RepoDB', new_callable=AsyncMock) as mock_repo_db, \
         patch('app.repositories.TestRunDB', new_callable=AsyncMock) as mock_test_run_db, \
         patch('app.core.utils.convert_timestamp_to_string', return_value="01 Jan 2024") as mock_convert_timestamp, \
         patch('app.core.utils.generate_unique_id', return_value="unique_id") as mock_generate_unique_id, \
         patch('app.handlers.notification_handler.EmailHandler.send_email_with_attachment', return_value=None) as mock_send_email, \
         patch('pandas.DataFrame.to_excel', return_value=None) as mock_to_excel, \
         patch('os.path.exists', return_value=True) as mock_path_exists, \
         patch('os.remove', return_value=None) as mock_remove:

        handler = AnalyticsHandler()
        handler.user_db = mock_user_db
        handler.repo_db = mock_repo_db
        handler.test_run_db = mock_test_run_db
        
        yield handler
        
        # Cleanup if necessary
        mock_user_db.reset_mock()
        mock_repo_db.reset_mock()
        mock_test_run_db.reset_mock()
        mock_convert_timestamp.reset_mock()
        mock_generate_unique_id.reset_mock()
        mock_send_email.reset_mock()
        mock_to_excel.reset_mock()
        mock_path_exists.reset_mock()
        mock_remove.reset_mock()


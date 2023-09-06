import pytest
from unittest.mock import AsyncMock
from lchop.infrastructure.dsl_engine import DSLEngine  # Replace with your actual import


# Create a mock WorkContext fixture
@pytest.fixture(scope="function")
def mock_dsl_error_handler():
    return AsyncMock()


# Create a mock WorkContext fixture
@pytest.fixture(scope="function")
def mock_work_context():
    mock = AsyncMock()
    mock.navigate = AsyncMock()  # Explicitly mock the navigate method
    return mock


# Inject the mock WorkContext into DSLEngine
@pytest.fixture(scope="function")
def engine(mock_work_context, mock_dsl_error_handler):
    engine_instance = DSLEngine(mock_work_context, mock_dsl_error_handler)
    return engine_instance


# Test for a valid `navigate` command
@pytest.mark.asyncio
async def test_run_valid_navigate_command(engine, mock_work_context):
    await engine.run_command("navigate", url="https://example.com")
    mock_work_context.navigate.assert_called_once_with(url="https://example.com")

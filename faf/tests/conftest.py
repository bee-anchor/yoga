import pytest
from faf.context import CONTEXT


@pytest.fixture(autouse=True)
def reset_context_config():
    CONTEXT.clear_context()
    yield
    CONTEXT.clear_context()
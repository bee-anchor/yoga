import pytest
from yoga.context import CONTEXT


@pytest.fixture(autouse=True)
def reset_context_config():
    CONTEXT.clear_context()
    yield
    CONTEXT.clear_context()

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "unit: Unit tests that test individual functions/methods"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that test multiple components together"
    )

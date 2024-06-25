import os
import pytest


@pytest.fixture(autouse=True)
def show_working_directory():
    print("Current Working Directory:", os.getcwd())

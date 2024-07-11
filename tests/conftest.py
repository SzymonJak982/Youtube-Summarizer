import os
import pytest

# TODO: Transfer other fixtures  here

@pytest.fixture(autouse=True)
def show_working_directory():
    print("Current Working Directory:", os.getcwd())

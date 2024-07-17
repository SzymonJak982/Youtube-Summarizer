import subprocess
import os
from settings import STATIC_FILE_DIR

def tmp_cleaner(path='../tmp'):
    command = f"rm {path}/*"
    subprocess.run(command, shell=True, check=True)
    #TODO: Refactor to operate on temp module in python


def get_path(relative_path):
    """:param relative_path- relative from src/prompts_schemas dir"""
    return os.path.join(STATIC_FILE_DIR, relative_path)

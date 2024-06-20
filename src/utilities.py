import subprocess

def tmp_cleaner(path='../tmp'):
    command = f"rm {path}/*"
    subprocess.run(command, shell=True, check=True)
    #TODO: Refactor to operate on temp module in python


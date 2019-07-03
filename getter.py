"""
    download a directory from google drive

    GDRIVE is the executable you're going to use, and SEARCH_STRING is how you find the directory you're looking for.
    This will download that directory into the current folder.

"""
import subprocess
from pprint import pprint

GDRIVE = "./gdrive-linux-x64"
SEARCH_STRING = "Zine Edition 0"

result = subprocess.run((GDRIVE, "list"), stdout=subprocess.PIPE)

for x in result.stdout.decode('utf-8').split("\n"):
    if SEARCH_STRING in x:
        ID = x.split()[0]

subprocess.run((GDRIVE, "download", "-r", ID))

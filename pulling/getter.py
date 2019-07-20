"""
    download a directory from google drive

    GDRIVE is the executable you're going to use, and SEARCH_STRING is how you find the directory you're looking for.
    This will download that directory into the current folder.

"""
import subprocess
from pprint import pprint

def main(gdrive="./gdrive-linux-x64", search_string="Zine Edition 0"):
    result = subprocess.run((gdrive, "list"), stdout=subprocess.PIPE)

    for x in result.stdout.decode('utf-8').split("\n"):
        if search_string in x:
            ID = x.split()[0]

    try:
        subprocess.run((gdrive, "download", "-r", ID))
        return True
    except UnboundLocalError:
        print(result.stdout.decode('utf-8'))
        print("are you connected to the internet?")
        #TODO: raise an exception
        return False

if __name__ == "__main__":
    import sys
    try:
        main(search_string=sys.argv[-1])
    except:
        main()

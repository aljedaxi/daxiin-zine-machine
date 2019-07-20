"""
    quickly create a vars file so you don't have to write out all those file paths.
"""

import yaml
from os import listdir
from os.path import isfile, join

extensions = {
    "tex": "prose",
    "txt": "prose",
    "png": "image",
    "jpg": "image",
    "odt": "odt",
    "pdf": "pdf",
}

def main(folders=("specials", "Zine Edition 0")):
    #folders: a list of folders to be searched through
    #extensions: a list of valid file extensions
    paths  = []
    types  = []
    titles = []
    for folder in folders:
        for filename in listdir(folder):
            extension = filename.split(".")[-1]
            try:
                types.append(extensions[extension])
            except:
                types.append("other")
            paths.append(f"{folder}/{filename}")
            titles.append(filename.split(".")[-2].replace("_", " "))

    protein = [{"file"  : path,
                "type"  : kind,
                "author": "Anonymous",
                "rights": "Peer Production License",
                "title" : title,} for title, path, kind in zip(titles, paths, types)
                ]

    return protein

if __name__ == "__main__":
    print(
        main(folders=("Zine Edition 0",))
    )

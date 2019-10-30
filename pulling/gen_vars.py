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
    "docx": "docx",
    "pdf": "pdf",
    "yml": "yml_prose",
    "md" : "md",
}

def main(folders=("input")):
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
            try:
                titles.append(filename.split(".")[-2].replace("_", " "))
            except:
                titles.append(filename.replace("_", " "))

    protein = [{"file"  : path,
                "type"  : kind,
                "author": "Anonymous",
                "rights": "Peer Production License",
                "title" : title,} for title, path, kind in zip(titles, paths, types)
                ]

    return protein

if __name__ == "__main__":
    print(
        main(folders=("input",)) #TODO get from command line
    )

"""
    quickly create a vars file so you don't have to write out all those file paths.
"""

extensions = {
    "tex": "prose",
    "txt": "prose",
    "png": "image",
    "jpg": "image",
    "pdf": "pdf",
}

def main():
    #folders: a list of folders to be searched through
    #extensions: a list of valid file extensions
    paths = []
    types = []
    for folder in folders:
        #list files in folder
        #for file in folder:
            #if file extension in extensions.keys()
            #TODO: see if you can get metadata from it?
            #paths.append(f"{folder}/{file}")
            #types.append(extensions[extension])

    protein = [{"file"  : path,
                "type"  : kind,
                "author": "Anonymous",
                "rights": "Peer Production License",
                "title" : "Untitled",} for path, kind in zip(paths, types)]

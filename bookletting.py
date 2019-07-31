#!/usr/bin/python3
"""
    this is the primary bookletting system.
"""
#_CONFILE = "config.yml"

def booklet(title, out_file):
    """
        this creates a printable booklet called f"{out_file}.pdf" from f"{title}.pdf".
        all of the buffer files made in the process are deleted.
    """
    from subprocess import call
    call(("pdfbook2",
          "--paper=letter",
          "--inner-margin=0",
         f"{title}.pdf"))
    call(("pdf270",
         f"{title}-book.pdf"))
    call(("pdfbook2",
          "--paper=letter",
          "--inner-margin=75",
         f"{title}-book-rotated270.pdf"))
    call(("mv",
         f"{title}-book-rotated270-book.pdf",
         f"{out_file}.pdf"))
    call(("rm",
         f"{title}-book.pdf",
         f"{title}-book-rotated270.pdf"))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")

    ARGS = parser.parse_args()

    IN_FILE = ARGS.infile
    #returns the part before the extension
    TITLE = IN_FILE.split(".")[0]

    OUT_FILE = f"{TITLE}_booklet"

    booklet(TITLE, OUT_FILE)

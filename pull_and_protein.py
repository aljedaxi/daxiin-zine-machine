import yaml
import pyaml
import subprocess
import re
from subprocess import call
from pulling import getter, gen_vars

def convert(infile, outfile="", verbose=False):
    def strip_extension(filename):
        name = infile.split(".")[:-1]

        try:
            name = "".join(name)
        except:
            pass

        return name

    name = strip_extension(infile)

    if not outfile:
        outfile = f"{name}.tex"

    command = ("pandoc", infile, "-o", outfile, "-t", "latex")

    if verbose:
        print(command)

    call(
        command
    )

    return outfile

def main(EDITION="ZineEdition0",
    EXTRA_FOLDERS=("specials", "permeate"),
    W2L="./w2l",
    W2L_CONFIG="config/daxiinclean.xml",
    LATEX_OUTDIR="./test/",
    DEFAULT_TEX_TYPE="prose",
    PULL=False,
    PROTEIN=True,
    CONVERT=True,
    VERBOSE=False,
):
    pulled = False
    if PULL:
        pulled = getter.main(search_string=EDITION)
        if not pulled:
            print("pull failed")
            exit()

    if PROTEIN:
        try:
            protein = gen_vars.main(folders=(EDITION, *EXTRA_FOLDERS))
        except:
            call(("mkdir", EDITION))
            protein = gen_vars.main(folders=(EDITION, *EXTRA_FOLDERS))

        odt_enumerated = [(p,article) for p, article in enumerate(protein) 
                          if article['type'] == 'odt']

        for position, article in odt_enumerated:
            outfile = convert(article['file'], verbose=VERBOSE)
            protein[position] = {
                    "file"  : outfile,
                    "type"  : DEFAULT_TEX_TYPE,
                    "author": "Anonymous",
                    "rights": "Peer Production License",
                    "title" : article['title'],
                    }

        conf = {
            "g_edition" : "0",
            "g_title"   : "The Anarchist Guide to: Home",
            "g_author"  : "Permeate Calgary",
            "g_font"    : "coelacanth",
            "g_template": "edition_template.tex",
            #"#backcover": "test/backcover.pdf"
            #"#frontcover": "test/frontcover.pdf"
            "special pages": {
                "contributors": {
                  "title": "contributors",
                  "author": "Permeate",
                  "template": "contributors.tex",
                  "type": "skip",
                  "rights": "Peer Production License",
                }
            },
            "editorial team": {
                "editor in chief": "aljedaxi",
                "visual director": "[emberlynn]",
                "ray of sunshine": "[valerie]",
            },
        }
        return {
            "protein": protein,
            "conf": conf,
        }

    return pulled

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pull", help="pull data from google drive",
        action="store_true")
    parser.add_argument("-dp", "--protein", 
        help="*don't* generate metadata from data", action="store_false")
    parser.add_argument("-v", "--verbose", 
        help="fucking guess", action="store_true")
    ARGS = parser.parse_args()
    print(
        pyaml.dump(
            main(
                PULL=ARGS.pull,
                PROTEIN=ARGS.protein,
                VERBOSE=ARGS.verbose
            )
        )
    )

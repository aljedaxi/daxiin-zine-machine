import yaml
import pyaml
import subprocess
import re
from subprocess import call
from pulling import getter, gen_vars

def cull(filename):
    begun = 0
    output = ""
    for line in open(filename).readlines():
        if begun:
            if "\\end{document" not in line:
                output += line

        if "\\begin{document}" in line:
            begun = 1

    open(filename, "w").write(output)

    return True

def main(EDITION="Zine Edition 0",
    EXTRA_FOLDERS=("specials", "permeate"),
    W2L="./w2l",
    W2L_CONFIG="config/daxiinclean.xml",
    LATEX_OUTDIR="./test/",
    PULL=False,
):
    if PULL:
        pulled = getter.main(search_string=EDITION)
        if not pulled:
            print("pull failed")
            exit()

    try:
        protein = gen_vars.main(folders=(EDITION, *EXTRA_FOLDERS))
    except:
        call(("mkdir", EDITION))
        protein = gen_vars.main(folders=(EDITION, *EXTRA_FOLDERS))

    odt = (f for f in protein if f['type'] == 'odt')
    for article in odt:
        command = (f"{W2L}/w2l",
             "-config",
            f"{W2L}/{W2L_CONFIG}",
            f"""./{article["file"]}""",
            LATEX_OUTDIR
        )
        latex = subprocess.run(
                   command,
                   stdout=subprocess.PIPE
                ).stdout.decode('utf-8')
        article['type'] = "prose"
        filename = f"{article['file'].split('/')[-1].split('.')[-2]}.tex"
        path = f"{LATEX_OUTDIR}{filename}"
        article['file'] = path
        cull(path)

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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--pull", help="pull data from google drive",
        action="store_true")
    parser.add_argument("-r", "--protein", 
        help="generate metadata from data", action="store_true")
    ARGS = parser.parse_args()
    print(
        pyaml.dump(
            main(
                PULL=ARGS.pull
            )
        )
    )

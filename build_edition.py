#/usr/bin/env python3
"""
    This is the code that's used to build the permeate zine,
    but i'm working on making it totally transferable between zines.
"""

from	subprocess	import call
from 	os			import path
        #this imports a module for each different type of article
import	jinja2
import  yaml

from    types_and_settings import poem, prose, image, custom
from    bookletting import booklet

def cleanup(title, minutes):
    """
        removes all of the files created by LaTeX,
        then moves the original minutes file into the archives.
    """
    call(("rm",
         f"{title}.aux",
         f"{title}.fdb_latexmk",
         f"{title}.fls",
         f"{title}.log",
         f"{title}.toc",
         f"{title}.tex",
        ))

    call(("mv",
          minutes,
          "archives/",))

def rename_texput(outfile):
    """renames autonamed LaTeX output"""
    call(("mv", "texput.pdf", f"{outfile}.pdf"))

def fill(template_file, outfile, meta, env):
    """
        fills a given template with data.
    """

    template = env.get_template(template_file)

    open(outfile, "w").write(
        template.render(
            **meta,
        )
    )

    call(("latexmk", "--pdf", outfile))

def format_articles(articles, env, force=False, verbose=False, bios={}, defaults="failed_formattings.tex"):
    """
        takes the list of articles---as defined in vars.yml---and
        if they haven't yet been formatted, formats them
        (using the code in types_and_settings/ and templates in templates/)
    """
    f_files = []
    for article in articles:
        text = ""
        try:
            text = open(article['file']).read()
        except UnicodeDecodeError:
            if verbose:
                print(f"{article['file']} is an image lol")
            text = "this is an image edit this template"
        except FileNotFoundError:
            print(f"article {article['title']}'s file {article['file']} doesn't exist!")
            continue

        #generate outfile filename; test for existence
        (directory, a_file) = article['file'].split("/")
        #the outfile is going to be .tex, even if the infile is an image
        outfile = "/".join((directory, f"f_{a_file[:-4]}.tex"))
        if path.isfile(outfile) and not force:
            if verbose:
                print(f"{outfile} already exists. Skipping {article['title']}")
            #TeX likes its input files implicitly extended
            f_files.append(outfile[:-4])
            continue

        #attach bio to author
        if article['author'] in bios.keys():
            article['bio'] = bios[article['author']]

        #check if title has subtitle in it
        if "\n" in article['title']:
            try:
                (meta['title'], meta['subtitle']) = meta['title'].split("\n")
            except ValueError:
                temp_title = meta['title'].split("\n")
                meta['title'] = temp_title[0]
                meta['subtitle'] = r"\\".join(temp_title[1:])

        #find the correct module to use based on the type of article
        function = globals().copy().get(article['type'])
        if not function:
            raise NotImplementedError(f"Function {function} not implemented.")
        formatted_article = function.main(text, meta=article, env=env)

        try:
            open(outfile, "w").write(formatted_article)
        except IOError as e:
            print(f"writing to {outfile} failed. Writing to {defaults} instead.\n{e}\n")
            open(defaults, "a").write(formatted_article)

        if verbose:
            print(f"writing formatted {article['title']} text to {outfile}")
        f_files.append(outfile[:-4])
    return f_files

def main(force=False, verbose=False, booklet=False):
    """
        exactly what you expect a main to do.
    """
    CONF = yaml.load(open('vars.yml').read())
    GLOBAL_CONF = yaml.load(open('global_vars.yml').read())
    ENV = jinja2.Environment(
        **GLOBAL_CONF['jinja2_env'],
    )

    META = CONF['conf']

    #compiles each article from txt into LaTeX,
    #using the templating systems defined in types_and_settings
    #force and verbose are passed to main
    F_FILES = format_articles(CONF['protein'],
                              ENV,
                              force=force,
                              verbose=verbose,
                              bios=GLOBAL_CONF['author_bios'],
                              defaults="failed_formattings.tex")

    META['files'] = F_FILES
    TEMPLATE_FILE = META['template']
    OUTFILE_CORE = f"{GLOBAL_CONF['zine_title']}_zine_{META['edition']}"

    fill(TEMPLATE_FILE,
         f"{OUTFILE_CORE}.tex",
         META,
         ENV)
    if booklet:
        booklet(OUTFILE_CORE,
                f"{GLOBAL_CONF['zine_title']}_booklet_{META['edition']}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",    action="store_true")
    parser.add_argument("-f", "--force",   help="force recreation of articles", action="store_true")
    parser.add_argument("-b", "--booklet", help="also booklet the pdf",         action="store_true")
    ARGS = parser.parse_args()

    main(force=ARGS.force,
       verbose=ARGS.verbose,
       booklet=ARGS.booklet)

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

from    types_and_settings import poem
from    bookletting import booklet

#template_file = ""

CONF = yaml.load(open('vars.yml').read())
GLOBAL_CONF = yaml.load(open('global_vars.yml').read())
#TODO: find a way to externalize this code
ENV = jinja2.Environment(
    block_start_string	    = '\BLOCK{',
    block_end_string		= '}',
    variable_start_string	= '\VAR{',
    variable_end_string	    = '}',
    comment_start_string	= '%/*',
    comment_end_string	    = '%*/',
    line_comment_prefix	    = '%//',
    line_statement_prefix	= '%%',
    trim_blocks 			= True,
    lstrip_blocks			= True,
    autoescape			    = False,
    loader				    = jinja2.FileSystemLoader("./"),
)

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

def fill(template_file, outfile, meta):
    """
        fills a given template with data.
    """

    template = ENV.get_template(template_file)

    #etwas = Popen(("pdflatex"), stdout=PIPE, 
    #              stdin=PIPE, stderr=PIPE).communicate(
    #                                                   input=bytes(
    #                                                         template.render(
    #                                                   ), "utf-8"
    #                                             )
    #                                        )
    #rename_texput(outfile)

    #this is the only thing that really changes from instance to instance
    #if you can find a way to change what's in the middle of it, you're golden
    open(outfile, "w").write(
        template.render(
            **meta,
        )
    )

    call(("latexmk", "--pdf", outfile))

def format_articles(articles):
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
        except FileNotFoundError:
            print(f"article {article['title']}'s file {article['file']} doesn't exist!")
            continue

        #generate outfile filename; test for existence
        (directory, a_file) = article['file'].split("/")
        outfile = "/".join((directory, f"f_{a_file}"))
        if path.isfile(outfile) and not FORCE:
            if VERBOSE:
                print(f"{outfile} already exists. Skipping {article['title']}")
            #TeX likes its input files implicitly extended
            f_files.append(outfile[:-4])
            continue

        #find the correct module to use based on the type of article
        function = globals().copy().get(article['type'])
        if not function:
            raise NotImplementedError(f"Function {function} not implemented.")
        formatted_article = function.main(text, meta=article, env=ENV)
        #TODO: put this in try except
        open(outfile, "w").write(formatted_article)
        if VERBOSE:
            print(f"writing formatted {article['title']} text to {outfile}")
        f_files.append(outfile[:-4])
    return f_files

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",    action="store_true")
    parser.add_argument("-f", "--force",   help="force recreation of articles", action="store_true")
    ARGS = parser.parse_args()

    #from sys import argv

    #if this is set, the program will rebuild articles that have already been processed
    FORCE = ARGS.force
    VERBOSE = ARGS.verbose

    META = CONF['conf']

    #compiles each article from txt into LaTeX, 
    #using the templating systems defined in types_and_settings
    _f_files = format_articles(CONF['protein'])

    META['files'] = _f_files
    TEMPLATE_FILE = META['template']
    outfile_core = f"{GLOBAL_CONF['zine_title']}_zine_{META['edition']}"

    fill(TEMPLATE_FILE, f"{outfile_core}.tex", META)
    booklet(outfile_core, f"{GLOBAL_CONF['zine_title']}_booklet_{META['edition']}")
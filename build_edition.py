#/usr/bin/env python3
"""
    This machine makes zines.
"""
VARS_DEFAULT = "test_vars.yml"

from	subprocess	import call
from 	os			import path
        #this imports a module for each different type of article
import	jinja2
import  yaml

from    types_and_settings import mb, poem, prose, image, custom, yml_prose, pdf
from    bookletting import booklet
from    LaTeXing import fill

def test():
    GLOBAL_CONF = yaml.load(open('global_vars.yml').read())
    ENV = jinja2.Environment(
        **GLOBAL_CONF['jinja2_env'],
    )
    print(
        prose.main(
            "i will dab on you",
            {
            "title":  "Test Test",
            "author": "aljedaxi",
            "type":   "image",
            "file":   "test/test.jpg",
            "rights": "Public Domain",
            },
            ENV,
            fill=fill,
        )
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

def format_articles(articles, env, force=False, verbose=False, bios={}, defaults="failed_formattings.tex"):
    """
        takes the list of articles---as defined in vars.yml---and
        if they haven't yet been formatted, formats them
        (using the code in types_and_settings/ and templates in templates/)
    """
    f_files = []
    c_authors = set()
    for article in articles:
        text = ""

        if article['type'] == "skip":
            c_authors.add(article['author'])
            f_files.append(f"skipped: {article['title']}")

            if verbose:
                print(f"writing formatted {article['title']} text to {outfile}")
                print(f"c_authors => {c_authors}")

            continue
            
        try:
            text = open(article['file']).read()
        except UnicodeDecodeError:
            if verbose:
                print(f"{article['file']} is an image lol")
            text = r"\Large this is an image edit this template"
        except FileNotFoundError:
            print(f"article {article['title']}'s file {article['file']} doesn't exist!")
            continue

        try:
            a_file = article['file'].split("/")[-1]
            directory = "/".join(article['file'].split("/")[0:-1])
        except:
            a_file = article['file']

        #the outfile is going to be .tex, even if the infile is an image
        outfile = "/".join(
            (directory, f"f_{a_file[:-4]}.tex")
        )
        if path.isfile(outfile) and not force:
            if verbose:
                print(f"{outfile} already exists. Skipping {article['title']}")
            #TeX likes its input files implicitly extended
            f_files.append(outfile[:-4])
            continue

        try:
            article['bio'] = bios[articles['author']]
        except TypeError:
            pass
        except KeyError:
            pass

            
        #check if title has subtitle in it
        if "\n" in article['title']:
            try:
                (meta['title'], meta['subtitle']) = meta['title'].split("\n")
            except ValueError:
                temp_title = meta['title'].split("\n")
                meta['title'] = temp_title[0]
                meta['subtitle'] = r"\\".join(temp_title[1:])

        #find the correct module to use based on the type of article
        try:
            #try to find the function within the file mb
            formatted_article = getattr(mb, article['type'])(text, meta=article, env=env, fill=fill)
        except AttributeError:
            module = globals().copy().get(article['type'])
            if not module:
                print(article['type'])
                print("if the file exists, make sure it's being imported")
                raise NotImplementedError(f"Function {module} not implemented.")

            formatted_article = module.main(text, meta=article, env=env)

        try:
            open(outfile, "w").write(formatted_article)
        except IOError as e:
            print(f"writing to {outfile} failed. Writing to {defaults} instead.\n{e}\n")
            open(defaults, "a").write(formatted_article)

        try:
            c_authors.add(article['author'])
        except:
            pass

        if verbose:
            print(f"writing formatted {article['title']} text to {outfile}")
            print(c_authors)

        f_files.append(outfile[:-4])

    return {'c_authors': c_authors,
            'f_files':   f_files}

def main(
    force=False, 
    verbose=False, 
    booklet_p=False, 
    varsfile=VARS_DEFAULT,
    g_varsfile="global_vars.yml",
    outfile_tex="test_edition.tex",
):
    """
        exactly what you expect a main to do.
    """
    if not outfile_tex:
        outfile_tex = "test_edition.tex",
        
    CONF = yaml.load(open(varsfile).read())
    GLOBAL_CONF = yaml.load(open(g_varsfile).read())
    ENV = jinja2.Environment(
        **GLOBAL_CONF['jinja2_env'],
    )

    META = CONF['conf']

    #compiles each article from txt into LaTeX,
    #using the templating systems defined in types_and_settings
    #force and verbose are passed to main
    formats = format_articles(CONF['protein'],
                              ENV,
                              force=force,
                              verbose=verbose,
                              bios=GLOBAL_CONF['author_bios'],
                              defaults="failed_formattings.tex")

    META['files'] = formats['f_files']
    META['contributors'] = formats['c_authors']

    for i, article in enumerate(META['files']):
        if "skipped" in article:
            article = article.split("skipped: ")[-1]
            outfile = f"specials/f_{article}.tex"
            if path.isfile(outfile) and not force:
                if verbose:
                    print(f"{outfile} already exists. Skipping {article['title']}")
                #TeX likes its input files implicitly extended
                META['files'][i] = outfile[:-4]
                continue
            a_meta = META['special pages'][article]
            template = ENV.get_template(a_meta['template'])
            open(outfile, "w").write(
                template.render(
                    **META,
                    **a_meta
                )
            )
            META['files'][i] = outfile[:-4]

    TEMPLATE_FILE = META['g_template']
    OUTFILE_CORE  = f"{GLOBAL_CONF['zine_title']}_zine_{META['g_edition']}"
    OUTFILE_TEX   = f"{OUTFILE_CORE}.tex"

    open(OUTFILE_TEX, "w").write(
        fill(TEMPLATE_FILE,
             META,
             ENV)
    )

    call(("latexmk", "--pdf", OUTFILE_TEX))

    if booklet_p:
        booklet(OUTFILE_CORE,
                f"{GLOBAL_CONF['zine_title']}_booklet_{META['g_edition']}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",    action="store_true")
    parser.add_argument("-f", "--force",   help="force recreation of articles", action="store_true")
    parser.add_argument("-b", "--booklet", help="also booklet the pdf",         action="store_true")
    parser.add_argument("-vars", "--vars_file", 
        help="yml file containing necessary metadata",
    )
    parser.add_argument("-o", "--out_file", 
        help="name for file which will store output",
    )

    ARGS = parser.parse_args()

    if ARGS.vars_file == None:
        ARGS.vars_file = VARS_DEFAULT

    #if ARGS.test:
    #    test()
    #    exit()

    main( force=ARGS.force,
        verbose=ARGS.verbose,
      booklet_p=ARGS.booklet,
       varsfile=ARGS.vars_file,
    outfile_tex=ARGS.out_file,
    )

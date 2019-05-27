#!/usr/bin/env python3

import sys
import jinja2
from   jinja2	import Template, Environment
from pprint import pprint

side = "left"
DEFAULT = {
    "title" : "Untitled",
    "author": "Anonymous",
    "type"  : "poem",
    "rights": "Copyright",
}
ENV = Environment(
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
    loader				    = jinja2.FileSystemLoader("../templates/"),
)
TEMPLATE = "poem.tex"

def main(text, meta=DEFAULT, env=ENV):
    lines_in = [line for line in text.split("\n")]
    template = env.get_template("poem.tex")
    if "\n" in meta['title']:
        try:
            (meta['title'], meta['subtitle']) = meta['title'].split("\n")
        except ValueError:
            temp_title = meta['title'].split("\n")
            meta['title'] = temp_title[0]
            meta['subtitle'] = r"\\".join(temp_title[1:])
    lines_out = poemize_neues(lines_in, meta, env)
    return lines_out

def poemize_neues(lines, meta, env):
    stanzas = []
    j = 0
    for i in range(len(lines)):
        if lines[i] is '':
            #creates a stanza from the last white space to this one
            stanzas.append(lines[j:i])
            #offset so the stanzas themselves don't have blank lines
            j = (i + 1)

    template = env.get_template(TEMPLATE)

    meta['stanzas'] = stanzas

    lines_out = template.render(
        **meta,
    )
    return lines_out

#consider deleting this
def poemize(lines, meta):
    """
        string with a poem as input and formats it with LaTeX
        makes it look Nietzschean at current
    """

    title = meta['title']
    author = meta['author']
    rights = meta['rights']

    lines_out = []

    #lines_out.append("\\addcontentsline{toc}{section}{\\makebox[16em][l]{%s} %s}"% (title, date))
    #lines_out.append("\\%sheader{%s %s}"% (side,title,date))
    lines_out.append(f"\\article_title{{{title}}}\n")
    lines_out.append(f"\\article_author{{{author}}}")
    lines_out.append("\\begin{poem}")

    begun = 1
    x = 0
    while x < len(lines):
        if (x + 1) == len(lines):
            lines_out.append("%s"% (lines[x]))
        elif len(lines[x].strip()) == 0:
            if begun:
                lines_out.append("\\begin{stanza}")
                begun = 0
            else:
                lines_out.append("\\end{stanza}\n\\begin{stanza}")
        elif len(lines[(x + 1)].strip()) == 0:
            lines_out.append("%s"% (lines[x]))
        else:
            lines_out.append("%s\\verseline"% (lines[x]))
        x += 1
    lines_out.append("\\end{stanza}")
    lines_out.append("\\end{poem}")
    lines_out.append(f"\n\\article_rights{{{rights}}}")
    return(lines_out);

if __name__ == "__main__":
    poem = open("my_fucking_restaurant.tex").read()
    print(main(poem))
        #insert each one into the index

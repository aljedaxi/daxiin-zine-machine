#!/usr/bin/env python3

import sys

side = "left"
DEFAULT = {
        "title" : "Untitled",
        "author": "Anonymous",
        "type"  : "poem",
        "rights": "Copyright",
}

def main(text, meta=DEFAULT):
    lines_in = [line for line in text.split("\n")]
    lines_out = poemize(lines_in, meta)
    return "\n".join(lines_out)

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
    poem = open("Ralph_Waldo_Emerson-Fable.tex").read()
    meta = {
        "title" : "Fable",
        "author": "Ralph Waldo Emerson",
        "type"  : "poem",
        "file"  : "emerson/Ralph_Waldo_Emerson-Fable.tex",
        "rights": "Public Domain",
    }
    print(main(poem, meta=meta))
        #insert each one into the index

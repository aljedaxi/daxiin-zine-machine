#!/usr/bin/python3

#things to add:

#create an index file; put all the necessary soykaf up here

import sys

side = "left"

def poemize(poem):
    """
        file with a poem as input and formats it with LaTeX
        makes it look Nietzschean at current
    """

    #lines = []
    #with open(poem, "r") as infile:
    #    #for line in infile:
    #    #    lines.append(line.strip())
    #    lines = [line.strip() for line in infile]

    lines = [line.strip() for line in open(poem).read()]

    with open(poem, "w") as outfile:
        title_date = lines[0].split(" ")
        del lines[0]
        date = title_date.pop()
        title = " ".join(title_date)
        outfile.write("\\addcontentsline{toc}{section}{\\makebox[16em][l]{%s} %s}\n"% (title, date))
        outfile.write("\\%sheader{%s %s}\n"% (side,title,date))
        outfile.write("\\poemtitle{\\textfrak{%s}}\n"% (title))
        outfile.write("\\begin{poem}\n")
        begun = 1
        x = 0
        while x < len(lines):
            if (x + 1) == len(lines):
                outfile.write("%s\n"% (lines[x]))
            elif len(lines[x].strip()) == 0:
                if begun:
                    outfile.write("\\begin{stanza}\n")
                    begun = 0
                else:
                    outfile.write("\\end{stanza}\n\\begin{stanza}\n")
            elif len(lines[(x + 1)].strip()) == 0:
                outfile.write("%s\n"% (lines[x]))
            else:
                outfile.write("%s\\verseline\n"% (lines[x]))
            x += 1
        outfile.write("\\end{stanza}\n")
        outfile.write("\\end{poem}\n")
        return(title);

if __name__ == "__main__":
    files = sys.argv[1:]    #makes files the list of all files given
    for f in files:
        poemize(f)
        #insert each one into the index

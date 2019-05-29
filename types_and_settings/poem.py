#!/usr/bin/env python3
"""
    this file deals with any poem that comes in.

    If you want to change the way the poems actually look,
    i'd recommend looking at the edition template.
"""

from   jinja2 import Environment
from  .render import fill

def main(text, meta={}, env=Environment()):
    """
        this is the driver for poem typesetting.
        text is the text of the poem.
        meta is metadata, eg, author, title, bio.
        env is a jinja2 environment.
    """
    lines_in = [line for line in text.split("\n")]
    meta['stanzas'] = stanzatize(lines_in)
    print(meta['stanzas'])
    exit()
    lines_out = fill("poem.tex", env=env, meta=meta)
    return lines_out

def stanzatize(lines):
    """
        this takes the lines of the poem and splits them into stanzas.
    """
    stanzas = []
    j = 0
    for i, line in enumerate(lines):
        if line == '':
            #creates a stanza from the last white space to this one
            stanzas.append(lines[j:i])
            #offset so the stanzas themselves don't have blank lines
            j = (i + 1)
    return stanzas

if __name__ == "__main__":
    POEM = open("my_fucking_restaurant.tex").read()
    print(main(POEM))
        #insert each one into the index

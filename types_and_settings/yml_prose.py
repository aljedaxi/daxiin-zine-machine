#!/usr/bin/env python3
"""
    this takes a work of yml and typesets it, because i can't be arsed to write '\\begin's '\\end's and '\\item's.
"""

from  jinja2 import Environment
from .render import fill
from .yml_to_tex import yml_to_tex

def main(text, meta={}, env=Environment()):
    """
        this is the driver for prose typesetting.
        text is the text of the prose.
        meta is metadata, eg, author, title, bio.
        env is a jinja2 environment.
    """
    meta['text'] = yml_to_tex(text)
    lines_out = fill("prose.tex", env=env, meta=meta)
    return lines_out

if __name__ == "__main__":
    PROSE = open("my_fucking_restaurant.tex").read()
    print(main(PROSE))
        #insert each one into the index

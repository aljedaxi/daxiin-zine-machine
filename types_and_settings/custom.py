#!/usr/bin/env python3
"""
    this takes something and assumes the source file has it's own internal typesetting.
    mostly this is for stuff that daxi's written.
"""

from   jinja2 import Environment
from  .render import fill

def main(text, meta={}, env=Environment()):
    """
        this is the driver for custom typesetting.
        text is the custom text. It can have any variables that get set in vars.yml.
        meta is metadata, eg, author, title, bio.
        env is a jinja2 environment.
    """
    if "\BLOCK" in text or "\VAR" in text:
        lines_out = env.from_string(text).render(
            **meta,
        )
    else:
        meta['text'] = text
        lines_out = fill("custom.tex", env=env, meta=meta)
    return lines_out

if __name__ == "__main__":
    PROSE = open("my_fucking_restaurant.tex").read()
    print(main(PROSE))
        #insert each one into the index


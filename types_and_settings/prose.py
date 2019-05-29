#!/usr/bin/env python3

import sys
import jinja2
from   jinja2	import Template, Environment

def fill(template="dab", env="dab", meta="dab"):
    template = env.get_template(template)

    lines_out = template.render(
        **meta,
    )
    return lines_out

def main(text, meta={}, env=Environment()):
    lines_in = [line for line in text.split("\n")]
    template = env.get_template("prose.tex")
    if "\n" in meta['title']:
        try:
            (meta['title'], meta['subtitle']) = meta['title'].split("\n")
        except ValueError:
            temp_title = meta['title'].split("\n")
            meta['title'] = temp_title[0]
            meta['subtitle'] = r"\\".join(temp_title[1:])
    meta['text'] = text
    lines_out = fill("prose.tex", env=env, meta=meta)
    return lines_out

if __name__ == "__main__":
    prose = open("my_fucking_restaurant.tex").read()
    print(main(prose))
        #insert each one into the index

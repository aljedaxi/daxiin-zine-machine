#!/usr/bin/env python3

import sys
import jinja2
from   jinja2	import Template, Environment
import rendering

side = "left"
DEFILE = "defaults.yml"
DEFAULTS = yaml.load(open(DEFILE).read())
ENV = Environment(
    **DEFAULTS['ENV']
)

def main(text, meta=DEFAULTS['META'], env=ENV):
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
    lines_out = rendering.fill(template=DEFAULTS['TEMPLATE'], env=env, meta=meta)
    return lines_out

if __name__ == "__main__":
    prose = open("my_fucking_restaurant.tex").read()
    print(main(prose))
        #insert each one into the index

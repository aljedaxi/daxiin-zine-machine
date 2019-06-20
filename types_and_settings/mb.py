"""
    mother brain.
    i'm getting tired of all the code duplication around here so i'm going to try to centralize it without sacrificing extendibility.
"""
from  jinja2 import Environment

def fill(template="prose.tex", env=Environment(), meta={}):
    template = env.get_template(template)

    lines_out = template.render(
        **meta,
    )
    return lines_out

def generic(template="default.tex"):
    def f(text, meta={}, env="dong", fill=(lambda x, y, z : f"error with arguments {x} {y} {z}"), template=template):
        if not template == "default.tex":
            #generate template name from filename
            template = f"{meta['type']}.tex"

        meta['text'] = text
        lines_out = fill(template, env=env, meta=meta)
        return lines_out
    return f

prose = generic(template="prose.tex")
image = generic(template="image.tex")
pdf   = generic(template="pdf.tex")

def custom(text, meta={}, env=Environment(), fill=fill):
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

#def pdf(text, meta={}, env=Environment()):
#    """
#        this is the driver for poem typesetting.
#        text is the text of the poem.
#        meta is metadata, eg, author, title, bio.
#        env is a jinja2 environment.
#    """
#    lines_out = fill("pdf.tex", env=env, meta=meta)
#    return lines_out

def poem(text, meta={}, env=Environment(), fill=fill):
    """
        this is the driver for poem typesetting.
        text is the text of the poem.
        meta is metadata, eg, author, title, bio.
        env is a jinja2 environment.
    """
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
    lines_in = [line for line in text.split("\n")]
    meta['stanzas'] = stanzatize(lines_in)
    lines_out = fill("poem.tex", env=env, meta=meta)
    return lines_out

def yml_prose(text, meta={}, env=Environment(), fill=fill):
    """
        this is the driver for prose typesetting.
        text is the text of the prose.
        meta is metadata, eg, author, title, bio.
        env is a jinja2 environment.
    """
    from .yml_to_tex import yml_to_tex
    meta['text'] = yml_to_tex(text)
    lines_out = fill("prose.tex", env=env, meta=meta)
    return lines_out

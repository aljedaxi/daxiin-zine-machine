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

def jinja2_p(text):
    if "\BLOCK" in text or "\VAR" in text:
        return True
    else:
        return False

def stanzatize(meta):
    """
        this takes the lines of the poem and splits them into stanzas.
    """
    lines = [line for line in meta['text'].split("\n")]
    stanzas = []
    j = 0
    for i, line in enumerate(lines):
        if line == '':
            #creates a stanza from the last white space to this one
            stanzas.append(lines[j:i])
            #offset so the stanzas themselves don't have blank lines
            j = (i + 1)

    meta['stanzas'] = stanzas

def ymly_tex(meta):
    from .yml_to_tex import yml_to_tex
    meta['text'] = yml_to_tex(meta['text'])

def generic(template="default.tex", 
            preprocessor=None):
    def f(text, 
          meta={}, 
          env="dong", 
          fill=(lambda x, y, z : f"error with arguments {x} {y} {z}"), 
          template=template, 
          preprocessor=preprocessor,
          ):
        """
            this is the whackiest thing i've ever done and am mostly doing it for fun.
        """

        if template == "default.tex":
            #generate template name from filename
            template = f"{meta['type']}.tex"

        meta['text'] = text

        if preprocessor:
            preprocessor(meta)

        lines_out = fill(template, env=env, meta=meta)
        return lines_out
    return f

def odt(text, 
        meta={}, 
        env="dong", 
        fill=(lambda x, y, z : f"error with arguments {x} {y} {z}"), 
        template="default.tex", 
        preprocessor=None,
        ):
    return "fuck you"

def other(text, 
        meta={}, 
        env="dong", 
        fill=(lambda x, y, z : f"error with arguments {x} {y} {z}"), 
        template="default.tex", 
        preprocessor=None,
        ):
    return "fuck you"

prose = generic(template="prose.tex")
image = generic(template="image.tex")
pdf   = generic(template="pdf.tex")
poem  = generic(template="poem.tex", preprocessor=stanzatize)
yml_prose  = generic(template="prose.tex", preprocessor=ymly_tex)

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

#def yml_prose(text, meta={}, env=Environment(), fill=fill):
#    """
#        this is the driver for prose typesetting.
#        text is the text of the prose.
#        meta is metadata, eg, author, title, bio.
#        env is a jinja2 environment.
#    """
#    from .yml_to_tex import yml_to_tex
#    meta['text'] = yml_to_tex(text)
#    lines_out = fill("prose.tex", env=env, meta=meta)
#    return lines_out

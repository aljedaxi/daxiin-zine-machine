from   jinja2	import Template, Environment

def fill(template="prose.tex", env=Environment(), meta={}):
    template = env.get_template(template)

    lines_out = template.render(
        **meta,
    )
    return lines_out

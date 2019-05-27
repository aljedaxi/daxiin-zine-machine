import jinja2
from   jinja2	import Template, Environment

DEFAULT_TEMPLATE = "prose.tex"
DEFAULT_META = {
    "title" : "Untitled",
    "author": "Anonymous",
    "type"  : "poem",
    "rights": "Copyright",
}
DEFAULT_ENV = Environment(
    block_start_string	    = '\BLOCK{',
    block_end_string		= '}',
    variable_start_string	= '\VAR{',
    variable_end_string	    = '}',
    comment_start_string	= '%/*',
    comment_end_string	    = '%*/',
    line_comment_prefix	    = '%//',
    line_statement_prefix	= '%%',
    trim_blocks 			= True,
    lstrip_blocks			= True,
    autoescape			    = False,
    loader				    = jinja2.FileSystemLoader("../templates/"),
)

def fill(template=DEFAULT_TEMPLATE, env=DEFAULT_ENV, meta=DEFAULT_META):
    template = env.get_template(template)

    lines_out = template.render(
        **meta,
    )
    return lines_out

if __name__ == "__main__":
    testy_META = DEFAULT_META
    testy_META['stanzas'] = [ "like feathers falling fore the sun", "like spray between the rocks", "we were like black and white---and yet", "like two birds in a flock"],

    print(fill("poem.tex", meta=testy_META))

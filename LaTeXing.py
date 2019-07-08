from    jinja2      import Template, Environment, FileSystemLoader

ENV = Environment(
    block_start_string      = '\BLOCK{',
    block_end_string        = '}',
    variable_start_string   = '\VAR{',
    variable_end_string     = '}',
    comment_start_string    = '%/*',
    comment_end_string      = '%*/',
    line_comment_prefix     = '%//',
    line_statement_prefix   = '%%',
    trim_blocks             = True,
    lstrip_blocks           = True,
    autoescape              = False,
    loader                  = FileSystemLoader("./"),
)


def fill(template_file, meta, env=ENV):
    """
        fills a given template with data.
    """

    template = env.get_template(template_file)

    return template.render(
        **meta,
    )

import yaml
import jinja2
from   jinja2	import Template, Environment

DEFILE = "defaults.yml"
DEFAULTS = yaml.load(open(DEFILE).read())
ENV = Environment(
    **DEFAULTS['ENV']
)


if __name__ == "__main__":
    testy_META = DEFAULTS['META']
    testy_META['stanzas'] = [ "like feathers falling fore the sun", "like spray between the rocks", "we were like black and white---and yet", "like two birds in a flock"],

    print(fill("poem.tex", meta=testy_META))

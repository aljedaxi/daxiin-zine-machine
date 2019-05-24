#!/usr/bin/env python3

EMERSON = "Ralph Waldo Emerson"

def add_author(lines, author):
    return (lines[0], author, *lines[1::])

if __name__ == "__main__":
    files = [
        "Fable.tex",
        "Forbearance.tex",
        "Give_all_to_Love.tex",
        "Humble_Bee.tex",
        "The_Rhodora.tex",
        "The_Snow_Storm.tex",
        "Woodnotes2.tex",
        "Woodnotes.tex",
    ]
    author = EMERSON
    for poem in files:
        lines = [line for line in open(poem).read().split("\n")]
        new_lines = add_author(lines, author)
        open(f"{author}-{poem}", "w").write("\n".join(new_lines))

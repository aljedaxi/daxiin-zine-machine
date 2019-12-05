daxiin zine machine
=================
## Abstract
the idea is that for each new edition of the zine, you simply clone this repo into a new dir, and populate it with the articles and art for the particular issue.

## Requirements
	* python3 runtime
	* pandoc
	* latex installation with latexmk
	* ghostscript
	* if you're using arch
		```sh
			sed -i 's,/usr/bin/env python,&2,' /usr/bin/pdfbook2
		```
		it assumes python points to python2

## Files
### vars.yml
List of all the articles that will make up the edition.
Each type corresponds with a file in types_and_settings/; when build_edition comes upon it, it'll call <type>.main(text, meta, env), where 
	* text is whatever's in the associated file
	* meta is the metadata defined in the file vars.yml
	* env is a Jinja2 environment (you shouldn't have to worry about this).

the only exception to this is the `skipped' type, which is processed at the end of the run, and has access to it's own metadata, as well as the global metadata defined at the head of vars.yml .

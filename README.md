# website

My Personal Website

A simple static site generator written using Python and Jinja2.

Supports easy transliteration using the [Sanscript](https://github.com/indic-transliteration/sanscript.js/tree/3e109b09d0e69de1afb166ebd4d1ffb4e340a0c3) library by Arun Prasad. Dandas are not working idk why.

New Posts can be written in the _posts directory in markdown.


## Gh-Pages Setup Instructions
First of all, DON'T FORK IT just yet. It isn't complete and I ain't gonna sit around helping you fix it if you run into any issues.

If you are still using it, here are the instructions

1. Fork the Repo
2. Go to the repository settings and setup pages to run from the 'docs' folder of the main branch.
3. Go to Actions Tab and wait for the deploy to finish.
4.  Go to 'account_name.github.io' and hopefully your website will be live.
5. Clone Repo (See __Setup Instructions__) and make changes. Push to github to update site.

## Setup Instructions

```
git clone url_for(website)
cd website
virtualenv venv
source venv/bin/activate[.fish]
pip install requirements.txt
python build.py
```

Stop the devserver if you want to rerun the build after changing some files. (I really gotta do this better sometime)

## Goals
[x] Static Site that can be hosted on Github Pages

[x] Use Jinja2 for templating

[x] Write new Posts in Markdown, personal site data using 
yaml files and compile to html using a single command

[x] Vanilla js only

[ ] Decent Styling using Tailwind CSS

[ ] Searching Via Tags for Posts
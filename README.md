# sci_hub.py

## Forked from colindaniels@github.com/sci-hub

### C. Bryan Daniels

### `sci_hub.py` provides a simple script to download and pdf versions of PUBMED artiles as pdf documents.

def download_article(doi, mirrors=mirrors):
    """
    Takes a `doi` id for a PUBMED article then gets, downloads and saves a pdf copy to a  file.
    The file name is mangled so that `\` -> `_`. Optionally, a list of sci-hub mirrors can be provided.
    `mirrors` change regularly, so the defaults may need to be adjusted accordingly
    """

Usage within python:
import sci_hub
sci_hub.download_article('10.1038/nchembio.687')

Usage from the commnad line:
python sci_hub.py 10.1038/nchembio.687

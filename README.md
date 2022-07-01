# sci_hub.py

#### C. Bryan Daniels

#### `sci_hub.py` downloads and saves pdf versions of PUBMED articles from `sci-hub` servers.

This is a proof of concept. It should not be used to avoid copyright 

```
def download_article(doi, mirrors=mirrors):
    """
    Takes a `doi` id for a PUBMED article then gets, downloads and saves a pdf copy to a  file.
    The file name is mangled so that `\` -> `_`. Optionally, a list of sci-hub mirrors can be provided.
    `mirrors` change regularly, so the defaults may need to be adjusted accordingly
    """
```

#### Usage
Within python:
```
import sci_hub
sci_hub.download_article('10.1038/nchembio.687')
```
```
url_doi: https://sci-hub.se/10.1038/s41586-019-1046-1
url_final: https://sci-hub.se/downloads/2019-03-27/6a/10.1038@s41586-019-1046-1.pdf?download=true
10.1038/s41586-019-1046-1 downloaded -> 10.1038_s41586-019-1046-1.pdf
```

From commnad line:
```
python sci_hub.py 10.1038/nchembio.687
```
```
url_doi: https://sci-hub.se/10.1038/s41586-019-1046-1
url_final: https://sci-hub.se/downloads/2019-03-27/6a/10.1038@s41586-019-1046-1.pdf?download=true
10.1038/s41586-019-1046-1 downloaded -> 10.1038_s41586-019-1046-1.pdf
```

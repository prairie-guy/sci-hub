# sci_hub.py

#### C. Bryan Daniels

#### `sci_hub.py` downloads and saves pdf versions of PUBMED articles from `sci-hub` servers.

This is a proof of concept. It should not be used to avoid copyright restrictions.

```
def download_article(doi, mirrors=mirrors):
    """
    Takes a `doi` id for a PUBMED article then gets, downloads and saves a pdf copy to a file.
    The file name is mangled so that `\` -> `_`. Optionally, a list of sci-hub mirrors can be provided.
    `mirrors` change regularly, so the defaults may need to be adjusted accordingly.
    """
```

#### Usage
Within python:
```
import sci_hub
sci_hub.download_article('10.1586/eri.10.102')
```
```
url_doi: https://sci-hub.se/10.1586/eri.10.102
url_final: https://zero.sci-hub.se/2246/14a42f0c080bfe7ce33f82c060a7d572/bartley2010.pdf?download=true
10.1586/eri.10.102 downloaded -> 10.1586_eri.10.102.pdf
```

From commnad line:
```
python sci_hub.py 10.1586/eri.10.102
```
```
url_doi: https://sci-hub.se/10.1586/eri.10.102
url_final: https://zero.sci-hub.se/2246/14a42f0c080bfe7ce33f82c060a7d572/bartley2010.pdf?download=true
10.1586/eri.10.102 downloaded -> 10.1586_eri.10.102.pdf
```

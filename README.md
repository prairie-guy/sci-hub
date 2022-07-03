# sci_hub.py

#### C. Bryan Daniels

#### `doi2pdf.py` downloads and saves pdf versions of PUBMED articles from `sci-hub` servers.

This is a proof of concept. It should not be used to avoid copyright restrictions.

```
def doi2pdf(doi, mirrors=mirrors):
    """
    Takes a `doi` id for a PUBMED article then gets, downloads and saves a pdf copy to a  file.
    Optionally an absolute `path` can be provided.
    The saved file name is mangled so that `\` -> `_`.
    Optionally a list of sci-hub `mirrors` can be provided.
    These change regularly, so the defaults may need to be adjusted accordingly.
    """
```

#### Usage
Within python:
```python
import sci_hub
sci_hub.doi2pdf('10.1586/eri.10.102')
```
```
url_doi: https://sci-hub.se/10.1586/eri.10.102
url_final: https://zero.sci-hub.se/2246/14a42f0c080bfe7ce33f82c060a7d572/bartley2010.pdf?download=true
10.1586/eri.10.102 downloaded -> 10.1586_eri.10.102.pdf
```

From commnad line:
```bash
python doi2pdf 10.1586/eri.10.102
```
```
url_doi: https://sci-hub.se/10.1586/eri.10.102
url_final: https://zero.sci-hub.se/2246/14a42f0c080bfe7ce33f82c060a7d572/bartley2010.pdf?download=true
10.1586/eri.10.102 downloaded -> 10.1586_eri.10.102.pdf
```

```bash
echo 10.1586/eri.10.102 | ./doi2pdf.py
```
```
url_doi: https://sci-hub.se/10.1586/eri.10.102
url_final: https://zero.sci-hub.se/2246/14a42f0c080bfe7ce33f82c060a7d572/bartley2010.pdf?download=true
10.1586/eri.10.102 downloaded -> 10.1586_eri.10.102.pdf
```



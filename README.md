# sci_hub

#### C. Bryan Daniels

### `doi2pdf.py` downloads and saves pdf versions of PUBMED articles from `sci-hub` servers.

This is a proof of concept. It should not be used to avoid copyright restrictions.

```python
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
from doi2pdf import doi2pdf
doi2pdf('10.1586/eri.10.102')
```
```
url_doi: https://sci-hub.se/10.1586/eri.10.102
url_final: https://zero.sci-hub.se/2246/14a42f0c080bfe7ce33f82c060a7d572/bartley2010.pdf?download=true
10.1586/eri.10.102 downloaded -> 10.1586_eri.10.102.pdf
```

From command line:
```bash
python doi2pdf.py 10.1586/eri.10.102
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

### `pmid2doi.py` takes a PubMed ID and returns (`doi,pmid`)

``` python
def pmid2doi(pmid):
    """
    Takes a PubMed ID `pmid` and returns a tuple (`doi`,`pmid`)
    The signatures from within python and from the command line differ:
    `pmid2doi(pmid) -> (doi,pmid)`
    `./pmid2doi.py - > (doi,fname,pmid)`
    """
```

#### Usage
Within python:
```python
from pmid2doi import pmid2doi
print(pmid2doi('30952685')) 
```
```
('10.1101/pdb.prot098368', '30952685')  
```

From commnad line:
```bash
python doi2pdf 30952685
```
```
10.1101/pdb.prot098368, 10.1101_pdb.prot098368.pdf, 30952685
```


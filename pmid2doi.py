#!/usr/bin/env python

from pubmed_bibtex import bibtex_entry_from_pmid
import re, sys

# NOTE: The signatures from within python and from the command line differ:
# pmid2doi(pmid) -> (doi,pmid)
# ./pmid2doi.py - > (doi,fname,pmid)

def pmid2doi(pmid):
    """
    Takes a PubMed ID `pmid` and returns a tuple (`doi`,`pmid`)
    The signatures from within python and from the command line differ:
    `pmid2doi(pmid) -> (doi,pmid)`
    `./pmid2doi.py - > (doi,fname,pmid)`
    """
    btx = bibtex_entry_from_pmid(pmid)
    doi = re.findall(r'dx\.doi\.org\/(.*?)}', btx)[0]
    return doi, pmid

if __name__ == '__main__':
    if len(sys.argv) == 2:
        doi, pmid = pmid2doi(sys.argv[1])
        fname = f'{doi.replace("/","_")}.pdf'
        print(f"{doi},{fname},{pmid}")
    elif len(sys.argv) == 1:
        print("doi,fname,pmid")
        for line in sys.stdin:
            doi, pmid = pmid2doi(line.rstrip('\n'))
            fname = f'{doi.replace("/","_")}.pdf'
            print(f"{doi},{fname},{pmid}")
    else:
        print("usage: ./pmid2doi.py doi OR  echo pmid | ./pmid2doi ")

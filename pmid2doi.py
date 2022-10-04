#!/usr/bin/env python

from pmid2bibtex import getReference
import re, sys

# NOTE: The signatures from within python and from the command line differ.
# This allows the command line option to create csv files
# pmid2doi(pmid) -> (doi,pmid)
# ./pmid2doi.py - > (doi,fname,pmid)

def pmid2doi(pmid):
    """
    Takes a PubMed ID `pmid` and returns a tuple (`doi`,`pmid`)
    The signatures from within python and from the command line differ:
    `pmid2doi(pmid) -> (doi,pmid)`
    `./pmid2doi.py - > (doi,fname,pmid)`
    """
    pmid, reference = getReference(pmid)
    doi = reference['doi']
    return doi, pmid

if __name__ == '__main__':
    # pmid =  30440093
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

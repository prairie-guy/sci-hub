#!/usr/bin/env python

from pubmed_bibtex import bibtex_entry_from_pmid
import re, sys

def pmid2doi(pmid):
    btx = bibtex_entry_from_pmid(pmid)
    doi = re.findall(r'dx\.doi\.org\/(.*?)}', btx)[0]
    return pmid, doi

if __name__ == '__main__':
    # pmid = "31597913"
    # print(pmid2doi(pmid))
    if len(sys.argv) == 2:
        pmid, doi = pmid2doi(sys.argv[1])
        fname = f'{doi.replace("/","_")}.pdf'
        print(f"{doi},{fname},{pmid}")
    elif len(sys.argv) == 1:
        print("doi,fname,pmid")
        for line in sys.stdin:
            pmid, doi = pmid2doi(line.rstrip('\n'))
            fname = f'{doi.replace("/","_")}.pdf'
            print(f"{doi},{fname},{pmid}")
    else:
        print("usage: ./pmid2doi.py doi OR  echo pmid | ./pmid2doi ")

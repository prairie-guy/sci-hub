#!/usr/bin/env python
#
# pmid2pdf.py
# Forked from colindaniels@github.com/sci-hub
#
# C. Bryan Daniels
# July 1, 2022
#

import sys, re, requests
from pathlib import Path
from pmid2bibtex import getReference

# 21079590
# 35511947
# 32015498
# 31597913

def get_pdf(doi, mirror):
    """
    Requires a `doi` id for a PUBMED article and a specific `mirror` of sci-hub.
    If found, returns a pdf version of the article
    """
    url_doi = f'https://{mirror}/{doi}'
    print(f'url_doi: {url_doi}')
    resp = requests.get(url_doi).text
    href = re.findall(r"location\.href=(.*true)", resp)
    if href: href = href[0].replace("\'", '')
    else: return None
    url_final = f'https:{href}' if href.startswith('//') else f'https://{mirror}{href}'
    #print(f'url_final: {url_final}')
    resp = requests.get(url_final)
    return None if resp.status_code == 404 else resp.content

def pmid2pdf(pmid, path=None, mirrors=('sci-hub.se', 'sci-hub.st', 'sci-hub.ru')):
    """
    Takes a `pmid` id for a PUBMED article then gets, downloads and saves a pdf copy to a file.
    Optionally an absolute `path` can be provided. Mirrors can also be provided.
    These `change regularly, so the defaults may need to be adjusted accordingly.
    """
    for mirror in mirrors:
        id, reference = getReference(pmid)
        doi = reference['doi']
        ref_id = reference['ref_id']
        fname = f'{ref_id}.pdf'
        fname = Path(path)/fname if path else Path(fname)
        if fname.exists(): return(f'Not downloaded: {fname}')
        print(fname)
        pdf = get_pdf(doi, mirror)
        if pdf:
            with open(fname, 'wb') as fd:
                fd.write(pdf)
                print(f'downloaded -> {fname}')
            return
    print(f'failed to download -> {fname}')

if __name__ == '__main__':
    default_path = "/home/cdaniels/uofc/Articles/articles-lib"
    #print(f"edit if needed: default_path={default_path} Edit `default_path`")
    if len(sys.argv) == 3:
        pmid, path = sys.argv[1], sys.argv[2]
        pmid2pdf(pmid, path)
    elif len(sys.argv) == 2:
        pmid = sys.argv[1]
        pmid2pdf(pmid, default_path)
    elif len(sys.argv) == 1:
        for line in sys.stdin:
            pmid2pdf(line.rstrip('\n'), default_path)
    else:
        print("usage: ./pmid2pdf.py `pmid` OR ./pmid2pdf.py `pmid` `path`  OR  echo `pmid` | ./pmid2pdf.py ")

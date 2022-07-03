#!/usr/bin/env python
#
# doi2pdf.py
# Forked from colindaniels@github.com/sci-hub
#
# C. Bryan Daniels
# July 1, 2022
#

import requests, re, sys
from pathlib import Path

mirrors=('sci-hub.se', 'sci-hub.st', 'sci-hub.ru')

def get_pdf(doi, mirror):
    """
    Takes a `doi` id for a PUBMED article and a specific `mirror` of sci-hub.
    If found, returns a pdf version of the article
    """
    url_doi = f'https://{mirror}/{doi}'
    print(f'url_doi: {url_doi}')
    resp = requests.get(url_doi).text
    href = re.findall(r"location\.href=(.*true)", resp)
    if href: href = href[0].replace("\'", '')
    else: return None
    url_final = f'https:{href}' if href.startswith('//') else f'https://{mirror}{href}'
    print(f'url_final: {url_final}')
    resp = requests.get(url_final)
    return None if resp.status_code == 404 else resp.content

def download_article(doi, path=None, mirrors=mirrors):
    """
    Takes a `doi` id for a PUBMED article then gets, downloads and saves a pdf copy to a  file.
    Optionally an absolute `path` can be provided.
    The saved file name is mangled so that `\` -> `_`.
    Optionally a list of sci-hub `mirrors` can be provided.
    These `change regularly, so the defaults may need to be adjusted accordingly.
    """
    for mirror in mirrors:
        doi = doi.replace("https://dx.doi.org/","") # Not always present
        fname = f'{doi.replace("/","_")}.pdf'
        fname = Path(path)/fname if path else Path(fname)
        print(fname)
        pdf = get_pdf(doi, mirror)
        if pdf:
            with open(fname, 'wb') as fd:
                fd.write(pdf)
                print(f'downloaded -> {fname}')
            break

if __name__ == '__main__':
    #doi = '10.1586/eri.10.102'
    # if len(sys.argv) == 3:
    #     doi, path = sys.argv[1], sys.argv[2]
    # else:
    #     doi, path = sys.argv[1], None
    # download_article(doi, path)
    path = "/home/cdaniels/uofc/articles-lib"
    if len(sys.argv) == 2:
        doi = sys.argv[1]
        download_article(doi, path)
    elif len(sys.argv) == 1:
        for line in sys.stdin:
            download_article(line.rstrip('\n'), path)
    else:
        print("usage: ./doi2pdf.py doi OR  echo doi | ./doi2pdf.py ")

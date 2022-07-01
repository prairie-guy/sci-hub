#!/usr/bin/env python

#
# sci_hub.py
# Forked from colindaniels@github.com/sci-hub
#
# C. Bryan Daniels
# July 1, 2022
#

import requests, re, sys

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

def download_article(doi, mirrors=mirrors):
    """
    Takes a `doi` id for a PUBMED article then gets, downloads and saves a pdf copy to a  file.
    The file name is mangled so that `\` -> `_`. Optionally, a list of sci-hub mirrors can be provided.
    `mirrors` change regularly, so the defaults may need to be adjusted accordingly
    """
    for mirror in mirrors:
        fname = f'{doi.replace("/","_")}.pdf'
        pdf = get_pdf(doi, mirror)
        if pdf:
            with open(f'{fname}', 'wb') as fd:
                fd.write(pdf)
                print(f'{doi} downloaded -> {fname}')
            break

if __name__ == '__main__':
    #doi = '10.1586/eri.10.102'
    doi = sys.argv[1]
    download_article(doi)

#!/usr/bin/env python
import re, sys
from pathlib import Path
from pmid2bibtex import getReference, formatReference
# Largely based upon code from: https://github.com/zhuchcn/pubmed-bib

# 21079590
# 35511947
# 32015498
# 31597913
# path = '/home/cdaniels/uofc/bibtex-lib/refs.bib'


def pmid2bib(id, output_file):
    "Takes pubmed `id`, `output_file` and appends a BibTex record to `output_file`"
    #if not Path(output_file).is_file(): return(f"No output_file: {output_file} found")
    id_ref = getReference(id)
    if not id_ref: return None
    if Path(output_file).is_file() and re.search(f'{id}', open(output_file,"r").read()):
        return(f'Not saved: pmid={id} exits in {output_file}')
    with open(output_file, "a") as f:
        f.write(formatReference(id_ref))
    print(f'Appended bibtex: {id} to {output_file}')

if __name__ == '__main__':
    #pmid = 30440093
    default_path = "/home/cdaniels/uofc/bibtex-lib/refs.bib"
    #print(f"edit if needed: default_path={default_path} Edit `default_path`")
    if len(sys.argv) == 3:
        pmid, path = sys.argv[1], sys.argv[2]
        pmid2bib(pmid, path)
    elif len(sys.argv) == 2:
        pmid = sys.argv[1]
        pmid2bib(pmid, default_path)
    elif len(sys.argv) == 1:
        for line in sys.stdin:
            pmid2bib(line.rstrip('\n'), default_path)
    else:
        print("usage: ./pmid2bib.py `pmid` OR ./pmid2bib.py `pmid` `path`  OR  echo `pmid` | ./pmid2bib.py ")



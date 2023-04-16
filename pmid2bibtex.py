#!/usr/bin/env python
import requests, re, sys
from pathlib import Path
# Modified from: https://github.com/zhuchcn/pubmed-bib

# 21079590
# 35511947
# 32015498
# 31597913
# path = '/home/cdaniels/uofc/Articles/bibtex-lib/refs.bib'

def getReference(id):
    """
    Takes a pubmed `id` -> (id, ref)
    `ref` is a dict, originially returned by pubmed API.
    With error `pubmed_error(id)` -> (id, None)
    """
    url_format = 'https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/'
    queryParams = {'format': 'csl', 'id': id} # Parameters for query
    try:
        resp = requests.get(url_format, params = queryParams)
        if resp.status_code != 200: return pubmed_error(id)
        reference = resp.json()
        if not reference: return pubmed_error(id)
    except:
        return pubmed_error(id)

    title = reference['title'] if 'title' in reference.keys() else ''
    title = re.sub('<.*?>', '', title) # Remove html tags

    authors = reference['author'] if 'author' in reference.keys() else ''
    authorList = []
    for author in authors:
        if ('family' in author.keys()) and ('given' in author.keys()):
            authorList.append(author['family'] + ', ' + author['given'])
        elif ('family' in author.keys()) and ('given' not in author.keys()):
            authorList.append(author['family'])
        elif ('family' not in author.keys()) and ('given' in author.keys()):
            authorList.append(author['given'])
        else:
            continue
    author = ' and '.join(authorList)

    journal_long = reference.get('container-title') or ''
    journal = reference.get('container-title-short') or ''
    volume = reference.get('volume') or ''
    pages = reference.get('page') or ''
    doi = reference.get('DOI')
    doi = f'http://doi.org/{doi}'

    if 'issued' in reference.keys():
        year = reference['issued']['date-parts'][0][0]
    elif 'epub-date' in reference.keys():
        year = reference['epub-date']['date-parts'][0][0]

    ref_title = "".join(title.title().split()[:3])
    ref_title = re.sub(r'[^A-Za-z0-9]+', '', ref_title)

    ref_year = str(year)
    ref_journal = journal.replace(" ", "")
    ref_id = f'{ref_title}{ref_year}{ref_journal}'

    file = f'{ref_id}.pdf'

    ref = {
        "ref_id":ref_id,
        "title":title,
        "author":author,
        "journal_long":journal_long,
        "journal":journal,
        "volume":volume,
        "pages":pages,
        "year":year,
        "pmid":id,
        "doi":doi,
        "file":file}

    return id, ref


def pubmed_error(id):
    print(f"warning: No PubMed `reference` returned from `getReference({id})`")
    return None


def formatReference(id_ref):
    "Takes `id_ref` (id,reference) ->  BibTex record"
    if not id_ref: return None
    id, ref = id_ref
    output = f'''@article{{{ ref['ref_id']},
    title={{{ref['title']}}},
    author={{{ref['author']}}},
    {"journal-long"}={{{ref['journal_long']}}},
    {"journal"}={{{ref['journal']}}},
    volume={{{ref['volume']}}},
    pages={{{ref['pages']}}},
    year={{{ref['year']}}},
    PMID={{{ref['pmid']}}},
    DOI={{{ref['doi']}}},
    file={{{ref['file']}}}
}}
    '''
    return output


def pmid2bibtex(id):
    "Takes pubmed `id` and prints BibTex record"
    id_ref = getReference(id)
    if not id_ref: return None
    output = formatReference(id_ref)
    print(output)


def saveReference(id, output_file):
    "Takes pubmed `id`, `output_file` and appends a BibTex record to `output_file`"
    if not Path(output_file).is_file(): return(f"No output_file: {output_file} found")
    id_ref = getReference(id)
    if not id_ref: return None
    if re.search(f'{id}', open(output_file,"r").read()):
        return(f'Not saved: pmiid=c{id} exits in {output_file}')
    with open(output_file, "a") as f:
        f.write(formatReference(id_ref))
    print(f'Appended bibtex: {id} to {output_file}')

if __name__ == '__main__':
    #pmid = 30440093
    default_path = "/home/cdaniels/uofc/Articles/bibtex-lib/refs.bib"
    #print(f"edit if needed: default_path={default_path} Edit `default_path`")
    if len(sys.argv) == 3:
        pmid, path = sys.argv[1], sys.argv[2]
        pmid2bibtex(pmid, path)
    elif len(sys.argv) == 2:
        pmid = sys.argv[1]
        pmid2bibtex(pmid, default_path)
    elif len(sys.argv) == 1:
        for line in sys.stdin:
            pmid2bibtex(line.rstrip('\n'))
    else:
        print("usage: ./pmid2bibtex.py `pmid` OR ./pmid2bibtex.py `pmid` `path`  OR  echo `pmid` | ./pmid2bibtex.py ")

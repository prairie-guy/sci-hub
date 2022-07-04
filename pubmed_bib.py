#!/usr/bin/env python
import click, requests, re, sys
from pathlib import Path
# Largely based upon code from: https://github.com/zhuchcn/pubmed-bib

# 30440093
# 21079590
# 35511947
# 32015498
# 31597913
#

def getReference(id):
    """
    Takes a pubmed `id` -> (id, reference)
    `reference` is a dict returned by pubmed API.
    With error `pubmed_error(id)` -> (id, None)
    """
    url_format = 'https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/'
    queryParams = {'format': 'csl', 'id': id} # Parameters for query
    try:
        resp = requests.get(url_format, params = queryParams)
        if resp.status_code != 200: return pubmed_error(id)
        reference = resp.json()
        if not reference: return pubmed_error(id)
        return id, reference
    except:
        return pubmed_error(id)

def pubmed_error(id):
    print(f"warning: No PubMed `reference` returned from `getReference({id})`")
    return None

def formatReference(id_ref, use_short=True):
    "Takes `id_ref` (id,reference) ->  BibTex record"
    if not id_ref: return None
    id, reference = id_ref
    title = reference['title'] if 'title' in reference.keys() else ''
    title = re.sub("<sub>(.+)</sub>", "$_{\\1}$", title) # convert to latex
    title = re.sub("<sup>(.+)</sup>", "$^{\\1}$", title)

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

    journal_long = reference.get('container-title') or ''
    journal_short = reference.get('container-title-short') or ''
    volume = reference.get('volume') or ''
    page = reference.get('page') or ''
    doi = reference.get('DOI')
    file = f'{doi.replace("/","_")}.pdf' # Mangle doi -> fname
    
    if 'issued' in reference.keys():
        year = reference['issued']['date-parts'][0][0]
    elif 'epub-date' in reference.keys():
        year = reference['epub-date']['date-parts'][0][0]

    ref_id = authors[0]["family"].lower() \
            if "family" in authors[0].keys() else authors[0]
    #ref_id += str(year) + title.split(' ')[0].lower()
    ref_id += str(year) + journal_short.replace(" ", "")

    output = f'''@article{{{ ref_id },
    title={{{title}}},
    author={{{' and '.join(authorList)}}},
    {"journal-long" if use_short else "journal"}={{{journal_long}}},
    {"journal" if use_short else "journal-short"}={{{journal_short}}},
    volume={{{volume}}},
    pages={{{page}}},
    year={{{year}}},
    PMID={{{id}}},
    DOI={{{doi}}},
    file={{{file}}}
}}
'''
    return output

def showReference(id, use_short=True):
    "Takes pubmed `id` and prints BibTex record"
    id_ref = getReference(id)
    if not id_ref: return None
    output = formatReference(id_ref, use_short)
    click.echo(output)

def saveReference(id, output_file, use_short=True):
    "Takes pubmed `id`, `output_file` and appends a BibTex record to `output_file`"
    if not Path(output_file).is_file(): return(f"No output_file: {output_file} found")
    id_ref = getReference(id)
    if not id_ref: return None
    with open(output_file, "a") as f:
        f.write(formatReference(id_ref, use_short))
    print(f'Appended bibtex: {id} to {output_file}')

def convertReferences(input_file, output_file=None):
    # Takes newline deliminated file `input_file` of pubmed `ids` writes BibTex records to file `output_file`
    if not Path(input_file).is_file(): return(f"No input_file: {input_file} found")
    if output_file and Path(output_file).is_file():
        return(f"Output_file: {output_file} already exists")
    n_fail = 0
    with open(input_file) as ih:
        oh = open(output_file, 'w') if output_file else sys.stdout
        for id in ih:
            id_ref = getReference(id.rstrip())
            if not id_ref:
                n_fail += 1
            else:
                btx = formatReference(id_ref)
                print(btx, file=oh)
    if n_fail > 0: print(f'{n_fail} bibtex records not found')

@click.command()
@click.option('--id', default=None,  help="The PubMed PMID.")
@click.option('--input-file', default=None,
              help='A text file with list of PMID')
@click.option('--output-file', default=None,
              help='The output file to store BibTex styled references')

def pubMed2BibTex(id, input_file, output_file):
    '''
    Retrieve article reference from PubMed in BibTex format.
    '''
    if id:
        if output_file:
            saveReference(id, output_file)
        else:
            showReference(id)
    elif output_file and input_file:
            convertReferences(input_file, output_file)
    elif input_file:
            convertReferences(input_file)
    else:
        print("usage: ./pubmed_bib.py --id [--input-file] [--output-file]")

if __name__ == '__main__':
    pubMed2BibTex()

import click
import requests
import json
import re

# Largely Based upon code from: https://github.com/zhuchcn/pubmed-bib

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
    
    if 'issued' in reference.keys():
        year = reference['issued']['date-parts'][0][0]
    elif 'epub-date' in reference.keys():
        year = reference['epub-date']['date-parts'][0][0]    

    ref_id = authors[0]["family"].lower() \
            if "family" in authors[0].keys() else authors[0]
    ref_id += str(year) + title.split(' ')[0].lower()

    output = f'''@article{{{ ref_id },
    title={{{title}}},
    author={{{' and '.join(authorList)}}},
    {"journal-long" if use_short else "journal"}={{{journal_long}}},
    {"journal" if use_short else "journal-short"}={{{journal_short}}},
    volume={{{volume}}},
    pages={{{page}}},
    year={{{year}}},
    PMID={{{id}}}
}}
'''
    return output

def showReference(id, use_short=True):
    "Takes pubmed `id` and prints BibTex record"
    id_ref = getReference(id)
    if not id_ref: return None
    output = formatReference(id_ref, use_short)
    click.echo(output)
    return

def saveReference(id, path, use_short=True):
    "Takes pubmed `id`, `path` and appends a BibTex record to `path`"
    id_ref = getReference(id)
    if not id_ref: return None
    with open(path, "a") as f:
        f.write(formatReference(id_ref, use_short))
    return

def convertReferences(input_file, output_file):
    # Read all PMIDs in
    id = []
    successNumber, failNumber = 0, 0
    with open(input_file) as ih:
        with open(output_file, 'w') as oh:
            for line in ih:
                ref = getReference(line.rstrip())
                print(ref)
                if 'status' in ref.keys() and ref['status'] == 'error' :
                    print(f'PMID {line.rstrip()} NOT FOUND')
                    failNumber += 1
                else: 
                    ref = formatReference(ref)
                    successNumber += 1
                    oh.write(ref+'\n')
    print(f'{successNumber} reference{"s" if successNumber > 1 else ""} ' +\
          f'retrieved.\n{failNumber} reference' +\
          f'{"s" if failNumber > 1 else ""} ' +\
          f'not found.')
    return

@click.command()
@click.option('--id', default=None,  help="The PubMed PMID.")
@click.option('--input-file', default=None,
              help='A text file with list of PMID')
@click.option('--output-file', default=None,
              help='The output file to store BibTex styled references')
@click.option('--short-journal/--long-journal', default=False,
              help="Use short journal name")


def pubMed2BibTex(id, input_file, output_file, short_journal):
    '''
    Retrieve article reference from PubMed in BibTex format.
    '''
    if id:
        if output_file:
            saveReference(id, output_file, short_journal)
        else:
            showReference(id, short_journal)
    elif input_file and output_file:
        convertReferences(input_file, output_file, short_journal)
    else:
        return

if __name__ == '__main__':
    pubMed2BibTex()

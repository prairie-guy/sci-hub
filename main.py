import requests, re, sys

def download_pdf(doi, mirror):
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

def get_article(doi, mirrors=('sci-hub.se', 'sci-hub.st', 'sci-hub.ru')):
    for mirror in mirrors:
        fname = f'{doi.replace("/","_")}.pdf'
        pdf = download_pdf(doi, mirror)
        if pdf:
            with open(f'{fname}', 'wb') as fd:
                fd.write(pdf)
                print(f'{doi} downloaded -> {fname}')
            break

if __name__ == '__main__':
    #doi = '10.1038/nchembio.687'
    doi = sys.argv[1]
    get_article(doi)

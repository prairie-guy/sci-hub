import requests
import re
from bs4 import BeautifulSoup

def get_content(query, m_domain):
    url = f'https://{m_domain}/{query}'
    #print(url)
    #regex ew
    first_response = requests.get(url)
    soup = BeautifulSoup(first_response.text, "html.parser")

    href = soup.find('button').attrs['onclick'].replace('location.href=', '').replace("\'", '')
    if href.startswith('//'):
        formatted_domain = f'https:{href}'
        print(formatted_domain)
    else:
        formatted_domain = f'https://{m_domain}{href}'
        print(formatted_domain)
    '''
    if not re.findall(r'id = "header".*>', first_response.text):
        return { 'success': False, 'response': None }
    else:

        #raw = re.findall(r'id = "header".*>', first_response.text)[0]
        #domain = re.findall('\/\/.*\/', raw)[0].replace('/', '')

        raw_params = re.findall("location\.href=.*", first_response.text)[0]
        print(raw_params)
        params = re.findall('\/\/.*true', raw_params)[0].replace('//', '')
        response = requests.get(f'https://{params}')
        '''
    response = requests.get(formatted_domain)

    if response.status_code == 404:
        return { 'success': False, 'response': None }
    else:
        return { 'success': True, 'response': response.content }

def content_to_pdf(content, filename):
    with open(filename, 'wb') as f:
        f.write(content)

def downlaod_pdf_from_query(query, mirrors=('sci-hub.se', 'sci-hub.st', 'sci-hub.ru')):
    for m in mirrors:
        #print(m)
        res = get_content(query, m)
        if res['success']:
            content_to_pdf(res['response'], f'{m}.pdf')
            break
    print('done')

if __name__ == '__main__':
    downlaod_pdf_from_query('10.1038/nchembio.687')

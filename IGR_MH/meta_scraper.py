from json import loads
from typing import Dict
from datetime import datetime

from prefect import task
from requests import Session
from bs4 import BeautifulSoup as bs


HOMEPAGE = 'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/registrationmaster/'
SESSION = Session()

@task
def get_districts() -> Dict:
    meta_data = {
                'site': 'https://isarita.igrmaharashtra.gov.in/',
                'url': 'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/registrationmaster/',
                'scraped_time': datetime.now(),

            }
    SESSION.headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/registrationmaster/'
        }
    )
    response = SESSION.get(HOMEPAGE)
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        district_drop_down = soup.find('select', {'id':'district_id1'})
        if district_drop_down:
            districts = {
                district.text: district['value'] 
                for district in district_drop_down.find_all('option')
                if district['value']
            }
            meta_data.update({'districts' : districts})
        else:
            meta_data.update({'exception': 'district drop down not available as per given selector'})
    else:
        meta_data.update({'exception': f'non 200 response code for URL -- {HOMEPAGE}'})
    return meta_data

@task
def get_sros(district_name: str, district_code: str) -> Dict:
    print(district_name)
    print('='*50)
    meta_data = {
        'scrapre_time': datetime.now(),
        'district_code': district_code,
        'district_name': district_name
    }
    url = f'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/get_office_data?district={district_code}'
    SESSION.headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/registrationmaster/'            
        }
    )
    response = SESSION.get(url)
    if response.status_code == 200:
        sro_data = loads(response.text)
        sros = []
        for sro_code, sro_name in sro_data.items():
            sros.append(
                {
                    'sro_name': sro_name,
                    'sro_code': sro_code
                }
            )
        meta_data.update(
            {
                'sro_code': sros
            }
        )
    return meta_data

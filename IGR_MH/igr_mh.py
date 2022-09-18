from os import getcwd
from os.path import join

from requests import Session
from bs4 import BeautifulSoup as bs
from python_anticaptcha import AnticaptchaClient, ImageToTextTask


HOMEPAGE_URL = 'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/registrationmaster/'


def solve_captcha_image(img):
    api_key = '504864cda4cdfdf3a8c46a1e809a7edb'
    client = AnticaptchaClient(api_key)
    task = ImageToTextTask(img)
    job = client.createTask(task)
    job.join()
    return job.get_captcha_text()


def solve_captcha(session_cookies):
    captcha_session = Session()
    captcha_session.cookies.set(session_cookies.keys()[0], session_cookies.values()[0])
    captcha_url = 'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/get_captcha'
    captcha_response = captcha_session.get(captcha_url)
    with open('captcha.png', 'wb') as _f: _f.write(captcha_response.content)
    captcha_text = solve_captcha_image(open(join(getcwd(), 'captcha.png'), 'rb'))
    return captcha_text


def get_tokens(page_html):
    soup = bs(page_html, 'html.parser')
    token_key = soup.find('input', {'name':'data[_Token][key]'})['value']
    csrf_token = soup.find('input', {'id':'csrftoken'})['value']
    token_fields = soup.find('input', {'name':'data[_Token][fields]'})['value']
    return {
        'token_key': token_key,
        'csrf_token': csrf_token,
        'token_fields': token_fields
    }


def start_request():
    igr_session = Session()
    igr_session.headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://isarita.igrmaharashtra.gov.in',
            'Referer': 'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/registrationmaster/',
        }
    )
    homepage_response = igr_session.get(HOMEPAGE_URL)
    captcha_text = solve_captcha(igr_session.cookies)
    tokens = get_tokens(homepage_response.content)
    start_scraping(igr_session, captcha_text, tokens)


def start_scraping(igr_session, captcha, tokens):
    for doc_no in range(0, 10):
        data = [
            ('_method', 'POST'),
            ('data[_Token][key]', tokens.get('token_key')),
            ('_method', 'POST'),
            ('data[_Token][key]', tokens.get('token_key')),
            ('data[registrationmaster][file_type]', 'R'),
            ('data[registrationmaster][year1]', '2015'),
            ('data[registrationmaster][district_id1]', '1'),
            ('data[registrationmaster][sroname]', '287'),
            ('data[registrationmaster][document_no]', doc_no),
            ('data[registrationmaster][captcha]', captcha),
            ('data[registrationmaster][csrftoken]', tokens.get('csrf_token')),
            ('btnadd', ''),
            ('tableparty_length', '5'),
            ('data[_Token][fields]', tokens.get('token_fields')),
            ('data[_Token][unlocked]', ''),
        ]
        data_response = igr_session.post('https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/registrationmaster/', data=data)
        with open(f'igr_test{doc_no}.html', 'w') as _f:
            _f.write(data_response.text)


if __name__ == '__main__':
    start_request()
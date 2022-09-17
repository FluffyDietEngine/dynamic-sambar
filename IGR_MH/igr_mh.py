import requests
from python_anticaptcha import AnticaptchaClient, ImageToTextTask

def solve_captcha(img):
    api_key = '504864cda4cdfdf3a8c46a1e809a7edb'
    client = AnticaptchaClient(api_key)
    task = ImageToTextTask(img)
    job = client.createTask(task)
    job.join()
    return job.get_captcha_text()
    

session = requests.Session()

captcha_url = 'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/get_captcha'

captcha_response = session.get(captcha_url)

with open('captcha.png', 'wb') as _f: _f.write(captcha_response.content)

captcha_text = solve_captcha(open('/home/santhosh/Desktop/projects/prefect_practice/captcha.png', 'rb'))

print(captcha_text)


# import pdb; pdb.set_trace()
cookies = {
    'CAKEPHP': 'jn0jr5a7u8bo3049fgvch553g6',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://isarita.igrmaharashtra.gov.in',
    'Connection': 'keep-alive',
    'Referer': 'https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/registrationmaster/',
    # 'Cookie': 'CAKEPHP=jn0jr5a7u8bo3049fgvch553g6',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}

data = [
    ('_method', 'POST'),
    ('data[_Token][key]', '19397d281df9f402dc6316778a84f3cece100aee'),
    ('_method', 'POST'),
    ('data[_Token][key]', '19397d281df9f402dc6316778a84f3cece100aee'),
    ('data[registrationmaster][file_type]', 'R'),
    ('data[registrationmaster][year1]', '2015'),
    ('data[registrationmaster][district_id1]', '1'),
    ('data[registrationmaster][sroname]', '287'),
    ('data[registrationmaster][document_no]', '1'),
    ('data[registrationmaster][captcha]', captcha_text),
    ('data[registrationmaster][csrftoken]', '31005172407270'),
    ('btnadd', ''),
    ('tableparty_length', '5'),
    ('data[_Token][fields]', '09bbab3ed5f40d67776ecdaea55ecf325a770441%3Aregistrationmaster.csrftoken'),
    ('data[_Token][unlocked]', ''),
]

response = requests.post('https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/registrationmaster/', cookies=cookies, headers=headers, data=data)

print(response)

with open('s.html', 'w') as _file:
    _file.write(response.text)
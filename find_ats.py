import requests
import re

urls = [
    'https://www.americanexpress.com/en-us/careers/search-jobs/',
    'https://www.genpact.com/careers/job-hub',
    'https://www.bain.com/careers/roles/',
    'https://careers.gs.com/',
    'https://careers.ey.com/',
    'https://jobs.bnymellon.com/',
    'https://careers.bankofamerica.com/en-us/job-search',
    'https://careers.jpmorgan.com/global/en/home'
]

headers = {'User-Agent': 'Mozilla/5.0'}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        # Look for workday, eightfold, or taleo
        matches = re.findall(r'https://[^/\"\']*\.(?:myworkdayjobs\.com|eightfold\.ai|taleo\.net|icims\.com|avature\.net)[^\"\']*', r.text)
        
        # also check for redirects
        if 'myworkdayjobs' in r.url or 'eightfold' in r.url or 'taleo' in r.url:
            matches.append(r.url)
            
        print(f'{url}: {set(matches)}')
    except Exception as e:
        print(f'{url}: Failed - {e}')

import requests

workday_tests = [
    ("Bain", "bain", "Bain_External_Career_Site", "wd1"),
    ("Goldman", "goldmansachs", "GS_External", "wd1"),
]

for name, tenant, portal, wd in workday_tests:
    url = f"https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{portal}/jobs"
    try:
        r = requests.post(url, json={'appliedFacets': {}, 'limit': 1, 'offset': 0, 'searchText': ''}, headers={'Content-Type': 'application/json'}, timeout=5)
        print(f"Workday {name} ({tenant}/{portal}): {r.status_code}")
    except:
        pass
        
eightfold_tests = [
    ("Amex", "aexp"),
    ("Genpact", "genpact"),
    ("BNY", "bnymellon"),
]

for name, domain in eightfold_tests:
    url = f"https://{domain}.eightfold.ai/api/apply/v2/jobs"
    try:
        r = requests.get(url, params={'domain': f'{domain}.eightfold.ai', 'limit': 1}, timeout=5)
        print(f"Eightfold {name} ({domain}): {r.status_code}")
    except:
        pass

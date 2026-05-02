import requests

workday_tests = [
    ("Amex", "aexp", "aexp_careers"),
    ("Amex", "aexp", "Amex"),
    ("Bain", "bain", "Bain"),
    ("Bain", "bain", "Bain_Careers"),
    ("BofA", "bofa", "Bank_of_America_Careers"),
    ("BofA", "ghr", "lateral-us"),
    ("Goldman", "goldmansachs", "GS"),
    ("Goldman", "goldmansachs", "Goldman_Sachs"),
    ("Genpact", "genpact", "Genpact_External_Career_Site"),
    ("EY", "ey", "EY_External_Careers"),
    ("JPMC", "jpmc", "Jpmc"),
    ("JPMC", "jpmc", "jpmorgan")
]

for name, tenant, portal in workday_tests:
    url = f"https://{tenant}.wd1.myworkdayjobs.com/wday/cxs/{tenant}/{portal}/jobs"
    try:
        r = requests.post(url, json={'appliedFacets': {}, 'limit': 1, 'offset': 0, 'searchText': ''}, headers={'Content-Type': 'application/json'}, timeout=5)
        print(f"Workday wd1 {name} ({tenant}/{portal}): {r.status_code}")
    except:
        pass
        
    url3 = f"https://{tenant}.wd3.myworkdayjobs.com/wday/cxs/{tenant}/{portal}/jobs"
    try:
        r = requests.post(url3, json={'appliedFacets': {}, 'limit': 1, 'offset': 0, 'searchText': ''}, headers={'Content-Type': 'application/json'}, timeout=5)
        if r.status_code != 403:
            print(f"Workday wd3 {name} ({tenant}/{portal}): {r.status_code}")
    except:
        pass
        
    url5 = f"https://{tenant}.wd5.myworkdayjobs.com/wday/cxs/{tenant}/{portal}/jobs"
    try:
        r = requests.post(url5, json={'appliedFacets': {}, 'limit': 1, 'offset': 0, 'searchText': ''}, headers={'Content-Type': 'application/json'}, timeout=5)
        if r.status_code != 403:
            print(f"Workday wd5 {name} ({tenant}/{portal}): {r.status_code}")
    except:
        pass

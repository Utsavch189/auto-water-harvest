import requests

def has_internet():
    try:
        requests.get('https://google.com')
        return True
    except:
        return False

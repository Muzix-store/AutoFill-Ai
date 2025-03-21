# HTML get request function
import requests

def get_html (link):
    r = requests.get(url=link, auth=('user', 'pass'))
    with open ("./HTML/parsed.html", 'w') as file:
        file.write(r.text)

import requests

def generar_cookies():
    s = requests.Session()
    response = s.get('https://www.youtube.com/')

    cookies = s.cookies
    with open('cookies.txt', 'w') as file:
        for cookie in cookies:
            file.write(f"{cookie.name}={cookie.value}\n")
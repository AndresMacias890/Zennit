import requests

def obtener_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return []



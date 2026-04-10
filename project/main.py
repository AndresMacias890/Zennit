from helper import obtener_post

post = obtener_post()

print("primeros 5 posts: ")

for post in post [:5]:
    print(f"ID:{post['id']} - Titulo:{post['title']}")
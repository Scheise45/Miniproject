import sys
import requests


def get_map_image(filename="map.png"):
    server_address = "https://static-maps.yandex.ru/1.x/?"
    ll_spn = "ll=0,0&spn=180,90&l=map"  # Полная карта мира

    map_request = f"{server_address}{ll_spn}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Сохраняем изображение
    with open(filename, "wb") as file:
        file.write(response.content)

    return filename  # Возвращаем имя файла с картой

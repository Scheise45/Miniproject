import sys
import requests


def get_map_image(lon=0, lat=0, spn=180, filename="map.png"):
    server_address = "https://static-maps.yandex.ru/1.x/?"

    ll_spn = f"ll={lon},{lat}&spn={spn},{spn/2}&l=map"
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

    return filename

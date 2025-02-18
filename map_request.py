import sys
import requests


def get_map_image(filename="map.png"):
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    ll_spn = 'll=37.530887,55.703118&spn=0.002,0.002'

    # Формируем запрос
    map_request = f"{server_address}{ll_spn}&apikey={api_key}"
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

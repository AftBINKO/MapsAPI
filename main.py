import response
import requests
import pygame
import sys
import os


def ll(x, y):
    return f"{x},{y}"


class Map:
    def __init__(self, ui, ll, t):
        self.lon, self.lat = ll
        self.t = t
        self.ui = ui
        print("Добро пожаловать в Яндекс.Карты")

    def start(self):
        response = self.load_map()
        self.show(response.content)

    def load_map(self):
        api_server = "http://static-maps.yandex.ru/1.x/"

        params = {
            "ll": ll(self.lon, self.lat),
            "l": self.t
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        return response

    def show(self, f):
        if self.ui == "PyGame":
            # Запишем полученное изображение в файл.
            try:
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(f)
            except IOError as error:
                print(f"Ошибка: {error.__class__.__name__}")
                sys.exit(2)

            # Инициализируем pygame
            pygame.init()
            screen = pygame.display.set_mode((600, 450))
            # Рисуем картинку, загружаемую из только что созданного файла.
            screen.blit(pygame.image.load(map_file), (0, 0))
            # Переключаем экран и ждем закрытия окна.
            pygame.display.flip()
            while pygame.event.wait().type != pygame.QUIT:
                pass
            pygame.quit()

            # Удаляем за собой файл с изображением.
            os.remove(map_file)
        else:
            print("Не готово, используй PyGame")


def main():
    ui = "PyGame"  # интерфейс, через который будет выводиться карта
    lon, lan = 50.606852, 55.364880  # широта и долгота
    t = "map"  # режим карты

    m = Map(ui, (lon, lan), t)
    m.start()


if __name__ == "__main__":
    main()

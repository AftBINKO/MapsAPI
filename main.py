import response
import requests
import pygame
import sys
import os


def ll(x, y):
    return f"{x},{y}"


class Map:
    def __init__(self, ui, ll, t, z, map_file="map.png"):
        self.lon, self.lat = ll
        self.t = t
        self.z = z
        self.ui = ui
        self.map_file = map_file
        print("Добро пожаловать в Яндекс.Карты")

    def start(self):
        response = self.load_map()
        self.create_map(response.content)
        self.show()

    def load_map(self):
        api_server = "http://static-maps.yandex.ru/1.x/"

        params = {
            "ll": ll(self.lon, self.lat),
            "l": self.t,
            "z": self.z
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        return response

    def create_map(self, f):
        # Запишем полученное изображение в файл.
        try:
            with open(self.map_file, "wb") as file:
                file.write(f)
        except IOError as error:
            print(f"Ошибка: {error.__class__.__name__}")
            sys.exit(2)

    def update(self):
        response = self.load_map()
        self.create_map(response.content)

    def show(self):
        if self.ui == "PyGame":
            # Инициализируем pygame
            pygame.init()
            screen = pygame.display.set_mode((600, 450))
            # Рисуем картинку, загружаемую из только что созданного файла.
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_PAGEUP and self.z <= 17:
                            self.z += 1
                            self.update()
                        elif event.key == pygame.K_PAGEDOWN and self.z > 1:
                            self.z -= 1
                            self.update()

                screen.blit(pygame.image.load(self.map_file), (0, 0))
                pygame.display.flip()

            pygame.quit()

            # Удаляем за собой файл с изображением.
            os.remove(self.map_file)
        else:
            print("Не готово, используй PyGame")


def main():
    ui = "PyGame"  # интерфейс, через который будет выводиться карта
    lon, lan = 50.606852, 55.364880  # широта и долгота
    t = "map"  # режим карты
    z = 17  # масштабирование

    m = Map(ui, (lon, lan), t, z)
    m.start()


if __name__ == "__main__":
    main()

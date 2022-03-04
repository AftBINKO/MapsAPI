import response
import requests
import pygame
import math
import sys
import os


def ll(x, y):
    return f"{x},{y}"


class Map:
    def __init__(self, ui, ll, t, z, fullscreen=False):
        self.lon, self.lat = ll
        self.t = t
        self.z = z
        self.ui = ui
        self.fullscreen = fullscreen

        self.lat_step = 0.002
        self.lon_step = 0.002
        self.coord_to_geo_x = 0.0000428
        self.coord_to_geo_y = 0.0000428

        self.map_file = "tmp.png"
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
        print(self.lon, self.lat)

    def show(self):
        if self.ui == "PyGame":
            # Инициализируем pygame
            pygame.init()
            if self.fullscreen:
                screen = pygame.display.set_mode((600, 450), pygame.FULLSCREEN)
            else:
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

                        elif event.key == pygame.K_LEFT and \
                                self.lon - self.lon_step * math.pow(2, 15 - self.z) > -180:
                            self.lon -= self.lon_step * math.pow(2, 15 - self.z)
                            self.update()
                        elif event.key == pygame.K_RIGHT and \
                                self.lon + self.lon_step * math.pow(2, 15 - self.z) < 180:
                            self.lon += self.lon_step * math.pow(2, 15 - self.z)
                            self.update()
                        elif event.key == pygame.K_UP and \
                                self.lat + self.lat_step * math.pow(2, 15 - self.z) < 85:
                            self.lat += self.lat_step * math.pow(2, 15 - self.z)
                            self.update()
                        elif event.key == pygame.K_DOWN and \
                                self.lat - self.lat_step * math.pow(2, 15 - self.z) > -85:
                            self.lat -= self.lat_step * math.pow(2, 15 - self.z)
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
    fullscreen = False  # вывод карты в полном экране

    m = Map(ui, (lon, lan), t, z, fullscreen=fullscreen)
    m.start()


if __name__ == "__main__":
    main()

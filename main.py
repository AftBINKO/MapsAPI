import pygame


def ll(x, y):
    return f"{x},{y}"

class Map:
    def __init__(sel):
        print("Добро пожаловать в Яндекс.Карты")

    def load_map(self):
        pass

    def show(ui, f):
        if ui == "PyGame":
            # Запишем полученное изображение в файл.
            try:
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
            except IOError as error:
                print("Ошибка")

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
    pass


if __name__ == "__main__":
    main()

class Dot:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x          # столбец
        self.y = y          # строка

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False

class Ship:
    nose = None
    size = None

    def __init__(self, size, nose, direction):
        self.size = size
        self.nose = nose
        self.direction = direction
        self.hp = size
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.size):
            if self.direction == 'H':       # horizontally
                dot_ship = Dot(self.nose.x + i, self.nose.y)
            else:
                dot_ship = Dot(self.nose.x, self.nose.y + i)
            ship_dots.append(dot_ship)
        return ship_dots

class Board():
    def __init__(self, state_cells, list_ships, hid, num_sur):
        self.state_cells = [['0'] * 6 for i in range(6)]   # список с состоянием каждой клетки
        self.list_ships = []                               # список кораблей
        self.hid = hid                                     # типа bool, нужно скрывать доску(для врага) или нет(для себя)
        self.num_sur = num_sur                             # количество живых кораблей

    @staticmethod
    def add_ships(self):
        for dot in Ship.dots():


    @staticmethod
    def contour(self):
        contour_ship = []
        if self.direction == 'H':
            for i in range(-1, Ship.size):
                for j in range(-1, 1, 2):
                    contour_dot = Dot(Ship.nose.x + i, Ship.nose.y + j)
                    contour_ship.append(contour_dot)
            for i in range(Ship.size):
                dot_ship = Dot(Ship.nose.x + i, Ship.nose.y)
                contour_ship.remove(dot_ship)
            return contour_ship
        else:
            for i in range(-1, 1, 2):
                for j in range(-1, Ship.size):
                    contour_dot = Dot(Ship.nose.x + i, Ship.nose.y + j)
                    contour_ship.append(contour_dot)
            for i in range(Ship.size):
                dot_ship = Dot(Ship.nose.x, Ship.nose.y + i)
                contour_ship.remove(dot_ship)
            return contour_ship

    @staticmethod
    def out():
        if Dot.x < 1 or Dot.y < 1 or Dot.x > 6 or Dot.y > 6:
            return True
        return False

    @staticmethod
    def player_shot(self):
        try:
            shot = Dot(x = int(input('Введите координату X выстрела:')), y = int(input('Введите координату Y выстрела:')))
            if shot == '■':
                shot = 'X'
            else:
                shot = 'T'
        except IndexError:
            print('Вы выстрелили за пределы доски!')




    def print_board(self):
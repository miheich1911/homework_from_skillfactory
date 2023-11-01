class Dot:
    def __init__(self, x, y):
        self.x = x          # столбец
        self.y = y          # строка

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False

class Ship:
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
    def __init__(self, hid, field, list_ships, num_sur):
        self.hid = hid
        self.field = field
        self.list_ships = list_ships
        self.num_sur = num_sur


    def add_ship(self, dot, ship):
        self.field = [['0'] * 6 for i in range(6)]
        self.list_ships = []
        self.num_sur = 0
        occupied_points = []
        for dot in ship.dots():
            if self.out(dot) or dot in occupied_points:
                raise Exception("Невозможно поставить корабль на это место")
            else:
                continue
        self.field[dot.x - 1][dot.y - 1] = '■'
        occupied_points.append(dot)
        occupied_points.append(self.contour(ship))
        self.list_ships.append(ship)
        self.num_sur += 1
        return self.list_ships, self.num_sur, self.field

    def contour(self, ship):
        contour_ship = []
        for dot in ship.dots():
            for i in range(-1, 1):
                for j in range(-1, 1):
                    contour_dot = Dot(dot.x + i, dot.y + j)
                    if self.out(contour_dot) or contour_dot in ship.dots():
                        continue
                    else:
                        contour_ship.append(contour_dot)
        return contour_ship

    def out(self, dot):
        if dot.x < 1 or dot.y < 1 or dot.x > 6 or dot.y > 6:
            return True
        return False

    def shot(self, dot):
        try:
            shot_dot = dot(x = int(input('Введите координату X выстрела:')), y = int(input('Введите координату Y выстрела:')))
            if shot_dot == '■':
                shot_dot = 'X'
            else:
                shot_dot = 'T'
        except IndexError:
            print('Вы выстрелили за пределы доски!')

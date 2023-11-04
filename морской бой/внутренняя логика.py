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
    def __init__(self, hid):
        self.hid = hid
        self.field = [['0'] * 6 for i in range(6)]
        self.list_ships = []
        self.num_sur = 0
        self.occupied_points = []

    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out(dot) or dot in self.occupied_points:
                raise Exception("Невозможно поставить корабль на это место!")
        for dot in ship.dots():
            self.field[dot.x - 1][dot.y - 1] = '■'
        self.occupied_points.append(ship.dots())
        self.occupied_points.append(self.contour(ship))
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

    def shot(self, dot, ship):
        shot_dot = dot(int(input('Введите номер строки для выстрела:')), int(input('Введите номер колонны для выстрела:')))
        try:
            if shot_dot == '■':
                shot_dot = 'X'
                print('Попал!')
                ship.hp -= 1
            else:
                shot_dot = 'T'
                print('Мимо!')
            if ship.hp == 0:
                for dot in ship.contour():
                    dot = 'T'
                print('Убит!')
        except IndexError:
            print('Вы выстрелили за пределы доски!')


    def print_board(self):
        print(" |1|2|3|4|5|6")
        for i, row in enumerate(self.field, start=1):
            print(i, *row, sep='|')




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
        self.hid = hid                                # типа bool, нужно скрывать доску(для врага) или нет(для себя)

    # def add_ships(self, ship):
    #     list_ships = []                               # список кораблей
    #     num_sur = 0                                   # количество живых кораблей
    #     for dot in ship.dots():
    #         if dot.out() is True or dot in ship.contour() or dot in ship.dots():
    #             raise Exception("Невозможно поставить корабль на это место")
    #         else:
    #             continue
    #     list_ships.append(ship)
    #     num_sur += 1
    #     return list_ships



    def add_ship(self, field, ship, list_ships):
        field = [['0'] * 6 for i in range(6)]
        list_ships = []                               # список кораблей
        num_sur = 0                                   # количество живых кораблей
        for dot in ship.dots():
            # если точка за пределами поля, или попадает в контур другого корабля, или совпадает с точкой другого корабля
            if self.out(dot) or dot in self.contour(Ship) or dot in Ship.dots:
                raise Exception("Невозможно поставить корабль на это место")
            else:
                ship.append(dot)
        list_ships.append(ship)
        field.append(list_ships)
        num_sur += 1
        return field

    
    def contour(self, ship):
        contour_ship = []
        for dot in ship.dots():
            for i in range(-1, 1):
                for j in range(-1, 1):
                    contour_dot = dot(x + i, y + j)
                    if contour_dot.out() is True or contour_dot in ship.dots():
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


    def print_board(self):

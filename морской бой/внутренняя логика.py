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
        for dot in ship.dots:
            if self.out(dot) or dot in self.occupied_points:
                raise Exception("Невозможно поставить корабль на это место!")
        for dot in ship.dots:
            self.field[dot.x - 1][dot.y - 1] = '■'
        self.occupied_points.append(ship.dots)
        self.occupied_points.append(self.contour(ship))
        self.list_ships.append(ship)
        self.num_sur += 1
        return self.list_ships, self.num_sur, self.field

    def contour(self, ship):
        contour_ship = []
        for dot in ship.dots:
            for i in range(-1, 1):
                for j in range(-1, 1):
                    contour_dot = Dot(dot.x + i, dot.y + j)
                    if self.out(contour_dot) or contour_dot in ship.dots:
                        continue
                    else:
                        contour_ship.append(contour_dot)
        return contour_ship

    def out(self, dot):
        if dot.x < 1 or dot.y < 1 or dot.x > 6 or dot.y > 6:
            return True
        return False

    def shot(self, dot):
        perfect_shots = []
        if dot in perfect_shots:     #если выстрел В СПИСКЕ произведенных выстрелов
            raise Exception("Вы уже стреляли в эту клетку! Введите корректные данные для выстрела!")
        else:     #если выстрел НЕ В СПИСКЕ произведенных выстрелов
            for ship in self.list_ships:     #для корябля из списка кораблей
                if dot in ship.dots:     #если выстрел ПОПАДАЕТ в одну из точек корабля
                    self.field[dot.x - 1][dot.y - 1] = 'X'     #точка помечается знаком 'X'
                    ship.hp -= 1     #жизнь корабля уменьшается на 1
                    perfect_shots.append(dot)     #выстрел записывается в список произведенных выстрелов\
                    print('Попал! Сделайте еще один выстрел')
                    if ship.hp == 0:     #если корабль погибает
                        for dot in self.contour(ship):     # для точек контура корабля
                            self.field[dot.x - 1][dot.y - 1] = 'T'      #точки помечаются знаком 'T'
                            self.num_sur -= 1     #счетчик живых кораблей уменьшается на 1
                            self.list_ships.remove(ship)     #корабль удалаяется из списка кораблей
                            perfect_shots.append(dot)     #точки контура добавляются в список не разрешенных для выстрела клеток. то есть в список произведенных выстрелов, чтобы игрок по ним уже не мог стрелять
                            print('Корабль потоплен!') 
                    return perfect_shots
                else:    #если выстрел НЕ ПОПАДАЕТ в одну из точек корабля
                    if dot in self.out(dot):    #если выстрел ВЫШЕЛ за пределы поля
                        raise Exception("Введите корректные данные для выстрела!")
                    else:    #если выстрел НЕ ВЫШЕЛ за пределы поля (но он не попал в корабль, то есть промах)
                        self.field[dot.x - 1][dot.y - 1] = 'T'    #точка помечается знаком 'X'
                        perfect_shots.append(dot)
                        print('Промах!')
                    return perfect_shots

    def print_board(self):
        print(" |1|2|3|4|5|6")
        for i, row in enumerate(self.field, start=1):
            print(i, *row, sep='|')

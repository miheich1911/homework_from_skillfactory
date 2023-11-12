import random
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
            if self.direction == 0:       # horizontally
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
        self.occupied_points.extend(self.contour(ship))
        self.list_ships.append(ship)
        self.num_sur += 1
        return self.list_ships, self.num_sur, self.field

    def contour(self, ship):
        contour_ship = []
        for dot in ship.dots:
            for i in range(-1, 2):
                for j in range(-1, 2):
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
        if self.out(dot) or self.field[dot.x - 1][dot.y - 1] == 'X' or self.field[dot.x - 1][dot.y - 1] == 'T':
            raise Exception("Введите корректные данные для выстрела!")
        else:
            for ship in self.list_ships:  # для корябля из списка кораблей
                if dot in ship.dots:
                    self.field[dot.x - 1][dot.y - 1] = 'X'
                    ship.hp -= 1
                    print('Попал! Сделайте еще один выстрел')
                    if ship.hp == 0:  # если корабль погибает
                        for dot in self.contour(ship):
                            self.field[dot.x - 1][dot.y - 1] = 'T'
                        self.num_sur -= 1
                        self.list_ships.remove(ship)
                        print('Корабль потоплен!')
            else:
                if self.field[dot.x - 1][dot.y - 1] == '0':
                    self.field[dot.x - 1][dot.y - 1] = 'T'
                    print('Промах!')
                    return False

    def print_board(self):
        print(" |1|2|3|4|5|6")
        for i, row in enumerate(self.field, start=1):
            print(i, *row, sep='|')


class Player:
    def __init__(self, own, enemy_board):
        self.own = own
        self.enemy_board = enemy_board



    def ask(self):
        pass

    def move(self):
        try:
            self.enemy_board.shot(self.ask())
            self.enemy_board.print_board()
            if self.enemy_board.shot(self.ask()) is False:
                return False
            else:
                return True
        except Exception as ex:
            print(ex)
            return True



class User(Player):
    def ask(self):
        print(f'Ход игрока {self.name()}')
        x = int(input('Введите номер строки:'))
        y = int(input('Введите номер столбца:'))
        dot = Dot(x, y)
        return dot

    def name(self):
        return 'Пользователь'



class AI(Player):
    def ask(self):
        print(f'Ход игрока {self.name()}')
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        dot = Dot(x, y)
        return dot

    def name(self):
        return 'Компьютер'



class Game:
    def __init__(self):
        self.user_board = self.random_board(False)
        self.ai_board = self.random_board(True)
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def greet(self):
        print('Добро пожаловать в игру морской бой 6х6!')

    def loop(self):
        count = 0
        if count % 2 == 0:
            self.user.move()
            if self.user.move() is False:
                count += 1
                if self.ai_board.list_ships == 0:
                    print("Вы победили!")
            else:
                return
        else:
            self.ai.move()
            if self.ai.move() is False:
                count += 1
                if self.user_board.list_ships == 0:
                    print("Компьютер победил!")
            else:
                return




    def random_board(self, hid):
        board = Board(hid)
        size = [3, 2, 2, 1, 1, 1, 1]
        count = 0
        for i in size:
            while True:
                try:
                    x = random.randint(1, 6)
                    y = random.randint(1, 6)
                    direction = random.randint(0, 1)     #горизонтальное и вертикальное
                    ship = Ship(i, Dot(x, y), direction)
                    board.add_ship(ship)
                    count += 1
                    continue
                except Exception:
                    pass
            if count > 1000:
                raise Exception('превышено допустимое количество попыток')
        return board


    def start(self):
        self.greet()
        print('Ваша доска!')
        self.user_board.print_board()
        self.loop()
        print('Игра окончена!')


game = Game()
game.start()







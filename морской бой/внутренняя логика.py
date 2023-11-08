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

    def name(self):
        pass

    def ask(self, dot):
        print(f'Ход игрока {self.name()}')
        pass

    def move(self, dot):
        dot = self.ask(dot)
        try:
            shot = self.enemy_board.shot(dot)
            self.enemy_board.print_board()
            return shot
        except Exception as ex:
            print(ex)
            return True



class User(Player):
    def ask(self, dot):
        dot = Dot(int(input('Введите номер строки:')), int(input('Введите номер столбца:')))
        return dot

    def name(self):
        return 'Пользователь'



class AI(Player):
    def ask(self, dot):
        dot = Dot(random.randint(1, 6), random.randint(1, 6))
        return dot

    def name(self):
        return 'Компьютер'



class Game:
    def __init__(self):
        user_board = self.random_board()
        ai_board = self.random_board()
        self.user_board = user_board
        self.ai_board = ai_board
        self.user = User(user_board, ai_board)
        self.ai = AI(ai_board, user_board)



    def greet(self):
        print('Добро пожаловать в игру морской бой 6х6!')

    def loop(self):
        while True:
            if self.user_board.list_ships == 0:
                print('Поражение:( Компьютер победил:(')
                return
            if not self.ai.move():
                break
        while True:
            if self.ai_board.list_ships == 0:
                print('Поздравляем! Вы победили!:)')
                return
            if not self.user.move():
                break


    def random_board(self):
        board = Board(False)
        size = [3, 2, 2, 1, 1, 1, 1]
        count = 0
        if count < 1000:
            for i in size:
                x = random.randint(1, 6)
                y = random.randint(1, 6)
                direction = random.choice(['H', 'V'])     #горизонтальное и вертикальное
                ship = Ship(i, Dot(x, y), direction)
                try:
                    board.add_ship(ship)
                except:
                    print("Невозможно поставить корабль на это место!")
                    count += 1
                    continue
        return board


    def start(self):
        self.greet()
        print('Ваша доска!')
        self.user_board.print_board()
        self.loop()
        print('Игра окончена!')

if __name__ == '__main__':
    game = Game()
    game.start()







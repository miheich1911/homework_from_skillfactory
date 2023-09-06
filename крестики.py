field = list(range(1,10))

def draw_field(field):
    print("-" * 13)
    for i in range(3):
        print(f'| {field[0 + i*3]} | {field[1 + i*3]} | {field[2 + i*3]} |')
        print("-" * 13)

def make_move(mark):
    valid = False
    while not valid:
        player_answer = int(input(f'Куда поставим {mark}?'))
        if player_answer >= 1 and player_answer <=9:
            if (str(field[player_answer - 1]) not in 'X0'):
                field[player_answer - 1] = mark
                valid = True
            else:
                print('Эта клетка занята. Выберите другую клетку.')
        else:
            print('Неправильный ввод. Введите число от 1 до 9.')

def winning_condition(field):
    check_win = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for variable in check_win:
        if field[variable[0]] == field[variable[1]] == field[variable[2]]:
            return field[variable[0]]
    return False

def play_game(field):
    counter = 0
    win = False
    while not win:
        draw_field(field)
        if counter % 2 == 0:
            make_move('X')
        else:
            make_move('0')
        counter += 1
        if counter > 4:
            qwerty = winning_condition(field)
            if qwerty:
                draw_field(field)
                print(qwerty, 'выиграл')
                win = True
                break
        if counter == 9:
            draw_field(field)
            print('Ничья')
            break
play_game(field)

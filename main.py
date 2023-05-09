# build 2048 in python using pygame!!
import pygame
import random

pygame.init()

# initial set up
ligne = int(input("Nombre de ligne que vous souhaitez : "))
colone = int(input("Nombre de colone que vous souhaitez : "))
nbToWin = int(input("Entrez le nombre qui une fois atteint arretera la partie (Mettre 0 pour ne pas avoir de limite) : "))
WIDTH = 1400
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
diffL = ligne - 4
diffC = colone - 4 
board_values = [[0 for _ in range(4+diffL)] for _ in range(4+diffC)]
board_test = [[0 for _ in range(4+diffL)] for _ in range(4+diffC)]
game_over = False
spawn_new = True
sonLancer = False
sonLancerRecord = False
newRecordSon = pygame.mixer.Sound("leSonRecord.ogg")
sonTryhard = pygame.mixer.Sound("leSon.ogg")
sonChill = pygame.mixer.Sound("leSonChill.ogg")
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high


# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [850, 50, 450, 100], 0, 10)
    game_over_text1 = font.render('Perdu!', True, 'white')
    game_over_text2 = font.render('Appuyer sur Entrer pour Redémarrer', True, 'white')
    screen.blit(game_over_text1, (1030, 65))
    screen.blit(game_over_text2, (860, 105))

def draw_win():
    pygame.draw.rect(screen, 'black', [850, 50, 450, 100], 0, 10)
    game_over_text1 = font.render('Gagner!', True, 'white')
    game_over_text2 = font.render('Appuyer sur Entrer pour Redémarrer', True, 'white')
    screen.blit(game_over_text1, (1030, 65))
    screen.blit(game_over_text2, (860, 105))

# take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4 + diffL)] for _ in range(4 + diffC)]
    if direc == 'UP':
        for i in range(4 + diffC):
            for j in range(4 + diffL):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1 ][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1 ][j]:
                        board[i - shift - 1 ][j] *= 2
                        score += board[i - shift - 1 ][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3 + diffC):
            for j in range(4 + diffL):
                shift = 0
                for q in range(i + 1):
                    if board[3 + diffC - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 + diffC - i + shift][j] = board[2 + diffC- i][j]
                    board[2 + diffC - i][j] = 0
                if 3 + diffC - i + shift <= 3 + diffC:
                    if board[2 + diffC - i + shift][j] == board[3 + diffC - i + shift][j] and not merged[3 + diffC - i + shift][j] \
                            and not merged[2 + diffC - i + shift][j]:
                        board[3 + diffC - i + shift][j] *= 2
                        score += board[3 + diffC - i + shift][j]
                        board[2 + diffC - i + shift][j] = 0
                        merged[3 + diffC - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4 + diffC):
            for j in range(4 + diffL):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift] and not j - shift == 0 :
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4 + diffC):
            for j in range(4 + diffL):
                shift = 0
                for q in range(j):
                    if board[i][3 + diffL - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 + diffL - j + shift] = board[i][3 + diffL - j]
                    board[i][3 + diffL - j] = 0
                if 4 + diffL - j + shift <= 3 + diffL:
                    if board[i][4 + diffL - j + shift] == board[i][3 + diffL - j + shift] and not merged[i][4 + diffL - j + shift] \
                            and not merged[i][3 + diffL - j + shift]:
                        board[i][4 + diffL - j + shift] *= 2
                        score += board[i][4 + diffL - j + shift]
                        board[i][3 + diffL - j + shift] = 0
                        merged[i][4 + diffL - j + shift] = True
    return board

# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3 + diffC)
        col = random.randint(0, 3 + diffL)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 1600, 700], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'Meilleur Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 710))
    screen.blit(high_score_text, (10, 750))
    pass


# draw tiles for game
def draw_pieces(board):
    for i in range(4 + diffC):
        for j in range(4 + diffL):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

# check des possibilité de mouvement pour savoir si la partie est finit
def test_gameOver(board):

    merged = [[False for _ in range(4 + diffL)] for _ in range(4 + diffC)]
    
    for i in range(3 + diffC): #Check si faisable de deplacer vers le bas 
        for j in range(4 + diffL):
            shift = 0
            for q in range(i + 1):
                if board[3 + diffC - q][j] == 0:
                    shift += 1
            if shift > 0:
                board[2 + diffC - i + shift][j] = board[2 + diffC- i][j]
                board[2 + diffC - i][j] = 0
            if 3 + diffC - i + shift <= 3 + diffC:
                if board[2 + diffC - i + shift][j] == board[3 + diffC - i + shift][j] and not merged[3 + diffC - i + shift][j] \
                        and not merged[2 + diffC - i + shift][j]:
                        return False

    for i in range(4 + diffC): #Check si faisable de deplacer vers le droite 
        for j in range(4 + diffL):
            shift = 0
            for q in range(j):
                if board[i][3 + diffL - q] == 0:
                    shift += 1
            if shift > 0:
                board[i][3 + diffL - j + shift] = board[i][3 + diffL - j]
                board[i][3 + diffL - j] = 0
            if 4 + diffL - j + shift <= 3 + diffL:
                if board[i][4 + diffL - j + shift] == board[i][3 + diffL - j + shift] and not merged[i][4 + diffL - j + shift] \
                        and not merged[i][3 + diffL - j + shift]:
                        return False
    return True                    

def win_game(board):
    for i in range(4 + diffC):
        for j in range(4 + diffL):
            value = board[i][j]
            if value >= nbToWin and not nbToWin == 0:
                return True
    return False

# main game loop
run = True


while run:

    if sonLancer == False:
        if nbToWin == 0 : 
            sonChill.play(loops=1)
            sonLancer = True
        else :
            sonTryhard.play(loops=1)
            sonLancer = True

    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if win_game(board_values) == True :
        draw_win()
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        board_test = board_values
        if test_gameOver(board_test) == True :
            draw_over()
            if high_score > init_high:
                file = open('high_score', 'w')
                file.write(f'{high_score}')
                file.close()
                init_high = high_score

        elif test_gameOver(board_test) == False :
            game_over = False
            board_test = board_values
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and win_game(board_values) == False:
                direction = 'UP'
            elif event.key == pygame.K_DOWN and win_game(board_values) == False:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and win_game(board_values) == False:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and win_game(board_values) == False:
                direction = 'RIGHT'

            if game_over:

                if high_score >= init_high and sonLancerRecord == False:
                    sonChill.stop()
                    sonTryhard.stop()
                    newRecordSon.play(loops=1)
                    sonLancerRecord = True

                if event.key == pygame.K_RETURN and win_game(board_values) == False:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    sonChill.stop()
                    sonTryhard.stop()
                    newRecordSon.stop()
                    init_count = 0
                    score = 0
                    direction = ''
                    sonLancer = False
                    game_over = False
                    sonLancerRecord = False



            if win_game(board_values) == True: 
                if high_score >= init_high and sonLancerRecord == False:
                    sonChill.stop()
                    sonTryhard.stop()
                    newRecordSon.play(loops=1)
                    sonLancerRecord = True

                if event.key == pygame.K_RETURN :
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    sonChill.stop()
                    sonTryhard.stop()
                    newRecordSon.stop()
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False
                    sonLancer = False
                    sonLancerRecord = False


    if score > high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()

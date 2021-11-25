import pygame
import sys
import random
import winsound
pygame.init()
clock = pygame.time.Clock()


#색 설정
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)


#스크린 크기 설정
size   = [800, 500]
screen = pygame.display.set_mode(size)

#스크린 이름 설정
pygame.display.set_caption("Hangman")


game_over = False


#image 파일
IMAGES = []      
hangman_status = 0      #행맨 image 초기값 설정

for i in range(8):
    image = pygame.image.load(f'images\hangman{i}.jpg')             #for문과 f-string을 이용해 행맨 이미지를 0~7까지 순서대로 load
    IMAGES.append(image)                                            #IMAGES 리스트에 추가

#Buttons
ROWS = 2    #행
COLS = 13   #열  #알파벳 26개니까~
GAP = 20
SIZE = 40
BOXES = []

for row in range(ROWS):
    for col in range(COLS):
        x = ((GAP * col) + GAP) + (SIZE * col)
        y = ((GAP * row) + GAP) + (SIZE * row) + 330
        box = pygame.Rect(x,y,SIZE,SIZE)                            #pygame으로 (x, y) 점에서 가로세로 SIZE = 40크기 사각형 그려줌
        BOXES.append(box)                                           #BOXES 리스트에 계속 추가

BUTTONS = []
A = 65                                                              #파이썬 내장함수. 아스키코드에서 A=65로 시작, Z=132임. 그 뒤는 소문자 좌라락,,,,,,

for index, box in enumerate(BOXES):                                 #for (인덱스값, 변수) in enumerate(순서있는자료형):
    letter = chr(A+index)                                           #무슨말이냐면 단순히 변수값만 불러오는게 아니라 (인덱스값, 변수값)으로 짝지어 불러옴. 여기서는 BOXES리스트에 있는 box에다 index 짝으로 불러옴
    button = [box, letter]                                          #순서가 있는 자료형(리스트!!, 문자열, 튜플)을 입력으로 받아 인덱스 값을 포함하는 enumerate 객체를 리턴
    BUTTONS.append(button)                                          #chr(A) 하면 chr(65)니까 letter = A 되겠지? 인덱스값은 첫번째 변수니까 0. index는 0부터 1234계속 증가할거니까 65+0, 65+1, 65+2 이렇게 들어가고 A,B,C 주루룩 순서대로 나오게됨

#Fonts
button_font = pygame.font.Font('Maplestory_Bold.ttf', 30)
game_font = pygame.font.Font('Maplestory_Bold.ttf', 60)
letter_font = pygame.font.Font('Maplestory_Bold.ttf', 50)
start_font = pygame.font.Font('Maplestory_Bold.ttf', 50)

#Word
with open ("textfile.txt") as myfile:
    file = myfile.read()
words = file.split(",")
WORD = random.choice(words)
print(WORD)
print(words)

#시작화면
def start_screen():
    screen.fill(BLACK)
    start_text = start_font.render("Let's start Hangman game !!", True, WHITE)
    start_text_rect = start_text.get_rect(center=(800//2, 240))
    screen.blit(start_text, start_text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)


#Button 만들기
def draw_buttons(BUTTONS):
    for box, letter in BUTTONS:
            button_text = button_font.render(letter, True, BLACK)
            button_rect = button_text.get_rect(center = (box.x +20, box.y + 20))    #box의 x, y좌표에 20만큼 더한 위치에 letter 표
            screen.blit(button_text, button_rect)                                   #왼쪽(button_text)을 오른쪽(위치)에 표시
            pygame.draw.rect(screen, BLACK, box, 3)                                 #pygame.draw.rect(화면 지정 변수명,(R,G,B),pg.Rect(그릴x축,그릴y축,폭, 높이), 테두리 굵기)


#추측하는 WORD screen에 표시
def display_guess():
    display_text = ''                                                               #display_text 변수 선언
    for letter in WORD:
        if letter in GUESSED:
            display_text += f"{letter} "                                       # += : add AND (계속 더해서 늘어남)   #f-string : f'문자열 {변수} 문자열'
        else:
            display_text += "_ "
    #for문 이용해 display_text에 letter랑 _를 경우에 맞추어 연이어 +=로 대입한 것//처음에 GUESSED 리스트는 비어있으니 else만 실행. 우리가 글자를 맞추면 GUESSED 리스트에 append되므로 if 성립, 글자표시됨.
    text = letter_font.render(display_text, True, BLACK)                            #pygame.font.render(텍스트, antialias여부, 텍스트 색 지정, 텍스트 배경색 지정)
    screen.blit(text, (400, 200))                                                   #screen.blit(text를, 원하는 좌표에 나타냄)





start_screen()

#Screen에 보여지는 Title
title = "Hangman"
title_text = game_font.render(title, True, BLACK)
title_rect = title_text.get_rect(center=(800//2, 50))               #get_rect에는 좌표값이 아닌 변수,,그런게 들어가야함.
                                                                    #근데 center는 이전에 정의되어있지 않으니 좌표를 바로 정의해주는것.

GUESSED = []

# 핵심
while True:                                                         #while True같은 이벤트루프가 있어야 창이 닫히지 않음.
    for event in pygame.event.get():                                #pygame 이용해 event 받음. 우측상단 X 누르면 종료. 그냥 멈춤.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()                                              #강제로 스크립트 종료 (sys 모듈 이용)

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_pos = event.pos                                 #pos()는 좌표값을 반환해주는 함수. 근데 .은 왜찍은거지 저렇게하면 뭐 의미가 있나

            for button, letter in BUTTONS:
                if button.collidepoint(clicked_pos):                #클릭이 button과 충돌했는지 확인
                    GUESSED.append(letter)                          #GUESSED 리스트에 letter 추가
                    if letter not in WORD:                          #만약 WORD에 클릭한 letter없으면
                        hangman_status += 1                         #행맨사진 다음장
                        if hangman_status == 7:                     #만약 행맨사진 마지막순서 되면 게임오버
                            game_over = True                        #game_over = False였는데 True로 바꿔줌
                        
                    BUTTONS.remove([button, letter])                #BUTTONS에서 [button, letter]를 제거함.
            
    screen.fill(WHITE)
    screen.blit(IMAGES[hangman_status], (100, -50))
    screen.blit(title_text, title_rect)
    draw_buttons(BUTTONS)
    display_guess()

    win = True                                                      #상태설정 : win이라는 변수를 이따 쓸건데~ 논리값(참/거짓)이야~

    for letter in WORD:                             #WORD에 있는걸 '한글자씩' 가져와서 넣어주는 것  for ?? in WORD
        if letter not in GUESSED:
            win = False

    #game_over_message 설정
    if win:
        game_over = True
        game_over_message = "You won !!"
    else:
        game_over_message = "You lost !!"
        
    pygame.display.flip()       #pygame.display.update() 해도 똑같
    clock.tick(50)

    #game_over_sound 설정
    if win:
        game_over = True
        game_over_sound = 'correct_sound'
    else:
        game_over_sound = 'wrong_sound'

    #게임 오버 시
    if game_over:
        screen.fill(WHITE)
        text = game_font.render(game_over_message, True, BLACK)
        text_rect = text.get_rect(center=(800//2, 240))
        screen.blit(text, text_rect)
        pygame.display.flip()
        winsound.PlaySound(game_over_sound, winsound.SND_ALIAS)     #SND_ALIAS = 저장소에 있는 이름의 소리 가져와 재생
        pygame.time.delay(3000)     #3초 있다 꺼짐.
        pygame.quit()
        sys.exit()
        

    pygame.display.flip()

pygame.quit()

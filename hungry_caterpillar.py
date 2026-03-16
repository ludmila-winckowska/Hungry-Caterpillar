import pygame #библиотека
import random #что бы появляось в разных местах
import math

pygame.init()

font = pygame.font.SysFont(None, 30) #шрифт

#скорость гусеницы
clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 540))
pygame.display.set_caption("Hungry Caterpillar")
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("images/background.png").convert()
background = pygame.transform.scale(background, (500, 540))

#клубника
strawberries = pygame.image.load("images/strawberries.png").convert_alpha()
strawberries = pygame.transform.scale(strawberries,(50,50))

#гриб
mushroom = pygame.image.load("images/mushroom.png").convert_alpha()
mushroom = pygame.transform.scale(mushroom,(50,50))
#координаты гриба
mush_x = random.randint(0,9)
mush_y = random.randint(0,9)

#ежевика
blackberry = pygame.image.load("images/blackberry.png").convert_alpha()
blackberry = pygame.transform.scale(blackberry,(50,50))

#виноград
grapes = pygame.image.load("images/grapes.png").convert_alpha()
grapes = pygame.transform.scale(grapes,(50,50))

#черешня
cherry = pygame.image.load("images/cherry.png").convert_alpha()
cherry = pygame.transform.scale(cherry,(50,50))

#черника
blueberry = pygame.image.load("images/blueberry.png").convert_alpha()
blueberry = pygame.transform.scale(blueberry,(50,50))

#пчела
bee = pygame.image.load("images/bee.png").convert_alpha()
bee = pygame.transform.scale(bee,(50,50))

#роза
rose = pygame.image.load("images/rose.png").convert_alpha()
rose = pygame.transform.scale(rose,(50,50))

#кристал
crystal = pygame.image.load("images/crystal.png").convert_alpha()
crystal = pygame.transform.scale(crystal,(50,50))

#жаба
frog = pygame.image.load("images/frog.png").convert_alpha()
frog = pygame.transform.scale(frog,(50,50))

#гусеница
head_img = pygame.image.load("images/caterpillar_head.png").convert_alpha()
body_img = pygame.image.load("images/caterpillar_body.png").convert_alpha()
tail_img = pygame.image.load("images/caterpillar_tail.png").convert_alpha()

head_img = pygame.transform.scale(head_img,(50,50))
body_img = pygame.transform.scale(body_img,(50,50))
tail_img = pygame.transform.scale(tail_img,(50,50))

#чтобы обьекты сами попадали в сетку
cell_size= 50

#гусеница

caterpillar = [(5,5), (4,5), (3,5)] #тело
direction = (1, 0) #движение
move_delay = 200 #0,2 секунды движение гусеницы
last_move = 0

grid_x = random.randint(0, 9)
grid_y = random.randint(0, 9)
print(grid_x, grid_y)

sx = grid_x * cell_size
sy = grid_y * cell_size + 40

#переменные игры
score = 0
lives = 3
level = 1
invincible_until = 0#переменная для мигания гусеницы при столкновении в себя
level = 1 #уровни

#светлячкииииии
# --- FIREFLIES ---
fireflies = []

#создание больших светлячков
for _ in range(7):
    gx = random.randint(0, 9) #клетка по х
    gy = random.randint(0, 9) #кетка по у
    x = gx * cell_size + cell_size//2
    y = gy * cell_size + cell_size//2
    fireflies.append({"x": x, "y": y, "r": 3, "phase": random.randint(0,1000),
"jitter": 1.5, "vx": random.uniform(-0.05,0.05), "vy": random.uniform(-0.05,0.05)})
    
#создание маленьких светлячков
for _ in range(7):
    gx = random.randint(0,9)
    gy = random.randint(0,9)
    x = gx * cell_size + cell_size//2
    y = gy * cell_size + cell_size//2
    fireflies.append({"x": x, "y": y, "r": 1.5, "phase": random.randint(0,1000),
"jitter": 1.5,"vx": random.uniform(-0.05,0.05), "vy": random.uniform(-0.05,0.05)})

    

print("fireflies:", len(fireflies))

#Game Over
game_over_img = pygame.image.load("images/game_over.png").convert()
game_over_img = pygame.transform.scale(game_over_img,(356,540))#размер настоящей
#картинки 1024/1536=0.66, 540*0.66=356

#функция картинку game over
def game_over_screen():
    sound_start.play()#музыка для заставки play
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover = 170 < mouse_x <330 and 440 <mouse_y < 510
        screen.fill((0,0,0))
        screen.blit(game_over_img,(72,0))#чтобы была картинка гейм овер поцентру
        if hover:
            glow = pygame.Surface((140,45),pygame.SRCALPHA)#свечение кнопки
            glow.fill((255,255,255,35))
            screen.blit(glow,(180,467))
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                #координаты кнопки
                if 170 < mouse_x <330 and 440 < mouse_y <510:
                    reset_game()
                    sound_click.play()#звук клик
                    sound_start.stop()#чтобы музыка остановилась
                    return
                
#сброс игры после game over и нажатия кнопки try again
def reset_game():
    global caterpillar, direction, score, lives, level
    global grid_x, grid_y, mush_x, mush_y, last_move
    caterpillar = [(5,5),(4,5),(3,5)]#голова+тело+хвост
    direction = (1,0)
    score = 0
    level = 1
    lives = 3
    grid_x = random.randint(0,9)
    grid_y = random.randint(0,9)
    mush_x = random.randint(0,9)
    mush_y = random.randint(0,9)
    last_move = pygame.time.get_ticks()

#это код который делает всегда любую картинку нужного размера
def scale_to_fit(img, max_w, max_h):
    w, h = img.get_size()
    scale = min(max_w / w, max_h / h)
    new_size = (int(w * scale), int(h * scale))
    return pygame.transform.scale(img,new_size)

#заставка игры с кнопкой play
cover_img = pygame.image.load("images/cover.png").convert()
cover_img = scale_to_fit(cover_img, 500, 540)

#добавляю функцию, чтобы заставка не исчезала, а была до нажатия play
def show_cover():
    sound_start.play()#музыка для заставки play
    while True:
        x = (500 - cover_img.get_width()) //2
        y = (540 - cover_img.get_height()) // 2
        screen.blit(cover_img, (x, y))
        #свечение кнопки play
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover = 198 < mouse_x < 300 and 338 < mouse_y <367
        if hover:
            for i in range(3):
                glow = pygame.Surface((102 + i*3, 29 + i*3), pygame.SRCALPHA)
                glow.fill((255,160,255,40))
                screen.blit(glow, (198 - i*1, 338 - i*1))
        #курсор в виде пальчика
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover = 198 < mouse_x < 300 and 338 < mouse_y <367
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
        pygame.display.update()#обновляет экран
                               #(показывает всё что мы нарисовали)
        
        for event in pygame.event.get():#проверяем события(обработка событий)
                                        #(клик мыши,клавиши,закрытие окна)
            if event.type == pygame.QUIT:#если нажали крестик закрытия окна
                pygame.quit()#закрыть pygame
                exit()#полностью завершить программу
                
            if event.type == pygame.MOUSEBUTTONDOWN:#чтобы кнопка play нажималась
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                if 198 < mouse_x < 300 and 338 < mouse_y <367:
                    sound_click.play()#звук клик
                    sound_start.stop()#чтобы музка остановилась
                    return
            
#заставка перед начаом игры "round №"
round_images = [pygame.image.load("images/round_1.png").convert(),
                pygame.image.load("images/round_2.png").convert(),
                pygame.image.load("images/round_3.png").convert(),
                pygame.image.load("images/round_4.png").convert(),
                pygame.image.load("images/round_5.png").convert()]
for i in range(len (round_images)):#подгоняю под размер
    round_images[i] = scale_to_fit(round_images[i],500,540)
#функция показа заставки уровня
def show_round(level):
    sound_play.play(-1)#музыка для игры
    img = round_images[level-1]
    while True:
        screen.fill((0,0,0))#очищаем экран от предыдущей заставки
        x = (500 - img.get_width())//2
        y = (540 - img.get_height())//2
        screen.blit(img, (x,y))
        text = font.render("Press any key to start", True, (242,236,63))
        screen.blit(text, (140,150))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                sound_click.play()#звук клик
                return

#музыка
pygame.mixer.init()
sound_start = pygame.mixer.Sound("sounds/start.mp3")
sound_play = pygame.mixer. Sound("sounds/play.mp3")
sound_berry = pygame.mixer.Sound("sounds/berry.mp3")
sound_damage = pygame.mixer.Sound("sounds/damage.mp3")
sound_click = pygame.mixer.Sound("sounds/click.mp3")
            
#чтобы включилась заставка с Play 
show_cover()

#запуск заставки названия raund перед уровнем
show_round(level)
                
#заставка по окончанию каждого уровня "level complete"
complete_images = [pygame.image.load("images/level_complete_1.png").convert(),
                   pygame.image.load("images/level_complete_2.png").convert(),
                   pygame.image.load("images/level_complete_3.png").convert(),
                   pygame.image.load("images/level_complete_4.png").convert()]
for i in range(len(complete_images)):#подгоняю по размеру
    complete_images[i]= scale_to_fit(complete_images[i],500,540)
#функция показа экрана завершения уровня
def show_level_complete(level):
    sound_start.play()#музыка для заставки play
    img = complete_images[level-1]
    while True:
        screen.fill((0,0,0))
        x = (500 - img.get_width())//2
        y = (540 - img.get_height())//2
        screen.blit(img,(x,y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                sound_click.play()#звук клик
                sound_start.stop()#чтобы музка остановилась
                return

#финаьные картинки
win_img = pygame.image.load("images/win.png").convert()
win_img = scale_to_fit(win_img, 500, 540)
the_end_img = pygame.image.load("images/the_end.png").convert()
the_end_img = scale_to_fit(the_end_img, 500, 540)

#функция WIN (выиграш)
def show_win():
    sound_start.play()#музыка для заставки play
    firefly_color = (180,255,80)#цвет светячков
    while True:
        screen.fill((0,0,0))
        x = (500 - win_img.get_width()) // 2#заставка
        y = (540 - win_img.get_height()) // 2
        screen.blit(win_img,(x,y))
        t = pygame.time.get_ticks()
        for f in fireflies:#светлячки
# мерцание число 60..255
            f["x"] += f["vx"]
            f["y"] += f["vy"]
            if f["x"]<0 or f["x"]>500:f["vx"]*=-1
            if f["y"]<0 or f["y"]>500:f["vy"]*=-1
        
            alpha = 120 + 100 * math.sin((t + f["phase"]) * 0.004)
                  
            r = f["r"]

            size = 20* r
            glow = pygame.Surface((size, size),pygame.SRCALPHA)

            center = size//2
        
    # чуть-чуть "живости" — дрожание
            dx = random.uniform(-f["jitter"], f["jitter"])
            dy = random.uniform(-f["jitter"], f["jitter"])

    # рисуем кружок с альфой
            pygame.draw.circle(glow,(*firefly_color,int(alpha*0.15)),(center,center),6*r)
            pygame.draw.circle(glow,(*firefly_color,int(alpha*0.35)),(center,center),4*r)
            pygame.draw.circle(glow,(*firefly_color,int(alpha)),(center,center),1*r)
        
            screen.blit(glow, (f["x"] - center , f["y"] - center))
        
            s = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(s, (180, 255, 80, alpha), (10, 10), f["r"])
            screen.blit(s, (f["x"] - 10 + dx, f["y"] - 10 + dy))
        #текст "нажми любую кнопку"
        text = font.render("Press any key to start", True, (242,236,63))
        screen.blit(text, (140,500))
        pygame.display.update()
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

#функция the end
def show_the_end():
    firefly_color = (180,255,80)#цвет светячков
    while True:
        screen.fill((0,0,0))
        x = (500 - the_end_img.get_width()) // 2
        y = (540 - the_end_img.get_height()) // 2
        screen.blit(the_end_img,(x,y))
        t = pygame.time.get_ticks()
        for f in fireflies:#светлячки
# мерцание число 60..255
            f["x"] += f["vx"]
            f["y"] += f["vy"]
            if f["x"]<0 or f["x"]>500:f["vx"]*=-1
            if f["y"]<0 or f["y"]>500:f["vy"]*=-1
        
            alpha = 120 + 100 * math.sin((t + f["phase"]) * 0.004)
                  
            r = f["r"]

            size = 20* r
            glow = pygame.Surface((size, size),pygame.SRCALPHA)

            center = size//2
        
    # чуть-чуть "живости" — дрожание
            dx = random.uniform(-f["jitter"], f["jitter"])
            dy = random.uniform(-f["jitter"], f["jitter"])

    # рисуем кружок с альфой
            pygame.draw.circle(glow,(*firefly_color,int(alpha*0.15)),(center,center),6*r)
            pygame.draw.circle(glow,(*firefly_color,int(alpha*0.35)),(center,center),4*r)
            pygame.draw.circle(glow,(*firefly_color,int(alpha)),(center,center),1*r)
        
            screen.blit(glow, (f["x"] - center , f["y"] - center))
        
            s = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(s, (180, 255, 80, alpha), (10, 10), f["r"])
            screen.blit(s, (f["x"] - 10 + dx, f["y"] - 10 + dy))
        text = font.render("Press any key to start", True, (242,236,63))
        screen.blit(text, (150,450))
        text = font.render("Created by Ludmila Winckowska", True, (242,236,63))
        screen.blit(text, (100,490))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                sound_start.stop()#чтобы музка остановилась
                screen.fill((0,0,0))
                return


###################################################
###################################################
#цикл

running = True

while running:

    now = pygame.time.get_ticks() #про мигание гусеницы
    screen.blit(background, (0, 0)) #фон

    # --- draw fireflies (each frame) ---
    t = pygame.time.get_ticks() 

    #цвет светлячков в зависимости от уровня
    if level == 1:
        firefly_color = (180,255,80)
    elif level == 2:
        firefly_color = (120,200,255)
    elif level == 3:
        firefly_color = (200,120,255)
    elif level == 4:
        firefly_color = (255,140,220)
    elif level == 5:
        firefly_color = (255,120,80)

    #панель подстветка раунд, счёт, жизни
    panel = pygame.Surface((500,40),pygame.SRCALPHA)
    panel.fill((*firefly_color,60))#цвет панели в зависимости от уровня
    screen.blit(panel,(0,0))

    #строка информации (счёт, раунд. жизни)
    level_text = font.render(f"Level: {level}", True, firefly_color)#цвет
    score_text = font.render(f"Score: {score}", True, firefly_color)
    lives_text = font.render(f"Lives: {lives}", True, firefly_color)
    
    screen.blit(level_text, (20,10))#расстояние между словами
    screen.blit(score_text, (210,10))
    screen.blit(lives_text, (400,10))
        
    # мерцание число 60..255
    for f in fireflies:
        f["x"] += f["vx"]
        f["y"] += f["vy"]
        if f["x"]<0 or f["x"]>500:f["vx"]*=-1
        if f["y"]<0 or f["y"]>500:f["vy"]*=-1
        
        alpha = 120 + 100 * math.sin((t + f["phase"]) * 0.004)
                  
        r = f["r"]

        size = 20* r
        glow = pygame.Surface((size, size),pygame.SRCALPHA)

        center = size//2
        
    # чуть-чуть "живости" — дрожание
        dx = random.uniform(-f["jitter"], f["jitter"])
        dy = random.uniform(-f["jitter"], f["jitter"])

    # рисуем кружок с альфой
        pygame.draw.circle(glow,(*firefly_color,int(alpha*0.15)),(center,center),6*r)
        pygame.draw.circle(glow,(*firefly_color,int(alpha*0.35)),(center,center),4*r)
        pygame.draw.circle(glow,(*firefly_color,int(alpha)),(center,center),1*r)
        
        screen.blit(glow, (f["x"] - center , f["y"] - center))
        
        s = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(s, (180, 255, 80, alpha), (10, 10), f["r"])
        screen.blit(s, (f["x"] - 10 + dx, f["y"] - 10 + dy))


    #сетка
    for gx in range(0, 500, 50): pygame.draw.line(screen, (0,0,0),(gx,40),(gx,540))
    for gy in range(40, 540, 50): pygame.draw.line(screen, (0,0,0),(0,gy),(500,gy))

    #ягоды
    if level == 1:
        fruit = strawberries
    elif level == 2:
        fruit = blackberry
    elif level == 3:
        fruit = grapes
    elif level == 4:
        fruit = cherry
    elif level == 5:
        fruit = blueberry

    sx = grid_x * cell_size
    sy = grid_y * cell_size + 40
    
    screen.blit(fruit,(sx,sy))

    #препятствия
    if level == 1:
        obstacle = mushroom
    elif level == 2:
        obstacle = bee
    elif level == 3:
        obstacle = rose
    elif level == 4:
        obstacle = crystal
    elif level == 5:
        obstacle = frog

    mx = mush_x * cell_size
    my = mush_y * cell_size +40

    screen.blit(obstacle,(mx,my))
    
    #гусеница
    for i, segment in enumerate(caterpillar):
        x = segment[0] * cell_size
        y = segment[1] * cell_size + 40

        if i == 0: #голова
            rotated_head = head_img #чтобы голова поворачивалась
            if direction == (1,0):
                rotated_head = pygame.transform.rotate(head_img, 0)
            elif direction == (0,-1):
                rotated_head = pygame.transform.rotate(head_img, 90)
            elif direction == (-1,0):
                rotated_head = pygame.transform.rotate(head_img, 180)
            elif direction == (0,1):
                rotated_head = pygame.transform.rotate(head_img, 270)
            blink = (now % 200) < 100 #эта строка про мигание гусеницы
            if now < invincible_until:
                if blink:
                    screen.blit(rotated_head, (x,y))
            else:
                screen.blit(rotated_head,(x,y))
            

        elif i == len(caterpillar) - 1: #хвост
            prev = caterpillar[i-1]
            tail = caterpillar[i]
            tail_dir = (prev[0] - tail[0], prev[1] - tail[1])
            rotated_tail = tail_img
            
            if tail_dir == (1,0):
                rotated_tail = pygame.transform.rotate(tail_img,0)
            elif tail_dir == (-1,0):
                rotated_tail = pygame.transform.rotate(tail_img,180)
            elif tail_dir == (0,-1):
                rotated_tail = pygame.transform.rotate(tail_img, 90)
            elif tail_dir == (0,1):
                rotated_tail = pygame.transform.rotate(tail_img, 270)
            screen.blit(rotated_tail, (x,y))

        else:
            prev = caterpillar [i-1]#тело
            next = caterpillar [i+1]
            body_dir = (next[0] - prev[0], next[1] - prev[1])
            rotated_body = body_img
            if body_dir == (2,0) or body_dir == (-2,0):
                rotated_body = pygame.transform.rotate(body_img,0)
            elif body_dir == (0,2) or body_dir == (0,-2):
                rotated_body = pygame.transform.rotate(body_img,90)
            screen.blit(rotated_body, (x,y))
        
    #движение гусеницы
    now = pygame.time.get_ticks()
    if now - last_move>move_delay:
        
        head = caterpillar[0]
        new_x = (head[0] + direction[0]) % 10
        new_y = (head[1] + direction[1]) % 10

        new_head = (new_x, new_y)

        hit_self = new_head in caterpillar #про столкновение с собой
        if hit_self and now > invincible_until:
            sound_damage.play()#звук стокновение 
            lives -= 1
            invincible_until = now + 1500 #1.5 сукунды защиты от уменьшения
                                          #жизни при столкновении в себя
            
            #когда жизни 0, включается заставка game over
            if lives <= 0:
                game_over_screen()
                
        if not hit_self:#чтобы не выросла новая голова после столкновения с собой
            caterpillar.insert(0, new_head)

        #сьела и клубнику
        ate = (new_x == grid_x and new_y == grid_y)#сьела клубнику
        hit_mushroom = (new_x == mush_x and new_y == mush_y)#сьела гриб
        
        if hit_mushroom and now > invincible_until:
            sound_damage.play()#звук столкновение
            lives -= 1#сьел гриб -1 жизнь
            invincible_until = now + 1500#мигание гусеницы при столкновении
            
            #когда жизни 0, включается заставка game over
            if lives <= 0:
                game_over_screen()
                
            while True:#защита, чтобы гриб не появлялся на ягоде
                mush_x = random.randint(0,9)
                mush_y = random.randint(0,9)

                if not(mush_x == grid_x and mush_y == grid_y):
                    break
        
        #рост гусеницы
        if not ate and not hit_self:#и защита от уменьшения
                                    #при столкновении с собой
            caterpillar.pop()

        #создание новой клубники
        if ate:
            score +=1 #счёт
            sound_berry.play()#звук сьела ягоду
            if score >= 20:#для перехода на новый уровень
                sound_play.stop()#чтобы музка остановилась
                if level <= 4:#показать заставку пройденного раунда
                    show_level_complete(level)
                if level <5:#защита, не выходим за 5й уровень
                    level +=1
                    show_round(level)#показываем заставку нового уровня
                    score = 0
                    lives = 3
                else:
                    sound_play.stop()#чтобы музка остановилась
                    show_win()#покажи заставку выиграш
                    show_the_end()#покажи заставку the end
                    reset_game()#чтобы вернуось к началу игры и заставке play
                    show_cover()#покажи заставку play

                caterpillar = [(4,5),(3,5),(2,5)]#сброс гусеници на прежнее
            #место, после перехода на новый уровень (цифры -координаты места)
                direction = (1,0)

                grid_x = random.randint(0,9)
                grid_y = random.randint(0,9)
                
            while True:#защита, чтобы клубника не появлялась на грибе
                grid_x = random.randint(0,9)
                grid_y = random.randint(0,9)

                if not (grid_x == mush_x and grid_y == mush_y):
                    break

            sx = grid_x * cell_size
            sy = grid_y * cell_size + 40

        last_move = now
        
    pygame.display.update()
    
    for event in pygame.event.get():

        #управление стрелочками
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = (-1, 0)
            if event.key == pygame.K_RIGHT:
                direction = (1, 0)
            if event.key == pygame.K_UP:
                direction = (0, -1)
            if event.key == pygame.K_DOWN:
                direction = (0, 1)
        
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            
        #скорость гусеницы
        clock.tick(5)

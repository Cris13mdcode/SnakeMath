import pygame, random, sys, os, math

pygame.init()

# ─── Dimensiuni și grilă ────────────────────────────────────────────────
WIDTH, HEIGHT = 1000, 1000
CELL = 40  # dimensiune celulă pentru grila șarpelui (40x40 pixeli)
APPLE_SIZE = 40  # dimensiune măr (40x40 pixeli)

# ─── Fereastră ─────────────────────────────────────────────────────────
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakyMath")
clock = pygame.time.Clock()

# ─── Verificare fișiere imagine ─────────────────────────────────────────
required_files = [
    "snake_head.png",
    "snake_body.png",
    "Corner.png",
    "apple.png",
    "game_background.png",
    "main-menu.png",
    "question.png",
    "button.png",
    "button2.png"
]

# Verificăm dacă toate fișierele imagine există în directorul curent
font = pygame.font.Font(None, 36)  # Pentru mesaje de eroare
for file in required_files:
    file_path = os.path.join(file)
    if not os.path.exists(file_path):
        error_msg = f"Eroare: Fișierul {os.path.abspath(file_path)} lipsește! Asigură-te că toate imaginile sunt în directorul 'K:\\Users\\Cristi\\Desktop\\SnakeGame': {', '.join(required_files)}."
        print(error_msg)
        screen.fill((0, 0, 0))
        error_text = font.render(error_msg, True, (255, 0, 0))
        error_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(error_text, error_rect)
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

# ─── Încărcare sprite-uri (cap, corp, colț, măr, fundal) ───────────────
try:
    head_img = pygame.transform.scale(pygame.image.load("snake_head.png"), (CELL, CELL))
    body_img = pygame.transform.scale(pygame.image.load("snake_body.png"), (CELL, CELL))
    corner_img = pygame.transform.scale(pygame.image.load("Corner.png"), (CELL, CELL))
    apple_img = pygame.transform.scale(pygame.image.load("apple.png"), (APPLE_SIZE, APPLE_SIZE))
    background_img = pygame.transform.scale(pygame.image.load("game_background.png"), (WIDTH, HEIGHT))
    menu_background_img = pygame.transform.scale(pygame.image.load("main-menu.png"), (WIDTH, HEIGHT))
    question_background_img = pygame.transform.scale(pygame.image.load("question.png"), (WIDTH, HEIGHT))
    button_base_img = pygame.image.load("button.png").convert_alpha()
    button2_base_img = pygame.image.load("button2.png").convert_alpha()
    print(f"Succes: Toate imaginile ({', '.join(required_files)}) au fost încărcate din directorul '{os.path.abspath('.')}'!")
except pygame.error as e:
    error_msg = f"Eroare la încărcarea imaginilor: {str(e)}. Folosesc sprite-uri de rezervă (colorate)."
    print(error_msg)
    # Definim sprite-uri de rezervă pentru toate imaginile
    head_img = pygame.Surface((CELL, CELL))
    head_img.fill((0, 255, 0))  # Verde pentru cap
    body_img = pygame.Surface((CELL, CELL))
    body_img.fill((0, 200, 0))  # Verde închis pentru corp
    corner_img = pygame.Surface((CELL, CELL))
    corner_img.fill((0, 150, 0))  # Verde mediu pentru colțuri
    apple_img = pygame.Surface((APPLE_SIZE, APPLE_SIZE))
    apple_img.fill((255, 0, 0))  # Roșu pentru măr
    background_img = pygame.Surface((WIDTH, HEIGHT))
    background_img.fill((0, 50, 0))  # Verde închis pentru fundal
    menu_background_img = pygame.Surface((WIDTH, HEIGHT))
    menu_background_img.fill((0, 0, 50))  # Albastru închis pentru meniu
    question_background_img = pygame.Surface((WIDTH, HEIGHT))
    question_background_img.fill((20, 20, 20))
    # Buton de rezervă (gri)
    button_base_img = pygame.Surface((400, 100), pygame.SRCALPHA)
    button_base_img.fill((80, 80, 80, 230))
    button2_base_img = pygame.Surface((200, 80), pygame.SRCALPHA)
    button2_base_img.fill((100, 100, 100, 230))
    print("Avertisment: Imaginile nu au fost găsite. Folosesc sprite-uri de rezervă colorate.")

# ─── Fonturi ───────────────────────────────────────────────────────────
font = pygame.font.Font(None, 36)  # Pentru scor și mesaje
math_font = pygame.font.Font(None, 48)  # Pentru cifre pe șarpe/măr și întrebări
option_font = pygame.font.Font(None, 60)  # Pentru opțiuni de răspuns și meniu

# ─── UI Helpers ─────────────────────────────────────────────────────────
BUTTON_SIZE = (400, 100)
button_img_scaled = pygame.transform.scale(button_base_img, BUTTON_SIZE)
BUTTON2_SIZE = (200, 80)
button2_img_scaled = pygame.transform.scale(button2_base_img, BUTTON2_SIZE)

LIGHT_GREEN = (140, 255, 140)
DARK_GREEN = (0, 140, 0)

# ─── Efecte vizuale ─────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.life = 60  # 3 secunde la 20 FPS
        self.color = random.choice([(255, 255, 0), (255, 165, 0), (255, 69, 0), (255, 215, 0)])
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vy += 0.1  # gravitație
    
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / 60))
            size = max(2, int(8 * (self.life / 60)))
            color = (*self.color[:3], alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

particles = []
particle_timer = 0
snake_red_timer = 0  # Timer pentru șarpe roșu

def draw_button(label_text, center_pos, is_selected=False):
    btn_rect = button_img_scaled.get_rect(center=center_pos)
    screen.blit(button_img_scaled, btn_rect)

    # Two-tone green text (light top, dark bottom)
    text_light = option_font.render(label_text, True, LIGHT_GREEN)
    text_dark = option_font.render(label_text, True, DARK_GREEN)
    text_rect = text_light.get_rect(center=btn_rect.center)
    half_h = text_rect.height // 2

    # Optional subtle scale for selected
    if is_selected:
        # Slight visual emphasis by drawing a faint outline shadow
        shadow = option_font.render(label_text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
        screen.blit(shadow, shadow_rect)

    # Blit top half (light green)
    screen.blit(text_light, text_rect, area=pygame.Rect(0, 0, text_rect.width, half_h))
    # Blit bottom half (dark green)
    screen.blit(text_dark, (text_rect.x, text_rect.y + half_h), area=pygame.Rect(0, half_h, text_rect.width, text_rect.height - half_h))

def draw_button_resizable(label_text, center_pos, size, is_selected=False):
    btn_img = pygame.transform.scale(button_base_img, size)
    btn_rect = btn_img.get_rect(center=center_pos)
    screen.blit(btn_img, btn_rect)

    text_light = option_font.render(label_text, True, LIGHT_GREEN)
    text_dark = option_font.render(label_text, True, DARK_GREEN)
    text_rect = text_light.get_rect(center=btn_rect.center)
    half_h = text_rect.height // 2

    if is_selected:
        shadow = option_font.render(label_text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
        screen.blit(shadow, shadow_rect)

    screen.blit(text_light, text_rect, area=pygame.Rect(0, 0, text_rect.width, half_h))
    screen.blit(text_dark, (text_rect.x, text_rect.y + half_h), area=pygame.Rect(0, half_h, text_rect.width, text_rect.height - half_h))

def draw_button_resizable_singlecolor(label_text, center_pos, size, color, is_selected=False):
    btn_img = pygame.transform.scale(button_base_img, size)
    btn_rect = btn_img.get_rect(center=center_pos)
    screen.blit(btn_img, btn_rect)

    text = option_font.render(label_text, True, color)
    text_rect = text.get_rect(center=btn_rect.center)
    if is_selected:
        shadow = option_font.render(label_text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
        screen.blit(shadow, shadow_rect)
    screen.blit(text, text_rect)

def draw_button2(label_text, center_pos, is_selected=False):
    btn_rect = button2_img_scaled.get_rect(center=center_pos)
    screen.blit(button2_img_scaled, btn_rect)

    text_light = option_font.render(label_text, True, LIGHT_GREEN)
    text_dark = option_font.render(label_text, True, DARK_GREEN)
    text_rect = text_light.get_rect(center=btn_rect.center)
    half_h = text_rect.height // 2

    if is_selected:
        shadow = option_font.render(label_text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
        screen.blit(shadow, shadow_rect)

    screen.blit(text_light, text_rect, area=pygame.Rect(0, 0, text_rect.width, half_h))
    screen.blit(text_dark, (text_rect.x, text_rect.y + half_h), area=pygame.Rect(0, half_h, text_rect.width, text_rect.height - half_h))

# ─── Dificultăți ───────────────────────────────────────────────────────
DIFFICULTIES = {
    "Ușoară": {"max_num": 10, "operations": ["+", "-"]},
    "Medie": {"max_num": 20, "operations": ["+", "-"]},
    "Greu": {"max_num": 30, "operations": ["+", "-"]}
}
current_difficulty = "Ușoară"  # Setăm implicit „Ușoară” conform cererii

# ─── Funcții desen ─────────────────────────────────────────────────────
def draw_background():
    screen.blit(background_img, (0, 0))
    # Desenăm grila 40x40 cu o culoare închisă (gri închis)
    grid_color = (50, 50, 50)  # Gri închis
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y), 1)

def draw_menu_background():
    screen.blit(menu_background_img, (0, 0))

def draw_snake(coords, direction, current_sum):
    global snake_red_timer
    
    # Verificăm dacă șarpele trebuie să fie roșu
    is_red = snake_red_timer > 0
    
    for i, (x, y) in enumerate(coords):
        if i == 0:  # Capul șarpelui
            if direction == (0, CELL):  # Jos
                rotated_head = head_img
            elif direction == (0, -CELL):  # Sus
                rotated_head = pygame.transform.rotate(head_img, 180)
            elif direction == (CELL, 0):  # Dreapta
                rotated_head = pygame.transform.rotate(head_img, 90)
            elif direction == (-CELL, 0):  # Stânga
                rotated_head = pygame.transform.rotate(head_img, -90)
            
            # Dacă șarpele e roșu, colorăm capul
            if is_red:
                red_head = rotated_head.copy()
                red_head.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
                head_rect = red_head.get_rect(center=(x + CELL // 2, y + CELL // 2))
                screen.blit(red_head, head_rect)
            else:
                head_rect = rotated_head.get_rect(center=(x + CELL // 2, y + CELL // 2))
                screen.blit(rotated_head, head_rect)
            
            # Afișăm suma deasupra capului
            sum_text = math_font.render(str(current_sum), True, (255, 255, 255))
            sum_rect = sum_text.get_rect(center=(x + CELL // 2, y - CELL // 2))  # Plasăm deasupra capului
            screen.blit(sum_text, sum_rect)
        else:  # Corpul și colțurile șarpelui
            next_pos = coords[i - 1]  # Poziția segmentului următor (spre cap)
            prev_pos = coords[i + 1] if i + 1 < len(coords) else None  # Poziția segmentului precedent
            dx_next, dy_next = next_pos[0] - x, next_pos[1] - y
            if prev_pos:  # Verificăm dacă e colț
                dx_prev, dy_prev = x - prev_pos[0], y - prev_pos[1]
                if (dx_next != 0 and dy_prev != 0) or (dy_next != 0 and dx_prev != 0):  # Colț
                    if dx_next > 0 and dy_prev > 0:  # Dreapta -> Jos
                        rotated_corner = pygame.transform.rotate(corner_img, 0)
                    elif dx_next > 0 and dy_prev < 0:  # Dreapta -> Sus
                        rotated_corner = pygame.transform.rotate(corner_img, 270)
                    elif dx_next < 0 and dy_prev > 0:  # Stânga -> Jos
                        rotated_corner = pygame.transform.rotate(corner_img, 90)
                    elif dx_next < 0 and dy_prev < 0:  # Stânga -> Sus
                        rotated_corner = pygame.transform.rotate(corner_img, 180)
                    elif dy_next > 0 and dx_prev > 0:  # Jos -> Dreapta
                        rotated_corner = pygame.transform.rotate(corner_img, 180)
                    elif dy_next > 0 and dx_prev < 0:  # Jos -> Stânga
                        rotated_corner = pygame.transform.rotate(corner_img, 270)
                    elif dy_next < 0 and dx_prev > 0:  # Sus -> Dreapta
                        rotated_corner = pygame.transform.rotate(corner_img, 90)
                    elif dy_next < 0 and dx_prev < 0:  # Sus -> Stânga
                        rotated_corner = pygame.transform.rotate(corner_img, 0)
                    corner_rect = rotated_corner.get_rect(center=(x + CELL // 2, y + CELL // 2))
                    if is_red:
                        red_corner = rotated_corner.copy()
                        red_corner.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
                        screen.blit(red_corner, corner_rect)
                    else:
                        screen.blit(rotated_corner, corner_rect)
                else:  # Segment drept
                    if dy_next != 0:  # Vertical
                        rotated_body = pygame.transform.rotate(body_img, 90)
                        body_rect = rotated_body.get_rect(center=(x + CELL // 2, y + CELL // 2))
                        if is_red:
                            red_body = rotated_body.copy()
                            red_body.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
                            screen.blit(red_body, body_rect)
                        else:
                            screen.blit(rotated_body, body_rect)
                    else:  # Orizontal
                        body_rect = body_img.get_rect(center=(x + CELL // 2, y + CELL // 2))
                        if is_red:
                            red_body = body_img.copy()
                            red_body.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
                            screen.blit(red_body, body_rect)
                        else:
                            screen.blit(body_img, body_rect)
            else:  # Ultimul segment (coada)
                if dy_next != 0:  # Vertical
                    rotated_body = pygame.transform.rotate(body_img, 90)
                    body_rect = rotated_body.get_rect(center=(x + CELL // 2, y + CELL // 2))
                    if is_red:
                        red_body = rotated_body.copy()
                        red_body.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
                        screen.blit(red_body, body_rect)
                    else:
                        screen.blit(rotated_body, body_rect)
                else:  # Orizontal
                    body_rect = body_img.get_rect(center=(x + CELL // 2, y + CELL // 2))
                    if is_red:
                        red_body = body_img.copy()
                        red_body.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
                        screen.blit(red_body, body_rect)
                    else:
                        screen.blit(body_img, body_rect)

def draw_apple(pos, apple_number):
    offset = (CELL - APPLE_SIZE) // 2
    screen.blit(apple_img, (pos[0] + offset, pos[1] + offset))
    # Afișăm cifra pe măr (poate fi negativă)
    num_text = math_font.render(str(apple_number), True, (255, 255, 255))
    num_rect = num_text.get_rect(center=(pos[0] + CELL // 2, pos[1] + CELL // 2))
    screen.blit(num_text, num_rect)

# ─── Funcție pentru popup cu întrebare matematică ──────────────────────
def show_math_question(current_sum, apple_number, operation):
    if operation == "+":
        correct_answer = current_sum + apple_number
        question = f"{current_sum} + {apple_number} = ?"
    else:  # "-"
        correct_answer = current_sum - apple_number
        question = f"{current_sum} - {apple_number} = ?"

    # Generează 2 răspunsuri greșite (apropiate, dar diferite)
    wrong1 = correct_answer + random.randint(-2, -1) if random.choice([True, False]) else correct_answer + random.randint(1, 2)
    wrong2 = correct_answer + random.randint(-2, -1) if wrong1 > correct_answer else correct_answer + random.randint(1, 2)
    options = [correct_answer, wrong1, wrong2]
    random.shuffle(options)  # Amestecă opțiunile
    selected = 1  # Începe cu opțiunea din mijloc selectată (index 1)

    while True:
        # Fundal întrebare: imaginea question.png
        screen.blit(question_background_img, (0, 0))

        # Întrebarea pe button.png
        draw_button_resizable_singlecolor(question, (WIDTH // 2, HEIGHT // 2 - 100), (600, 100), (255, 255, 255))

        # Opțiuni jos pe button2.png (3 ferestre)
        option_width = WIDTH // 4
        for i, opt in enumerate(options):
            center_pos = (option_width * (i + 1), HEIGHT - 100)
            draw_button2(str(opt), center_pos, is_selected=(i == selected))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    selected = max(0, selected - 1)
                if e.key == pygame.K_RIGHT:
                    selected = min(2, selected + 1)
                if e.key == pygame.K_RETURN:  # Enter
                    chosen = options[selected]
                    return chosen == correct_answer

# ─── Funcție pentru meniul principal ───────────────────────────────────
def show_menu():
    global current_difficulty
    options = ["Start", "Dificultate", "Ieșire"]
    selected = 0

    while True:
        draw_menu_background()

        # Titlu
        title_text = option_font.render("SnakyMath", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        screen.blit(title_text, title_rect)

        # Opțiuni pe butoane
        for i, opt in enumerate(options):
            center = (WIDTH // 2, HEIGHT // 2 + i * 120)
            draw_button(opt, center, is_selected=(i == selected))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = max(0, selected - 1)
                if e.key == pygame.K_DOWN:
                    selected = min(len(options) - 1, selected + 1)
                if e.key == pygame.K_RETURN:
                    if options[selected] == "Start":
                        return  # Pornim jocul
                    elif options[selected] == "Dificultate":
                        show_difficulty_menu()
                    elif options[selected] == "Ieșire":
                        pygame.quit()
                        sys.exit()

def show_difficulty_menu():
    global current_difficulty
    diff_options = list(DIFFICULTIES.keys())
    selected = diff_options.index(current_difficulty)

    while True:
        draw_menu_background()

        # Titlu
        title_text = option_font.render("Selectează Dificultate", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
        screen.blit(title_text, title_rect)

        # Opțiuni pe butoane
        for i, opt in enumerate(diff_options):
            center = (WIDTH // 2, HEIGHT // 2 + (i - 1) * 120)
            draw_button(opt, center, is_selected=(i == selected))

        # Buton "Înapoi" (vizual). Navigarea rămâne prin ESC.
        draw_button("Înapoi (Esc)", (WIDTH // 2, HEIGHT // 2 + 200))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = max(0, selected - 1)
                if e.key == pygame.K_DOWN:
                    selected = min(len(diff_options) - 1, selected + 1)
                if e.key == pygame.K_RETURN:
                    current_difficulty = diff_options[selected]
                    return  # Înapoi la meniul principal
                if e.key == pygame.K_ESCAPE:
                    return  # Înapoi la meniul principal

# ─── Funcție pentru game over ───────────────────────────────────────────
def game_over(score):
    selected = 0  # 0: Restart, 1: Main Menu
    options = ["Restart", "Main Menu"]
    pygame.time.wait(300)
    while True:
        # Afișează fundalul jocului (fără overlay întunecat)
        draw_background()

        # Title button (red text)
        draw_button_resizable_singlecolor("GAME OVER", (WIDTH//2, HEIGHT//2 - 180), (600, 110), (255, 60, 60))

        # Action buttons
        draw_button(options[0], (WIDTH//2 - 240, HEIGHT//2 - 20), is_selected=(selected == 0))
        draw_button(options[1], (WIDTH//2 + 240, HEIGHT//2 - 20), is_selected=(selected == 1))

        # Score button below (blue text)
        draw_button_resizable_singlecolor(f"Score: {score}", (WIDTH//2, HEIGHT//2 + 120), (500, 100), (80, 160, 255))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    selected = max(0, selected - 1)
                if e.key == pygame.K_RIGHT:
                    selected = min(1, selected + 1)
                if e.key == pygame.K_RETURN:
                    if selected == 0:
                        return start_game()
                    else:
                        return main()
                if e.key == pygame.K_r:
                    return start_game()
                if e.key in (pygame.K_ESCAPE, pygame.K_m):
                    return main()

# ─── Logica joc ─────────────────────────────────────────────────────────
def random_cell(exclude):
    while True:
        x = random.randrange(CELL, WIDTH - CELL, CELL)
        y = random.randrange(CELL, HEIGHT - CELL, CELL)
        if (x, y) not in exclude:
            return (x, y)

def start_game():
    global particle_timer, particles, snake_red_timer
    
    # Inițializăm jocul
    snake = [(CELL * 2, CELL * 2)]
    direction = (CELL, 0)
    current_sum = 0
    score = 0
    max_num = DIFFICULTIES[current_difficulty]["max_num"]
    operations = DIFFICULTIES[current_difficulty]["operations"]
    apple_number = random.randint(1, max_num)
    operation = "+"
    apple = random_cell(snake)
    paused = False
    
    # Reset efecte vizuale
    particles.clear()
    particle_timer = 0
    snake_red_timer = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:  # Pauză
                    paused = not paused
                if not paused:
                    if e.key == pygame.K_UP and direction != (0, CELL): direction = (0, -CELL)
                    if e.key == pygame.K_DOWN and direction != (0, -CELL): direction = (0, CELL)
                    if e.key == pygame.K_LEFT and direction != (CELL, 0): direction = (-CELL, 0)
                    if e.key == pygame.K_RIGHT and direction != (-CELL, 0): direction = (CELL, 0)

        if paused:
            continue

        # ─ Mișcă șarpele ─
        proposed_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        # Dacă lovește peretele sau propriul corp: pierde o unitate din lungime și rămâne pe loc
        hits_wall = not (0 <= proposed_head[0] < WIDTH) or not (0 <= proposed_head[1] < HEIGHT)
        hits_self = proposed_head in snake
        if hits_wall or hits_self:
            if len(snake) > 1:
                snake.pop()  # reduce lungimea cu 1
                # sari peste restul logicii acestui frame
                # (nu mutăm capul, nu verificăm mărul)
                # continua la următorul ciclu
                # folosim continue din buclă
                # notă: sum și score rămân neschimbate
                pass
            else:
                return game_over(score)
            # Trecem la următoarea iterație fără alte acțiuni
            continue
        else:
            # Mișcare normală
            new_head = proposed_head
            snake.insert(0, new_head)

        # ─ Coliziune cu mărul ─
        ate_apple = False
        if new_head == apple:
            ate_apple = True
        else:
            snake.pop()  # Mișcare normală, pop coada

        # ─ Coliziune cu sine (fallback) ─
        # În mod normal e prins înainte de mutare, dar păstrăm un fallback defensiv
        if new_head in snake[1:]:
            if len(snake) > 1:
                # Anulăm mutarea capului și scurtăm coada
                snake.pop(0)
                snake.pop()
                continue
            else:
                return game_over(score)

        # Dacă a mâncat mărul, arată întrebarea
        if ate_apple:
            correct = show_math_question(current_sum, abs(apple_number), operation)
            if correct:
                if operation == "+":
                    current_sum += abs(apple_number)
                else:
                    current_sum -= abs(apple_number)
                current_sum = min(current_sum, max_num)
                current_sum = max(current_sum, 0)
                score += 1
                # Efecte vizuale pentru răspuns corect - particule pe întregul ecran
                for _ in range(50):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    particles.append(Particle(x, y))
                particle_timer = 60  # 3 secunde
            else:
                # Răspuns greșit: scade 1 punct din score și 1 celulă din șarpe
                score = max(0, score - 1)
                snake_red_timer = 20  # 1 secundă (20 FPS)
                if len(snake) > 1:
                    snake.pop()
                else:
                    return game_over(score)
            # Generează nou măr și operație
            operation = random.choice(operations)
            if operation == "+":
                apple_number = random.randint(1, max_num - current_sum) if current_sum < max_num else 1
            else:
                apple_number = -random.randint(1, current_sum) if current_sum > 0 else 1
            apple = random_cell(snake)

        # ─ Desen ─
        draw_background()
        draw_apple(apple, apple_number)
        draw_snake(snake, direction, current_sum)
        
        # Efecte vizuale (particule)
        if particle_timer > 0:
            particle_timer -= 1
            for particle in particles[:]:
                particle.update()
                particle.draw(screen)
                if particle.life <= 0:
                    particles.remove(particle)
        
        # Timer pentru șarpe roșu
        if snake_red_timer > 0:
            snake_red_timer -= 1
        
        # Afișare în colțul stânga sus: Sum și Length (length afișat cu -1, min 0)
        display_length = max(0, len(snake) - 1)
        left_text = font.render(f"Sum: {current_sum} | Length: {display_length}", True, (0, 0, 0))
        screen.blit(left_text, (10, 10))
        
        # Afișare în colțul dreapta sus: Score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(score_text, score_rect)
        
        if paused:
            # fundal semi-transparent
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(160)
            screen.blit(overlay, (0, 0))

            # Titlu pauză
            pause_text = option_font.render("PAUZĂ", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
            screen.blit(pause_text, pause_rect)

            # Buton „Continuă (P)”
            draw_button("Continuă (P)", (WIDTH // 2, HEIGHT // 2))

        pygame.display.flip()

        # Viteza crește, dar limitată la 15 FPS (mai lentă când șarpele e roșu)
        base_speed = min(15, 5 + len(snake) // 5)
        if snake_red_timer > 0:
            base_speed = max(8, base_speed - 3)  # Scade viteza când e roșu
        clock.tick(base_speed)

def main():
    show_menu()
    return start_game()

# ─── Rulează jocul ─────────────────────────────────────────────────────
if __name__ == "__main__":
    main()



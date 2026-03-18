import pygame
import random
import math
from codecarbon import EmissionsTracker

pygame.init()

# CONFIGURATION
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Quest")

clock = pygame.time.Clock()

# COULEURS
BG = (180, 220, 170)
PANEL = (120, 170, 110)
WOOD = (140, 100, 70)
LEAF = (70, 160, 90)
FLOWER = (220, 200, 120)
RED = (220, 80, 80)
WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
SHADOW = (90, 120, 90)

font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 28)

# CONSTANTES PARABOLE
GRAVITY = 35
START_X = 200
START_Y = 430
speed = 180

main_rect = pygame.Rect(150, 100, 600, 400)

button1 = pygame.Rect(180, 550, 150, 50)
button2 = pygame.Rect(375, 550, 150, 50)
button3 = pygame.Rect(570, 550, 150, 50)

play_button = pygame.Rect(350, 300, 200, 80)
menu_button = pygame.Rect(20, 650, 150, 40)

restart_button = pygame.Rect(300, 400, 150, 60)
back_menu_button = pygame.Rect(500, 400, 150, 60)

# INITIALISATION
game_state = "menu"
current_game = 1
game_over = False
victory = False

timer = 120
start_ticks = pygame.time.get_ticks()

progression_ecologique = 0

# MINI-JEU 1
graines_collectees = 0
recolte_terminee = False
graine_cible = pygame.Rect(random.randint(200, 700), random.randint(150, 450), 40, 40)

# MINI-JEU 2
chenille = [(300, 200)]
direction_chenille = (20, 0)
fruit = (500, 300)
timer_chenille = 0
pommes_mangees = 0
chenille_terminee = False

# MINI-JEU 3
tir_actif = False
temps_tir = 0
semis_reussis = 0
lancer_termine = False
angle = 45


def cible_atteignable(fx, fy):
    dx = fx - START_X
    for ang in range(25, 66):
        rad = math.radians(ang)
        y = START_Y - dx * math.tan(rad) + (GRAVITY * dx**2)/(2*speed**2*math.cos(rad)**2)
        if abs(y - fy) < 30:
            return True
    return False


def generer_fleur():
    while True:
        fx = random.randint(480, 620)
        fy = random.randint(260, 360)
        if cible_atteignable(fx, fy):
            return pygame.Rect(fx, fy, 40, 40)


fleur_cible = generer_fleur()


def draw_button(rect, color, text):
    pygame.draw.rect(screen, SHADOW, rect.move(3, 3), border_radius=18)
    pygame.draw.rect(screen, color, rect, border_radius=18)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=18)

    txt = small_font.render(text, True, BLACK)
    screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))


def reset_game():
    global progression_ecologique
    global graines_collectees, recolte_terminee
    global chenille, direction_chenille, pommes_mangees, chenille_terminee
    global tir_actif, temps_tir, semis_reussis, lancer_termine
    global game_over, victory, start_ticks, fleur_cible, angle

    progression_ecologique = 0

    graines_collectees = 0
    recolte_terminee = False

    chenille = [(300, 200)]
    direction_chenille = (20, 0)
    pommes_mangees = 0
    chenille_terminee = False

    tir_actif = False
    temps_tir = 0
    semis_reussis = 0
    lancer_termine = False

    fleur_cible = generer_fleur()
    angle = 45

    game_over = False
    victory = False
    start_ticks = pygame.time.get_ticks()


# BOUCLE PRINCIPALE
running = True

tracker = EmissionsTracker()
tracker.start()
try:
    while running:
        screen.fill(BG)

        for i in range(0, WIDTH, 80):
            pygame.draw.circle(screen, (160, 210, 150), (i, 60), 25)

        for i in range(40, WIDTH, 120):
            pygame.draw.circle(screen, (150, 200, 140), (i, 640), 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # SOURIS
            if event.type == pygame.MOUSEBUTTONDOWN:

                if game_state == "menu":
                    if play_button.collidepoint(event.pos):
                        reset_game()
                        game_state = "game"

                elif game_state == "game":

                    if game_over or victory:
                        if restart_button.collidepoint(event.pos):
                            reset_game()

                        if back_menu_button.collidepoint(event.pos):
                            reset_game()
                            game_state = "menu"

                    else:
                        if menu_button.collidepoint(event.pos):
                            game_state = "menu"

                        if button1.collidepoint(event.pos):
                            current_game = 1
                        if button2.collidepoint(event.pos):
                            current_game = 2
                        if button3.collidepoint(event.pos):
                            current_game = 3

                        # MINI-JEU 1
                        if current_game == 1 and graine_cible.collidepoint(event.pos) and not recolte_terminee:
                            graines_collectees += 1
                            graine_cible.x = random.randint(200, 700)
                            graine_cible.y = random.randint(150, 450)

                            if graines_collectees >= 10:
                                recolte_terminee = True
                                progression_ecologique += 1

                        # MINI-JEU 3
                        if current_game == 3 and not tir_actif and not lancer_termine:
                            tir_actif = True
                            temps_tir = 0
            # CLAVIER
            if event.type == pygame.KEYDOWN:

                if current_game == 2:
                    if event.key == pygame.K_UP:
                        direction_chenille = (0, -20)
                    if event.key == pygame.K_DOWN:
                        direction_chenille = (0, 20)
                    if event.key == pygame.K_LEFT:
                        direction_chenille = (-20, 0)
                    if event.key == pygame.K_RIGHT:
                        direction_chenille = (20, 0)

                if current_game == 3:
                    if event.key == pygame.K_LEFT:
                        angle = max(25, angle - 2)
                    if event.key == pygame.K_RIGHT:
                        angle = min(65, angle + 2)

        # MENU
        if game_state == "menu":
            title = font.render("Forest Quest", True, BLACK)
            screen.blit(title, (340, 200))
            draw_button(play_button, LEAF, "Commencer")

        # JEU
        else:

            secondes = timer - (pygame.time.get_ticks() - start_ticks)//1000

            if secondes <= 0:
                game_over = True

            if progression_ecologique >= 3:
                victory = True

            if game_over:
                screen.blit(font.render("La forêt s'affaiblit...", True, RED), (230, 250))
                draw_button(restart_button, LEAF, "Replanter")
                draw_button(back_menu_button, FLOWER, "Accueil")

            elif victory:
                screen.blit(font.render("Forêt restaurée !", True, LEAF), (270, 250))
                draw_button(restart_button, LEAF, "Replanter")
                draw_button(back_menu_button, FLOWER, "Accueil")

            else:

                pygame.draw.rect(screen, PANEL, main_rect, border_radius=30)
                draw_button(menu_button, FLOWER, "Accueil")

                # MINI-JEU 1
                if current_game == 1:
                    pygame.draw.rect(screen, WOOD, graine_cible, border_radius=8)
                    screen.blit(small_font.render(f"Graines {graines_collectees}/10", True, BLACK), (350, 120))

                # MINI-JEU 2
                elif current_game == 2:

                    timer_chenille += 1

                    if timer_chenille > 5:
                        timer_chenille = 0

                        head = (chenille[0][0]+direction_chenille[0], chenille[0][1]+direction_chenille[1])

                        if not main_rect.collidepoint(head) or head in chenille:
                            chenille = [(300, 200)]
                            pommes_mangees = 0

                        else:
                            chenille.insert(0, head)

                            if head == fruit:
                                pommes_mangees += 1
                                fruit = (
                                    random.randint(200, 700)//20*20,
                                    random.randint(150, 450)//20*20
                                )

                                if pommes_mangees >= 10:
                                    progression_ecologique += 1

                            else:
                                chenille.pop()

                    for segment in chenille:
                        pygame.draw.rect(screen, LEAF, (*segment, 20, 20), border_radius=6)

                    pygame.draw.rect(screen, RED, (*fruit, 20, 20), border_radius=6)

                    screen.blit(small_font.render(f"Fruits {pommes_mangees}/10", True, BLACK), (350, 120))

                # MINI-JEU 3
                elif current_game == 3:

                    pygame.draw.rect(screen, FLOWER, fleur_cible, border_radius=10)

                    pygame.draw.rect(screen, WHITE, (300, 470, 200, 20), border_radius=10)
                    pygame.draw.rect(screen, LEAF, (300, 470, (angle-25)*5, 20), border_radius=10)

                    screen.blit(small_font.render(f"Angle {angle}°", True, BLACK), (520, 465))

                    if tir_actif:
                        temps_tir += 0.08
                        rad = math.radians(angle)

                        x = START_X + speed*math.cos(rad)*temps_tir
                        y = START_Y - speed*math.sin(rad)*temps_tir + GRAVITY*temps_tir**2

                        pygame.draw.circle(screen, WOOD, (int(x), int(y)), 12)

                        if pygame.Rect(x-10, y-10, 20, 20).colliderect(fleur_cible):
                            semis_reussis += 1
                            tir_actif = False
                            fleur_cible = generer_fleur()

                            if semis_reussis >= 5:
                                progression_ecologique += 1

                        if y > 500:
                            tir_actif = False

                    screen.blit(small_font.render(f"Semis {semis_reussis}/5", True, BLACK), (350, 120))

                # HUD
                screen.blit(font.render(f"Progression {progression_ecologique}/3", True, BLACK), (620, 20))
                screen.blit(font.render(f"Temps {secondes}", True, BLACK), (20, 20))

                draw_button(button1, WOOD, "Récolte")
                draw_button(button2, LEAF, "Chenille")
                draw_button(button3, FLOWER, "Semis")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
finally:
    tracker.stop()

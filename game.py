
import pygame
import sys
import time
import math
import random

def dessiner_texte(fenetre, texte, font, couleur, pos):
    ombre = font.render(texte, True, (30,30,30))
    fenetre.blit(ombre, (pos[0]+2, pos[1]+2))

    txt = font.render(texte, True, couleur)
    fenetre.blit(txt, pos)


def dessiner_bouton(fenetre, rect, texte, font):
    souris = pygame.mouse.get_pos()

    couleur = (50,160,90)
    if rect.collidepoint(souris):
        couleur = (70,190,110)

    # Ombre
    ombre = rect.copy()
    ombre.y += 4
    pygame.draw.rect(fenetre, (30,30,30), ombre, border_radius=10)

    # Bouton
    pygame.draw.rect(fenetre, couleur, rect, border_radius=10)

    # Texte
    txt = font.render(texte, True, (240,240,240))
    rect_txt = txt.get_rect(center=rect.center)
    fenetre.blit(txt, rect_txt)


def dessiner_barre(fenetre, x, y, largeur, hauteur, progression):
    pygame.draw.rect(fenetre, (200,200,200), (x, y, largeur, hauteur), border_radius=10)
    pygame.draw.rect(fenetre, (0, 200, 0), (x, y, largeur * progression, hauteur), border_radius=10)

def dessiner_trajectoire(fenetre, x, y, vx, vy, zone):
    sim_x = x
    sim_y = y

    for i in range(30):
        vy += 0.2
        sim_x += vx
        sim_y += vy

        if not zone.collidepoint(sim_x, sim_y):
            break

        pygame.draw.circle(fenetre, (255, 255, 255), (int(sim_x), int(sim_y)), 3)


def jeu(fenetre, largeur, hauteur):
    # 🎨 Couleurs modernes
    VERT_FOND = (34, 120, 60)
    VERT_UI = (50, 160, 90)
    VERT_HOVER = (70, 190, 110)
    BLANC = (240, 240, 240)
    NOIR = (30, 30, 30)
    GRIS = (200, 200, 200)

    clock = pygame.time.Clock()

    score = 0
    objectif = 100

    temps_max = 30
    debut = time.time()

    font = pygame.font.SysFont(None, 40)

    mini_jeu = None

    bouton_arroser = pygame.Rect(50, hauteur - 80, 150, 50)
    bouton_fertiliser = pygame.Rect(250, hauteur - 80, 150, 50)
    bouton_couper = pygame.Rect(450, hauteur - 80, 200, 50)

    # 🔘 bouton menu
    bouton_menu = pygame.Rect(largeur - 120, 20, 100, 40)

    zone = pygame.Rect(largeur//2 - 250, hauteur//2 - 150, 500, 300)

    # 💧 goutte
    goutte_x = zone.left + 20
    goutte_y = zone.centery
    vx = 0
    vy = 0
    lance = False
    pret_a_lancer = False

    # 🌱 fertiliser
    panier = pygame.Rect(zone.centerx - 40, zone.bottom - 30, 80, 20)
    engrais = []
    vitesse_engrais = 5
    spawn_timer = 0
    rate = 30
    rates = 0
    max_rates = 5

    # 🌿 mauvaises herbes
    herbes = []
    spawn_timer_herbe = 0
    spawn_rate_herbe = 60
    max_herbes = 10

    vague = 1
    plantes = []

    def creer_plantes(vague):
        if vague == 1:
            return [
                pygame.Rect(zone.left + 300, zone.top + 50, 40, 40),
                pygame.Rect(zone.left + 350, zone.top + 150, 40, 40)
            ]
        elif vague == 2:
            return [
                pygame.Rect(zone.left + 250, zone.top + 40, 40, 40),
                pygame.Rect(zone.left + 320, zone.top + 120, 40, 40),
                pygame.Rect(zone.left + 400, zone.top + 80, 40, 40)
            ]
        return []

    message_fin = ""
    temps_message = 0

    running = True
    while running:

        temps_restant = int(temps_max - (time.time() - debut))
        # 🎉 victoire immédiate
        if score >= objectif:
            return "victoire"

        # ⏱️ fin du temps = game over
        if temps_restant <= 0:
            return "game_over"


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # 🔘 bouton menu
                if bouton_menu.collidepoint(event.pos):
                    return "menu"

                if bouton_arroser.collidepoint(event.pos):
                    mini_jeu = "arroser"
                    vague = 1
                    plantes = creer_plantes(vague)

                    goutte_x = zone.left + 20
                    goutte_y = zone.centery
                    vx = 0
                    vy = 0
                    lance = False
                    pret_a_lancer = True

                if bouton_fertiliser.collidepoint(event.pos):
                    mini_jeu = "fertiliser"
                    engrais = []
                    rates = 0
                    spawn_timer = 0
                    panier.x = zone.centerx - 40

                if bouton_couper.collidepoint(event.pos):
                    mini_jeu = "couper"
                    herbes = []
                    spawn_timer_herbe = 0

                if mini_jeu == "arroser" and pret_a_lancer:
                    if zone.collidepoint(event.pos) and not lance:

                        souris_x, souris_y = event.pos
                        dx = souris_x - goutte_x
                        dy = souris_y - goutte_y
                        distance = math.sqrt(dx*dx + dy*dy)

                        if distance != 0:
                            vx = dx / distance * 10
                            vy = dy / distance * 10
                            lance = True

        fenetre.fill(VERT_FOND)

        dessiner_texte(fenetre, f"Score: {score}", font, BLANC, (20, 15))
        dessiner_texte(fenetre, f"Temps: {temps_restant}", font, BLANC, (20, 50))

        # Barre de progression
        progression = score / objectif
        dessiner_barre(fenetre, 20, 90, 200, 20, progression)

        dessiner_bouton(fenetre, bouton_menu, "Menu", font)
        dessiner_bouton(fenetre, bouton_arroser, "Arroser", font)
        dessiner_bouton(fenetre, bouton_fertiliser, "Fertiliser", font)
        dessiner_bouton(fenetre, bouton_couper, "Couper", font)


        pygame.draw.rect(fenetre, (200,200,200), zone)
        pygame.draw.rect(fenetre, (0,0,0), zone, 3)

        # =====================
        # 💧 ARROSER
        # =====================
        if mini_jeu == "arroser":

            if not lance and len(plantes) > 0:
                souris_x, souris_y = pygame.mouse.get_pos()
                souris_x = max(zone.left, min(zone.right, souris_x))
                souris_y = max(zone.top, min(zone.bottom, souris_y))

                dx = souris_x - goutte_x
                dy = souris_y - goutte_y
                distance = math.sqrt(dx*dx + dy*dy)

                if distance != 0:
                    vx_temp = dx / distance * 10
                    vy_temp = dy / distance * 10
                    dessiner_trajectoire(fenetre, goutte_x, goutte_y, vx_temp, vy_temp, zone)

            if lance:
                vy += 0.2
                goutte_x += vx
                goutte_y += vy

            pygame.draw.circle(fenetre, (0, 0, 255), (int(goutte_x), int(goutte_y)), 8)

            for i in range(len(plantes)):
                pygame.draw.rect(fenetre, (0,255,0), plantes[i])
                if plantes[i].collidepoint(goutte_x, goutte_y):
                    score += 10
                    plantes.pop(i)
                    break

            if len(plantes) == 0:
                if vague == 1:
                    vague = 2
                    plantes = creer_plantes(vague)

                    goutte_x = zone.left + 20
                    goutte_y = zone.centery
                    vx = 0
                    vy = 0
                    lance = False
                else:
                    mini_jeu = None
                    message_fin = "Plantes arrosees !"
                    temps_message = pygame.time.get_ticks()

            if not zone.collidepoint(goutte_x, goutte_y):
                goutte_x = zone.left + 20
                goutte_y = zone.centery
                vx = 0
                vy = 0
                lance = False

        # =====================
        # 🌱 FERTILISER
        # =====================
        if mini_jeu == "fertiliser":

            souris_x = pygame.mouse.get_pos()[0]
            panier.centerx = souris_x

            if panier.left < zone.left:
                panier.left = zone.left
            if panier.right > zone.right:
                panier.right = zone.right

            spawn_timer += 1
            if spawn_timer >= rate:
                spawn_timer = 0

                taille = 10
                x = random.randint(zone.left, zone.right - taille)
                engrais.append(pygame.Rect(x, zone.top, taille, taille))

            for e in engrais[:]:
                e.y += vitesse_engrais

                if e.colliderect(panier):
                    score += 5
                    engrais.remove(e)

                elif e.bottom >= zone.bottom:
                    engrais.remove(e)
                    rates += 1

            pygame.draw.rect(fenetre, (139, 69, 19), panier)

            for e in engrais:
                pygame.draw.rect(fenetre, (255, 255, 0), e)

            texte_rates = font.render(f"Rates: {rates}/{max_rates}", True, (0,0,0))
            fenetre.blit(texte_rates, (zone.left + 10, zone.top + 10))

            if rates >= max_rates:
                mini_jeu = None
                message_fin = "Fertilisation terminee !"
                temps_message = pygame.time.get_ticks()

        # =====================
        # 🌿 COUPER LES HERBES
        # =====================
        if mini_jeu == "couper":

            spawn_timer_herbe += 1
            if spawn_timer_herbe >= spawn_rate_herbe:
                spawn_timer_herbe = 0

                taille = 30
                x = random.randint(zone.left, zone.right - taille)
                y = random.randint(zone.top, zone.bottom - taille)

                herbes.append(pygame.Rect(x, y, taille, taille))

            for h in herbes:
                pygame.draw.rect(fenetre, (0, 100, 0), h)

            if pygame.mouse.get_pressed()[0]:
                souris = pygame.mouse.get_pos()
                for h in herbes[:]:
                    if h.collidepoint(souris):
                        herbes.remove(h)
                        score += 3

            if len(herbes) >= max_herbes:
                mini_jeu = None
                message_fin = "Trop de mauvaises herbes !"
                temps_message = pygame.time.get_ticks()

        # message
        if message_fin != "":
            texte = font.render(message_fin, True, (0,0,0))
            fenetre.blit(texte, (zone.centerx - 140, zone.centery))

            if pygame.time.get_ticks() - temps_message > 2000:
                message_fin = ""

        pygame.display.flip()
        clock.tick(60)

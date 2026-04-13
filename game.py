import pygame
import sys
import time
import math
import random

# Fonction qui permet d'écrire du texte sur la fenetre
def dessiner_texte(fenetre, texte, font, couleur, pos):
    # Affichage de l'ombre du texte
    ombre = font.render(texte, True, (30,30,30)) # On défini la police d'écriture
    fenetre.blit(ombre, (pos[0]+2, pos[1]+2)) # On affiche le texte sur la fenetre

    # Affichage du texte sur la fenetre (la partie qui n'a pas d'ombre)
    txt = font.render(texte, True, couleur)
    fenetre.blit(txt, pos)

# Fonction qui permet créer un nouveau bouton
def dessiner_bouton(fenetre, rect, texte, font):
    souris = pygame.mouse.get_pos() # Position de la souri

    couleur = (50,160,90)
    if rect.collidepoint(souris):
        couleur = (70,190,110)

    # Création de l'ombre du bouton
    ombre = rect.copy()
    ombre.y += 4
    pygame.draw.rect(fenetre, (30,30,30), ombre, border_radius=10)

    # Création du bouton
    pygame.draw.rect(fenetre, couleur, rect, border_radius=10)

    # Affichage du texte dans le rectangle
    txt = font.render(texte, True, (240,240,240))
    rect_txt = txt.get_rect(center=rect.center)
    fenetre.blit(txt, rect_txt)

#Fonction qui affiche la barre de score dans le jeu
def dessiner_barre(fenetre, x, y, largeur, hauteur, progression):
    pygame.draw.rect(fenetre, (200,200,200), (x, y, largeur, hauteur), border_radius=10)
    pygame.draw.rect(fenetre, (0, 200, 0), (x, y, largeur * progression, hauteur), border_radius=10)

# Fonction qui permet de dessiner la trajectoire dans lee jeu
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

# Fonction qui gére la partie jeu avec les mini jeux du projet
def jeu(fenetre, largeur, hauteur):
    # On défini des couleurs
    VERT_FOND = (34, 120, 60)
    BLANC = (240, 240, 240)

    clock = pygame.time.Clock()

    score = 0
    objectif = 100
    temps_max = 30
    debut = time.time()

    font = pygame.font.SysFont(None, 40)
    mini_jeu = None

    # boutton mini jeu
    bouton_arroser = pygame.Rect(50, hauteur - 80, 150, 50)
    bouton_fertiliser = pygame.Rect(250, hauteur - 80, 150, 50)
    bouton_couper = pygame.Rect(450, hauteur - 80, 200, 50)

    # bouton menu
    bouton_menu = pygame.Rect(largeur - 120, 20, 100, 40)

    zone = pygame.Rect(largeur//2 - 250, hauteur//2 - 150, 500, 300)

    # affichage de la goutte
    goutte_x = zone.left + 20
    goutte_y = zone.centery
    vx = 0
    vy = 0
    lance = False
    pret_a_lancer = False

    # affichage de l'engrais
    panier = pygame.Rect(zone.centerx - 40, zone.bottom - 30, 80, 20)
    engrais = []
    vitesse_engrais = 5
    spawn_timer = 0
    rate = 30
    rates = 0
    max_rates = 5

    # affichage des mauvaises herbes
    herbes = []
    spawn_timer_herbe = 0
    spawn_rate_herbe = 60
    max_herbes = 10

    vague = 1
    plantes = []

    # On dessine une plante pour un mini jeu
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
        # Vérification de la victoire ou defaite du joueur
        if score >= objectif:
            return "victoire"
        if temps_restant <= 0:
            return "game_over"

        # Gestion des evenements dans le jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Gestion de la souri
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if bouton_menu.collidepoint(event.pos):
                    return "menu"

                if bouton_arroser.collidepoint(event.pos):
                    # Lance le mini jeu
                    mini_jeu = "arroser"
                    vague = 1
                    plantes = creer_plantes(vague) # affichage de plante à arrosées

                    goutte_x = zone.left + 20
                    goutte_y = zone.centery
                    vx = 0
                    vy = 0
                    lance = False
                    pret_a_lancer = True # Affichage de la goutte d'eau

                if bouton_fertiliser.collidepoint(event.pos):
                    # Lance le mini jeu de fertilisation
                    mini_jeu = "fertiliser"
                    engrais = []
                    rates = 0
                    spawn_timer = 0
                    panier.x = zone.centerx - 40

                if bouton_couper.collidepoint(event.pos):
                    # Lance le troisième mini jeu
                    mini_jeu = "couper"
                    herbes = []
                    spawn_timer_herbe = 0

                if mini_jeu == "arroser" and pret_a_lancer:
                    if zone.collidepoint(event.pos) and not lance:
                        # Donne la position de la souri
                        souris_x, souris_y = event.pos
                        dx = souris_x - goutte_x
                        dy = souris_y - goutte_y
                        distance = math.sqrt(dx*dx + dy*dy)

                        if distance != 0:
                            vx = dx / distance * 10
                            vy = dy / distance * 10
                            lance = True

        fenetre.fill(VERT_FOND)

        # Affichage du texte
        dessiner_texte(fenetre, f"Score: {score}", font, BLANC, (20, 15))
        dessiner_texte(fenetre, f"Temps: {temps_restant}", font, BLANC, (20, 50))

        # Affichage de la barre de progression
        progression = score / objectif
        dessiner_barre(fenetre, 20, 90, 200, 20, progression)

        # Affichage de l'ensemble des boutons pour la fenetre de jeu
        dessiner_bouton(fenetre, bouton_menu, "Menu", font)
        dessiner_bouton(fenetre, bouton_arroser, "Arroser", font)
        dessiner_bouton(fenetre, bouton_fertiliser, "Fertiliser", font)
        dessiner_bouton(fenetre, bouton_couper, "Couper", font)


        pygame.draw.rect(fenetre, (200,200,200), zone)
        pygame.draw.rect(fenetre, (0,0,0), zone, 3)

        # Mini jeu arroser
        if mini_jeu == "arroser":
            if not lance and len(plantes) > 0:
                souris_x, souris_y = pygame.mouse.get_pos()
                # On limite la souri à la zone de jeu
                souris_x = max(zone.left, min(zone.right, souris_x))
                souris_y = max(zone.top, min(zone.bottom, souris_y))

                # On calcule la direction
                dx = souris_x - goutte_x
                dy = souris_y - goutte_y
                distance = math.sqrt(dx*dx + dy*dy)

                # On calcule la vitesse de la goutte
                if distance != 0:
                    vx_temp = dx / distance * 10
                    vy_temp = dy / distance * 10
                    dessiner_trajectoire(fenetre, goutte_x, goutte_y, vx_temp, vy_temp, zone)

            if lance:
                vy += 0.2
                goutte_x += vx
                goutte_y += vy

            # On affiche la goutte
            pygame.draw.circle(fenetre, (0, 0, 255), (int(goutte_x), int(goutte_y)), 8)

            # On cherche de collisions avec des plantes
            for i in range(len(plantes)):
                pygame.draw.rect(fenetre, (0,255,0), plantes[i])
                if plantes[i].collidepoint(goutte_x, goutte_y):
                    score += 10
                    plantes.pop(i)
                    break

            if len(plantes) == 0:
                # Lance une seconde vague du mini jeu
                if vague == 1:
                    vague = 2
                    plantes = creer_plantes(vague)

                    # On replace la goutte à sa position d'origine
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
                # On replace la goutte à sa position d'origine
                goutte_x = zone.left + 20
                goutte_y = zone.centery
                vx = 0
                vy = 0
                lance = False

        # Mini jeu fertiliser
        if mini_jeu == "fertiliser":
            # On déplace le panier avec la souris
            souris_x = pygame.mouse.get_pos()[0]
            panier.centerx = souris_x

            # On fait en sorte que le panier ne sort pas de la zone de jeu
            if panier.left < zone.left:
                panier.left = zone.left
            if panier.right > zone.right:
                panier.right = zone.right

            # Apparition d'un engrais dans la fenetre de jeu
            spawn_timer += 1
            if spawn_timer >= rate:
                spawn_timer = 0
                taille = 10
                x = random.randint(zone.left, zone.right - taille)
                engrais.append(pygame.Rect(x, zone.top, taille, taille))

            # Gestion de la chute de l'engrais
            for e in engrais[:]: # On parcour une copie de la liste pour ne pas faire d'erreur
                e.y += vitesse_engrais
                # En cas de colision
                if e.colliderect(panier):
                    score += 5
                    engrais.remove(e)
                # En cas de sortie de l'écran
                elif e.bottom >= zone.bottom:
                    engrais.remove(e)
                    rates += 1

            # On affiche le panier
            pygame.draw.rect(fenetre, (139, 69, 19), panier)

            # On affiche les engrais
            for e in engrais:
                pygame.draw.rect(fenetre, (255, 255, 0), e)

            # On affiche le nombre de vie qu'il nous reste avant de perdre le mini jeu
            texte_rates = font.render(f"Rates: {rates}/{max_rates}", True, (0,0,0))
            fenetre.blit(texte_rates, (zone.left + 10, zone.top + 10))

            if rates >= max_rates:
                mini_jeu = None
                message_fin = "Fertilisation terminee !"
                temps_message = pygame.time.get_ticks()

        # Mini jeu couper
        if mini_jeu == "couper":

            # On fais apparaitre une herbe sur l'écran
            spawn_timer_herbe += 1
            if spawn_timer_herbe >= spawn_rate_herbe:
                spawn_timer_herbe = 0

                taille = 30
                # On la fait apparaitre à une position aléatoire
                x = random.randint(zone.left, zone.right - taille)
                y = random.randint(zone.top, zone.bottom - taille)

                herbes.append(pygame.Rect(x, y, taille, taille))

            # On affiche toutes les herbes sur l'écran
            for h in herbes:
                pygame.draw.rect(fenetre, (0, 100, 0), h)

            # Gestion des clics de la souris
            if pygame.mouse.get_pressed()[0]:
                souris = pygame.mouse.get_pos()
                # Gestion de la suppression des herbes
                for h in herbes[:]: # On parcour une coupie de la liste pour ne pas provoquer d'erreur
                    if h.collidepoint(souris):
                        herbes.remove(h)
                        score += 3
            # Défaite si le joueur n'est pas assez rapide pour supprimer les mauvaises herbes
            if len(herbes) >= max_herbes:
                mini_jeu = None
                message_fin = "Trop de mauvaises herbes !"
                temps_message = pygame.time.get_ticks()

        # On affiche un message de fin
        if message_fin != "":
            texte = font.render(message_fin, True, (0,0,0))
            fenetre.blit(texte, (zone.centerx - 140, zone.centery))

            if pygame.time.get_ticks() - temps_message > 2000:
                message_fin = ""

        # On met à jour la fenetre
        pygame.display.flip()
        # Gestion des fps du jeu
        clock.tick(60)

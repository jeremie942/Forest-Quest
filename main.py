import pygame
import sys
from menu import afficher_menu, ecran_fin
from game import jeu
from codecarbon import EmissionsTracker

tracker = EmissionsTracker()
tracker.start()

try:

    pygame.init()

    # Initialisation de la fenetre
    largeur, hauteur = 800, 600
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Forest Quest")

    running = True
    etat = "menu" # Indique dans quelle fenetre le jeu est
    # Boucle principale de pycharm
    while running:

        fenetre.fill((0, 0, 0))

        # Gestion des états de l'écran pour passer du menu à la fenêtre de jeu
        if etat == "menu":
            # On récupère les boutons jouer et quitter pour pouvoir savoir quand le joueur appuis dessus
            bouton_jouer, bouton_quitter = afficher_menu(fenetre, largeur, hauteur)
        elif etat == "jeu":
            etat = jeu(fenetre, largeur, hauteur)
        elif etat == "victoire":
            bouton_rejouer, bouton_menu_btn = ecran_fin(fenetre, largeur, hauteur,"VICTOIRE !", (0, 255, 0))
        elif etat == "game_over":
            bouton_rejouer, bouton_menu_btn = ecran_fin(fenetre, largeur, hauteur,"GAME OVER", (255, 50, 50))

        # Mise à jour de la fenêtre
        pygame.display.flip()

        # Gestion des différents événement que le joueur peut faire
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Gestion de la souri
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Seulement si on est dans le menu du jeu
                if etat == "menu":
                    if bouton_jouer.collidepoint(event.pos): # Detection des collisions avec le bouton
                        etat = "jeu"
                    if bouton_quitter.collidepoint(event.pos): # Detection des collisions avec le bouton
                        running = False

                # Gestion des écran de fin de partie en cas de victoire ou de défaite
                elif etat in ["victoire", "game_over"]:
                    if bouton_rejouer.collidepoint(event.pos):
                        etat = "jeu"
                    if bouton_menu_btn.collidepoint(event.pos):
                        etat = "menu"

    pygame.quit()
    sys.exit()
finally:
    tracker.stop()
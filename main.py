import pygame
import sys
from affichage import *

pygame.init()

largeur = 1000
hauteur = 800

fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Forest Quest")

blanc = (255, 255, 255)

score_joueur = 0
score_final = 100

debut, duree = creer_chrono(1) # Initialisation du chronomètre

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fenetre.fill(blanc)

    # Partie carré (à modifier)
    pygame.draw.rect(fenetre, (0,0,255), (100, 100, 800, 500))
    pygame.draw.rect(fenetre, (255,0,0), (50,650, 100,100))
    pygame.draw.rect(fenetre, (255, 0, 0), (200, 650, 100, 100))

    # Partie texte
    fenetre.blit(score_texte(score_joueur, score_final), (20, 20))
    victoire(score_joueur, score_final) # vérifie si le joueur à atteint le bon score


    afficher_chrono(fenetre, debut, duree, 900, 20)
    chrono_fini(debut, duree) # Vérifie si le joueur à encore du temps

    # mise a jour de la fenetre
    pygame.display.flip()


pygame.quit()
sys.exit()
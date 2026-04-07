import pygame
import sys
from menu import afficher_menu
from game import jeu

pygame.init()

# Initialisation de la fenetre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Forest Quest")


# ======================
# 🎨 ÉCRAN FIN (victoire / game over)
# ======================
def ecran_fin(fenetre, largeur, hauteur, texte, couleur):

    souris = pygame.mouse.get_pos()

    # 🌿 fond
    fenetre.fill((34, 120, 60))

    # 🟫 overlay sombre
    overlay = pygame.Surface((largeur, hauteur))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))
    fenetre.blit(overlay, (0, 0))

    # 🔤 polices
    font_titre = pygame.font.SysFont("arial", 80, bold=True)
    font_bouton = pygame.font.SysFont("arial", 40)

    # ✨ texte avec ombre
    def texte_ombre(txt, font, couleur, center):
        # Texte principal
        rendu = font.render(txt, True, couleur)
        rect = rendu.get_rect(center=center)

        # Ombre (même base, juste décalée)
        ombre = font.render(txt, True, (0, 0, 0))
        rect_ombre = rect.copy()
        rect_ombre.x += 3
        rect_ombre.y += 3

        # Dessin
        fenetre.blit(ombre, rect_ombre)
        fenetre.blit(rendu, rect)

    texte_ombre(texte, font_titre, couleur, (largeur // 2, 200))

    # 🔘 boutons
    bouton_rejouer = pygame.Rect(largeur // 2 - 120, 320, 240, 70)
    bouton_menu = pygame.Rect(largeur // 2 - 120, 420, 240, 70)

    def dessiner_bouton(rect, txt):
        col = (50, 160, 90)
        if rect.collidepoint(souris):
            col = (70, 190, 110)

        # ombre
        ombre = rect.copy()
        ombre.y += 5
        pygame.draw.rect(fenetre, (0, 0, 0), ombre, border_radius=12)

        # bouton
        pygame.draw.rect(fenetre, col, rect, border_radius=12)

        # texte
        rendu = font_bouton.render(txt, True, (255, 255, 255))
        fenetre.blit(rendu, rendu.get_rect(center=rect.center))

    dessiner_bouton(bouton_rejouer, "Rejouer")
    dessiner_bouton(bouton_menu, "Menu")

    return bouton_rejouer, bouton_menu


# ======================
# 🔁 BOUCLE PRINCIPALE
# ======================

running = True
etat = "menu"

while running:

    fenetre.fill((0, 0, 0))

    # ======================
    # 🎮 ÉTATS
    # ======================
    if etat == "menu":
        bouton_jouer, bouton_quitter = afficher_menu(fenetre, largeur, hauteur)

    elif etat == "jeu":
        etat = jeu(fenetre, largeur, hauteur)

    elif etat == "victoire":
        bouton_rejouer, bouton_menu_btn = ecran_fin(
            fenetre, largeur, hauteur,
            "VICTOIRE !", (0, 255, 0)
        )

    elif etat == "game_over":
        bouton_rejouer, bouton_menu_btn = ecran_fin(
            fenetre, largeur, hauteur,
            "GAME OVER", (255, 50, 50)
        )

    pygame.display.flip()

    # ======================
    # 🖱️ ÉVÉNEMENTS
    # ======================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # MENU
            if etat == "menu":
                if bouton_jouer.collidepoint(event.pos):
                    etat = "jeu"

                if bouton_quitter.collidepoint(event.pos):
                    running = False

            # ÉCRANS FIN
            elif etat in ["victoire", "game_over"]:

                if bouton_rejouer.collidepoint(event.pos):
                    etat = "jeu"

                if bouton_menu_btn.collidepoint(event.pos):
                    etat = "menu"

pygame.quit()
sys.exit()
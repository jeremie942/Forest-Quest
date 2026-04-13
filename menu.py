import pygame

# On défini des couleurs principales
VERT_FOND = (34, 120, 60)
VERT_BOUTON = (50, 160, 90)
VERT_HOVER = (70, 190, 110)
BLANC = (240, 240, 240)
NOIR = (30, 30, 30)

# Fonction qui permet d'affiche du texte dans le menu du jeu
def dessiner_texte(fenetre, texte, font, couleur, center):
    # Affichage de l'ombre
    ombre = font.render(texte, True, NOIR)
    rect_ombre = ombre.get_rect(center=(center[0]+2, center[1]+2))
    fenetre.blit(ombre, rect_ombre)

    # Affichage du texte
    txt = font.render(texte, True, couleur)
    rect = txt.get_rect(center=center)
    fenetre.blit(txt, rect)

# Fonction qui permet d'affiche un boutton dans le menu du jeu
def dessiner_bouton(fenetre, rect, texte, font):
    souris = pygame.mouse.get_pos()

    # Gestion de la souris quand elle est sur le bouton
    couleur = VERT_BOUTON
    if rect.collidepoint(souris):
        couleur = VERT_HOVER

    # Affichage de l'ombre
    ombre = rect.copy()
    ombre.y += 5
    pygame.draw.rect(fenetre, NOIR, ombre, border_radius=12)

    # Affichage du bouton
    pygame.draw.rect(fenetre, couleur, rect, border_radius=12)

    # Affichage du texte dans le bouton
    dessiner_texte(fenetre, texte, font, BLANC, rect.center)

# Fonction qui affiche l'ensemble du menu du jeu
def afficher_menu(fenetre, largeur, hauteur):
    # Affichage d'un fond vert
    fenetre.fill(VERT_FOND)

    # On définit les polices d'écritures
    font_titre = pygame.font.SysFont("arial", 80, bold=True)
    font_bouton = pygame.font.SysFont("arial", 40)

    # On affiche le titre du jeu
    dessiner_texte(fenetre,"Forest Quest",font_titre,BLANC,(largeur // 2, 120))

    # On affiche les boutons jouer et quitter dans le menu
    bouton_jouer = pygame.Rect(largeur//2 - 120, 250, 240, 70)
    bouton_quitter = pygame.Rect(largeur//2 - 120, 350, 240, 70)
    dessiner_bouton(fenetre, bouton_jouer, "Jouer", font_bouton)
    dessiner_bouton(fenetre, bouton_quitter, "Quitter", font_bouton)

    # On renvoie les boutons pour gérer leurs événements
    return bouton_jouer, bouton_quitter

# Fonction qui permet d'affiche un écran de game over ou de victoire
def ecran_fin(fenetre, largeur, hauteur, texte, couleur):

    souris = pygame.mouse.get_pos()

    fenetre.fill((34, 120, 60))

    # On définit les variable pour l'écran de game over
    overlay = pygame.Surface((largeur, hauteur))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))
    fenetre.blit(overlay, (0, 0))

    # On définit les police d'écritures
    font_titre = pygame.font.SysFont("arial", 80, bold=True)
    font_bouton = pygame.font.SysFont("arial", 40)

    # Une fonction qui permet d'afficher le texte avec les ombres
    def texte_ombre(txt, font, couleur, center):
        # Affichage du texte principal
        rendu = font.render(txt, True, couleur)
        rect = rendu.get_rect(center=center)

        # Affichage de l'ombre du texte principal
        ombre = font.render(txt, True, (0, 0, 0))
        rect_ombre = rect.copy()
        rect_ombre.x += 3
        rect_ombre.y += 3

        # On dessine dans la fenetre de jeu
        fenetre.blit(ombre, rect_ombre)
        fenetre.blit(rendu, rect)

    texte_ombre(texte, font_titre, couleur, (largeur // 2, 200))

    # On créer un bouton rejouer et menu
    bouton_rejouer = pygame.Rect(largeur // 2 - 120, 320, 240, 70)
    bouton_menu = pygame.Rect(largeur // 2 - 120, 420, 240, 70)

    # Fonction qui permet de créer un bouton
    def dessiner_bouton(rect, txt):
        col = (50, 160, 90)
        if rect.collidepoint(souris):
            col = (70, 190, 110)

        # Affichage de l'ombre du bouton
        ombre = rect.copy()
        ombre.y += 5
        pygame.draw.rect(fenetre, (0, 0, 0), ombre, border_radius=12)

        # Affichage du bouton
        pygame.draw.rect(fenetre, col, rect, border_radius=12)

        # Affichage du texte du bouton
        rendu = font_bouton.render(txt, True, (255, 255, 255))
        fenetre.blit(rendu, rendu.get_rect(center=rect.center))

    dessiner_bouton(bouton_rejouer, "Rejouer")
    dessiner_bouton(bouton_menu, "Menu")

    return bouton_rejouer, bouton_menu

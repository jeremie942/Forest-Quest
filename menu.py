import pygame

# 🎨 Couleurs modernes
VERT_FOND = (34, 120, 60)
VERT_BOUTON = (50, 160, 90)
VERT_HOVER = (70, 190, 110)
BLANC = (240, 240, 240)
NOIR = (30, 30, 30)


def dessiner_texte(fenetre, texte, font, couleur, center):
    # Ombre
    ombre = font.render(texte, True, NOIR)
    rect_ombre = ombre.get_rect(center=(center[0]+2, center[1]+2))
    fenetre.blit(ombre, rect_ombre)

    # Texte principal
    txt = font.render(texte, True, couleur)
    rect = txt.get_rect(center=center)
    fenetre.blit(txt, rect)


def dessiner_bouton(fenetre, rect, texte, font):
    souris = pygame.mouse.get_pos()

    # Hover
    couleur = VERT_BOUTON
    if rect.collidepoint(souris):
        couleur = VERT_HOVER

    # Ombre
    ombre = rect.copy()
    ombre.y += 5
    pygame.draw.rect(fenetre, NOIR, ombre, border_radius=12)

    # Bouton
    pygame.draw.rect(fenetre, couleur, rect, border_radius=12)

    # Texte
    dessiner_texte(fenetre, texte, font, BLANC, rect.center)


def afficher_menu(fenetre, largeur, hauteur):
    fenetre.fill(VERT_FOND)

    # Polices
    font_titre = pygame.font.SysFont("arial", 80, bold=True)
    font_bouton = pygame.font.SysFont("arial", 40)

    # Titre
    dessiner_texte(
        fenetre,
        "Forest Quest",
        font_titre,
        BLANC,
        (largeur // 2, 120)
    )

    # Boutons
    bouton_jouer = pygame.Rect(largeur//2 - 120, 250, 240, 70)
    bouton_quitter = pygame.Rect(largeur//2 - 120, 350, 240, 70)

    dessiner_bouton(fenetre, bouton_jouer, "Jouer", font_bouton)
    dessiner_bouton(fenetre, bouton_quitter, "Quitter", font_bouton)

    return bouton_jouer, bouton_quitter
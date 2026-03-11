import pygame

def score_texte(score_joueur, score_final):
    font = pygame.font.SysFont(None, 30)
    return font.render("Score : {}/{}".format(score_joueur, score_final), True, (0,0,0))

def creer_chrono(minutes):
    debut = pygame.time.get_ticks()
    duree = minutes * 60
    return debut, duree

def afficher_chrono(fenetre, debut, duree, x, y):
    font = pygame.font.SysFont(None, 30)
    temps_ecoule = (pygame.time.get_ticks() - debut) // 1000
    temps_restant = max(0, duree - temps_ecoule)

    minutes = temps_restant // 60
    secondes = temps_restant % 60

    chrono = f"{minutes:02}:{secondes:02}"

    texte = font.render(chrono, True, (0,0,0))
    fenetre.blit(texte, (x, y))



def victoire(score_joueur, score_final):
    if score_joueur >= score_final:
        print("Victoire du joueur")

def chrono_fini(debut, duree):
    temps_ecoule = (pygame.time.get_ticks() - debut) // 1000
    if temps_ecoule >= duree:
        print("Fin plus de temps")
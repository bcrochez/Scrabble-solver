# -*-coding:Latin-1 -*
from iutk import *

cptCharg = 0

# affiche une lettre avec (x,y) comme coin en haut à gauche
def afficheLettre(x, y, lettre):
    rectanglePlein(x+1, y+1, x+39, y+39, "#EFF382")
    texteCentre(x+20, y+20, lettre, "black")

# initialise l'interface
def initInterface():
    rectanglePlein(0, 0, 1200, 700, "dark green")
    rectangle(800, 0, 1199, 699)
    rectangleCouleur(801, 1, 1198, 698, "grey")
    miseAJour()

# affiche le score total
def afficheScoreTot(score):
    rectanglePlein(10, 620, 300, 650+hauteurTexte("A"), "dark green")
    rectangleCouleur(10, 620, 12+longueurTexte("Score total:        "+str(score)), 650+hauteurTexte("A"), "red")
    rectangleCouleur(11, 621, 11+longueurTexte("Score total:        "+str(score)), 649+hauteurTexte("A"), "dark red")
    texte(25, 635, "Score total: "+str(score), "black")
    miseAJour()

# affiche le menu
def afficheMenu():
    afficheBouton(850, 30, 1150, 90, "Faire un nouveau tirage")  
    afficheBouton(850, 120, 1150, 180, "Faire un tirage à la main")
    afficheBouton(850, 210, 1150, 270, "Trouver le meilleur coup") 
    afficheBouton(850, 300, 1150, 360, "Réinitialiser le jeu")
    afficheBouton(850, 390, 1150, 450, "Charger un plateau")
    afficheBouton(850, 480, 1150, 540, "Sauvegarder le plateau")
    afficheBouton(850, 570, 1150, 630, "Quitter")

# affiche un bouton avec le texte avec comme coin supérieur gauche (x1, x2) et coin inférieur droit (y1, y2)
def afficheBouton(x1, x2, y1, y2, texte):
    rectanglePlein(x1, x2, y1, y2, "yellow")
    rectangle(x1, x2, y1, y2)
    rectangleCouleur(x1+1, x2+1, y1-1, y2-1, "grey")
    texteCentre(x1+(y1-x1)/2, x2+(y2-x2)/2, texte, "black")
    miseAJour()
    
# affiche le tirage
def afficheTirage(tirage):
    rectanglePlein(620, 20, 700+42, 20+15*42, "dark green") # on masque les tirages précédents
    texte(620, 20, "Tirage:", "black");
    i = 0
    for lettre in tirage:
        afficheLettre(700, 20+i, lettre);
        i += 42
    miseAJour();
    
# affiche un mot et son score
def afficheCoup(mot, score):
    rectanglePlein(50, 150, 799, 190+42, "dark green") # on masque les coups précédents
    texte(50, 150, "Meilleur coup:", "black")
    texte(50+longueurTexte("Meilleur coup:")+30, 150, "Score: "+str(score), "black")
    i = 0
    for lettre in mot:
        afficheLettre(50+i, 190, lettre)
        i += 42
    miseAJour()

# affiche le plateau
def affichePlateau(plateau, plateauBonus):
    rectangle(0, 0, 604, 604)
    rectangleCouleur(1, 1, 603, 603, "grey")
    rectanglePlein(2, 2, 602, 602, "dark green")
    i = 0
    j = 0
    while i < 15:
        while j < 15:
            rectangle(i*40+2, j*40+2, i*40+40+2, j*40+40+2)	# met la case 
            if plateauBonus[i][j] == "lct":
                rectanglePlein(i*40+3, j*40+3, i*40+40+1, j*40+40+1, "dark blue")	# lettre compte triple
            elif plateauBonus[i][j] == "lcd":
                rectanglePlein(i*40+3, j*40+3, i*40+40+1, j*40+40+1, "cyan")        # lettre compte double
            elif plateauBonus[i][j] == "mcd":
                rectanglePlein(i*40+3, j*40+3, i*40+40+1, j*40+40+1, "pink")        # mot compte double
            elif plateauBonus[i][j] == "mct":
                rectanglePlein(i*40+3, j*40+3, i*40+40+1, j*40+40+1, "red")         # mot compte triple
            elif type(plateau[i][j]) == str :
                afficheLettre(i*40+2, j*40+2, plateau[i][j])	# affiche lettre
            j += 1
        j = 0
        i += 1
    miseAJour()


# affiche un chargement
def chargement():
    rectanglePlein(0, 0, 1200, 700, "dark green")
    afficheBouton(450, 300, 750, 400, "Chargement ...")
    miseAJour()

# -*-coding:Latin-1 -*
from scrabble import *
from graphique import *
from time import *
				
creeFenetre(1200,700)

choix =""
lettres = {}
tirage = []
plateau = []
nbLettres = 0
scoreTotal = 0
lettres, nbLettres, plateau = initScrabble()
plateauBonus = initPlateauBonus()
chargement()
print(clock())
fichier = open("../ODS6.txt", "r")
contenu = fichier.readlines()
dictionnaire = initDico(contenu)
fichier.close()
print(clock())

initInterface()
affichePlateau(plateau, plateauBonus)
x = 0
y = 0

while choix != "quitter":
	afficheMenu()
	afficheScoreTot(scoreTotal)
	x, y = clic()
	if (x >= 850 and x <= 1150) and (y >= 30 and y <= 90):
		if nbLettres > 0:
			lettres, nbLettres, tirage = tirageAlea(lettres, nbLettres, tirage)
		afficheTirage(tirage)
	if (x >= 850 and x <= 1150) and (y >= 120 and y <= 180):
		tirage = tirageMan(tirage)
		afficheTirage(tirage)
	if (x >= 850 and x <= 1150) and (y >= 210 and y <= 270):
		print("debut algo:", clock())
		scoreTotal = meilleurCoupAlgo(lettres, plateau, tirage, dictionnaire, scoreTotal, plateauBonus)
		print("fin algo:", clock())
		affichePlateau(plateau, plateauBonus)
		afficheTirage(tirage)
	if (x >= 850 and x <= 1150) and (y >= 300 and y <= 360):
		lettres, nbLettres, plateau = initScrabble()
		plateauBonus = initPlateauBonus()
		tirage = []
		scoreTotal = 0
		affichePlateau(plateau, plateauBonus)
		afficheTirage(tirage)
	if (x >= 850 and x <= 1150) and (y >= 390 and y <= 450):
		lettres, nbLettres, plateau = initScrabble()
		plateauBonus = initPlateauBonus()
		name = input(">Entrez le nom du fichier: ")
		try:
			fichier = open(name, "r")
		except:
			print("Ce fichier n'existe pas!")
			continue
		contenu = fichier.readlines()
		plateau, plateauBonus = loadPlateau(contenu, plateauBonus)
		tirage = []
		scoreTotal = 0
		affichePlateau(plateau, plateauBonus)
		afficheTirage(tirage)
		fichier.close()
	if (x >= 850 and x <= 1150) and (y >= 480 and y <= 540):
		name = input(">Entrez le nom de la sauvegarde: ")
		fichier = open(name, "w")
		savePlateau(plateau, fichier)
		fichier.close()
	if (x >= 850 and x <= 1150) and (y >= 570 and y <= 630):
		choix = "quitter"

fermeFenetre()

exit()

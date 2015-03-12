# -*-coding:Latin-1 -*

from random import *
from graphique import *


scoreMaxGlob = 0		# 
motMaxGlob = ""			#
iMaxGlob = 7			# variable globale pour stocker le meilleur coup courant
jMaxGlob = 7			#
sensGlob = "horizontal"	#
usedLetter = 0
listeMotGlob = []
seed(a=10)

# Initialise le sac
def initScrabble():
	lettres = {}
	lettres[1] = ['A', 9, 1]
	lettres[2] = ['B', 2, 3]
	lettres[3] = ['C', 2, 3]
	lettres[4] = ['D', 3, 2]
	lettres[5] = ['E', 15, 1]
	lettres[6] = ['F', 2, 4]
	lettres[7] = ['G', 2, 2]
	lettres[8] = ['H', 2, 4]
	lettres[9] = ['I', 8, 1]
	lettres[10] = ['J', 1, 8]
	lettres[11] = ['K', 1, 10]
	lettres[12] = ['L', 5, 1]
	lettres[13] = ['M', 3, 2]
	lettres[14] = ['N', 6, 1]
	lettres[15] = ['O', 6, 1]
	lettres[16] = ['P', 2, 3]
	lettres[17] = ['Q', 1, 8]
	lettres[18] = ['R', 6, 1]
	lettres[19] = ['S', 6, 1]
	lettres[20] = ['T', 6, 1]
	lettres[21] = ['U', 6, 1]
	lettres[22] = ['V', 2, 4]
	lettres[23] = ['W', 1, 10]
	lettres[24] = ['X', 1, 10]
	lettres[25] = ['Y', 1, 10]
	lettres[26] = ['Z', 1, 10]
	
	i = 0
	nbLettres = 0
	while i < 26:
		nbLettres += lettres[1+i][1]
		i += 1
	
	plateau = initPlateau()
	return lettres, nbLettres, plateau

# initialisation du plateau
def initPlateau():
	plateau = []
	i = 0
	j = 0
	while i < 15:	# 15 listes de 15 (plateau 15x15)
		tmp = []
		while j < 15:
			tmp.append(-1)
			j += 1
		plateau.append(tmp)
		j = 0
		i += 1
	return plateau

def loadPlateau(fichier, plateauBonus):
	plateau = initPlateau()
	i=0
	j=0
	for line in fichier:
		for letter in line:
			if letter == '\n' or letter == ' ':
				continue
			elif letter == '_':
				plateau[i][j] = -1
			else:
				plateau[i][j] = letter
				plateauBonus[i][j] = -1
			i+=1
		i=0
		j+=1
	return plateau, plateauBonus

def savePlateau(plateau, fichier):
	i=0
	j=0
	while j<15:
		while i<15:
			if plateau[i][j] == -1:
				fichier.write('_')
			else:
				fichier.write(plateau[i][j])
			i+=1
		if j != 14:
			fichier.write("\n")
		i=0
		j+=1

def initPlateauBonus():
	plateau = initPlateau()
	i = 0
	j = 0
	while i < 15:
		while j < 15:
			if (i == 1 or i == 5 or i == 9 or i == 13) and (j == 1 or j == 5 or j == 9 or j == 13):
				plateau[i][j] = "lct"	# lettre compte triple
			elif ((i == 6 or i == 8) and (j == 2 or j == 12)) or ((i == 2 or i == 12) and (j == 6 or j == 8)):
				plateau[i][j] = "lcd"	#lettre compte double
			elif ((i == 3 or i == 11) and j == 7) or ((j == 3 or j == 11) and i == 7):
				plateau[i][j] = "lcd"	#lettre compte double
			elif ((j == 0 or j == 14) and (i == 3 or i == 11)) or ((i == 0 or i == 14) and (j == 3 or j == 11)):
				plateau[i][j] = "lcd"	#lettre compte double
			elif (i == 0 or i == 7 or i == 14) and (j == 0 or j == 7 or j == 14):
				plateau[i][j] = "mct"	# mot compte triple dans les coins et millieu extérieur
			if i == j or i == 14-j:	# rempli les diagonales
				if i == 5 or i == 9:
					plateau[i][j] = "lct"	# lettre compte triple
				elif i == 6 or i == 8:
					plateau[i][j] = "lcd"	# lettre compte double
				elif i == 0 or i == 14 or j == 0 or j ==14:
					plateau[i][j] = "mct"		# mot compte triple
				else:
					plateau[i][j] = "mcd"	# mot compte double
			j += 1
		j = 0
		i += 1
	return plateau

# Effectue un tirage manuel // ne marche pas en graphique
def tirageMan(tirage):
	string = input("Rentrez votre tirage (seulement des lettres sans accent, les 15 premières lettres seront gardées \net les autres caractères ne seront pas pris en compte) :\n>")
	i = 0
	for a in string:
		if i >= 15:
			return tirage
		if a in "abcdefghijklmnopqrstuvwxyz" or a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			tirage.append(a.upper())
			i += 1
		else:
			continue
	return tirage

# Effectue un tirage aléatoire
def tirageAlea(lettres, nbLettres, tirage, nb = 7):
	cpt = 0
	i = len(tirage)
	while i < nb and nbLettres > 0:
		cpt = randrange(nbLettres)
		j = 0
		while j < 26:
			if lettres[1+j][1] == 0: 	# s'il n'y a plus de lettre[1+j] on passe à la suivante
				j += 1
				continue
			elif cpt <= lettres[1+j][1]: 	# si le compteur est inférieur au nombre de cette lettre
				tirage.append(lettres[1+j][0]) 	# on la prend
				lettres[1+j][1] -= 1  	# et on décrémente son nombre
				nbLettres -= 1
				i += 1
				break
			else:		#sinon on passe à la lettre suivante et on retire au compteur le nombre de lettres qu'on a passé
				cpt -= lettres[1+j][1]
				j += 1
	return lettres, nbLettres, tirage

#initialisation du dictionnaire en utilisant un arbre préfixe
def initDico(fichier):
	racine = dict()
	for mot in fichier:
		dicoCourant = racine
		for lettre in mot:
			if lettre != '\n' :
				dicoCourant = dicoCourant.setdefault(lettre, {})
		dicoCourant = dicoCourant.setdefault('_fin_', '_fin_')
	return racine


# détermine la liste de tout les mots accepté par le tirage (en théorie)	
def motAccepte(tirage, dictionnaire, mot, liste):
	tirageTmp = tirage
	for etat in dictionnaire:													# pour chaque etat/lettre du dictionnaire courant
		motTmp = mot
		if etat in tirageTmp:													# s'il est dans le tirage
			motTmp += etat														# on l'ajoute au mot
			tirageTmp.remove(etat)												# on retire la lettre du tirage
			liste = motAccepte(tirageTmp, dictionnaire[etat], motTmp, liste)	# on ajoute a la liste tout les mots acceptés à partir du dictionnaire
			tirageTmp.append(etat)												# on remet la lettre dans le tirage et on passe à la suivante
		if etat == "_fin_":														# si c'est un mot accepté on l'ajoute à la liste
			liste.append(mot)		
	return liste

# teste si un mot est gardable
def legalMove(mot, i, j, plateau, lettres, sens, plateauBonus):
	global scoreMaxGlob
	global motMaxGlob
	global iMaxGlob
	global jMaxGlob
	global sensGlob
	global listeMotGlob
	global usedLetter
	scoreTmp = scoreMot(mot, lettres, i, j, plateau, plateauBonus)
	if scoreTmp > scoreMaxGlob:			# si le score du mot est plus grand que le score du précédent on le garde
		if i-len(mot) >= 0 and usedLetter > 0:
			listeMotGlob = []
			scoreMaxGlob = scoreTmp
			listeMotGlob.append((mot, i, j, sens))
			#motMaxGlob = mot
			#iMaxGlob = i
			#jMaxGlob = j
			#sensGlob = sens
	elif scoreTmp == scoreMaxGlob and usedLetter > 0:
		listeMotGlob.append((mot, i, j, sens))


def forceBrute(plateau, tirage, dictionnaire, lettres, plateauBonus, sens, liste, crossCheck):
	global usedLetter
	j = 0
	while j <= 14:
		listeMot = []
		i = 0
		while i <= 14:   # ajout des lettres de la ligne
			if plateau[i][j] != -1:
				tirage.append(plateau[i][j])
			i += 1
		listeMot = motAccepte(tirage, dictionnaire, "", listeMot) # liste des mots acceptés
		i = 0
		while i <= 14:
			if plateau[i][j] != -1:
				tirage.remove(plateau[i][j])   # retire les lettres de la ligne
			i += 1
		i = 0
		while i <= 14:
			for mot in listeMot:
				listeUsed = []
				nbA = 0
				ok = 1
				usedLetter = 0
				if i+len(mot) > 15:
					continue
				if i == 0 or (i != 0 and plateau[i-1][j] == -1):
					k = i
					for lettre in mot:
						if (plateau[k][j] == -1 and lettre in crossCheck[k][j] and lettre in tirage) or (plateau[k][j] != -1 and lettre == plateau[k][j]):
							if plateau[k][j] == -1 and lettre in tirage:
								tirage.remove(lettre)
								listeUsed.append(lettre)
								usedLetter += 1
							if (k, j) in liste:
								nbA += 1
							k += 1
							continue
						else:
							ok = 0
							break
				if ok == 1 and nbA > 0 and (k > 14 or plateau[k][j] == -1):
					legalMove(mot, k-1, j, plateau, lettres, sens, plateauBonus)
				for lettre in listeUsed:
					tirage.append(lettre)
			i += 1
		j += 1

			
# trouve le meilleur coup à partir d'un tirage et d'un plateau
def meilleurCoupAlgo(lettres, plateau, tirage, dictionnaire, scoreTotal, plateauBonus):
	global scoreMaxGlob
	global motMaxGlob
	global iMaxGlob
	global jMaxGlob
	global sensGlob
	global listeMotGlob
	global usedLetter
	listeMot = []
	liste = listOfAnchor(plateau)		# on calcule la liste des ancres
	transP = transposePlateau(plateau)	# la transposée du plateau
	transL = listOfAnchor(transP)		# la transposée des ancres
	crossCheckV = crossChecking(plateau, dictionnaire, liste)	# les cross check vertical et horizontal
	crossCheckH = crossChecking(transP, dictionnaire, transL)
	if len(liste) == 0:		# s'il n'y a pas d'ancre c'est le premier coup (7, 7)
		listeMot = motAccepte(tirage, dictionnaire, "", listeMot)
		i = 14
		while i >= 7 :
			for mot in listeMot:
				usedLetter = 0
				if i-len(mot) < 7:
					usedLetter = len(mot)
					legalMove(mot, i, 7, plateau, lettres, "horizontal", plateauBonus)
			i -= 1
		j = 7
		while j <= 14:
			for mot in listeMot:
				usedLetter = 0
				if j-len(mot) < 7:
					usedLetter = len(mot)
					legalMove(mot, j, 7, transP, lettres, "vertical", transposePlateau(plateauBonus))
			j += 1
	else:
		forceBrute(plateau, tirage, dictionnaire, lettres, plateauBonus, "horizontal", liste, crossCheckV)
		forceBrute(transP, tirage, dictionnaire, lettres, transposePlateau(plateauBonus), "vertical", transL, crossCheckH)
					
	print(listeMotGlob)
	if len(listeMotGlob) != 0 :
		motMaxGlob = listeMotGlob[0][0]
		iMaxGlob = listeMotGlob[0][1]
		jMaxGlob = listeMotGlob[0][2]
		sensGlob = listeMotGlob[0][3]
		for uplet in listeMotGlob:
			if uplet[0] < motMaxGlob:
				motMaxGlob = uplet[0]
				iMaxGlob = uplet[1]
				jMaxGlob = uplet[2]
				sensGlob = uplet[3]
		print(iMaxGlob, jMaxGlob, motMaxGlob, sensGlob, scoreMaxGlob, usedLetter)
		k = len(motMaxGlob)-1
		if sensGlob == "horizontal":						# selon le sens du mot on l'ajoute au plateau avec (iMax, jMax) la case vide à droite du mot
			for lettre in motMaxGlob:						
				if plateau[iMaxGlob-k][jMaxGlob] == -1:
					for lettreT in tirage:
						if lettre == lettreT:
							tirage.remove(lettre)
							break
					plateau[iMaxGlob-k][jMaxGlob] = lettre
					plateauBonus[iMaxGlob-k][jMaxGlob] = -1
				k -= 1
		elif sensGlob == "vertical":
			for lettre in motMaxGlob:
				if plateau[jMaxGlob][iMaxGlob-k] == -1:
					for lettreT in tirage:
						if lettre == lettreT:
							tirage.remove(lettre)
							break
					plateau[jMaxGlob][iMaxGlob-k] = lettre
					plateauBonus[jMaxGlob][iMaxGlob-k] = -1
				k -= 1
		scoreTotal += scoreMaxGlob
	scoreMaxGlob = 0
	listeMotGlob = []
	motMaxGlob = ""
	return scoreTotal
	
# détermine la liste des ancres		
def listOfAnchor(plateau):
	liste =[]
	i = 0
	while i < 15:
		j = 0
		while j < 15:
			if plateau[i][j] != -1:						# si la case contient une lettre
				if j != 0 and plateau[i][j-1] == -1 and (i, j-1) not in liste:	# si la case au dessus est vide c'est une ancre
					liste.append((i, j-1))
				if j != 14 and plateau[i][j+1] == -1 and (i, j+1) not in liste:	# si la case en dessous est vide, ancre
					liste.append((i, j+1))
				if i != 14 and plateau[i+1][j] == -1 and (i+1, j) not in liste:	# si la case à droite est vide, ancre
					liste.append((i+1, j))
				if i != 0 and plateau[i-1][j] == -1 and (i-1, j) not in liste:	# si la case à gauche est vide, ancre
					liste.append((i-1, j))
			j += 1
		i += 1
	return liste

# calcule le score d'un mot
def scoreMot(mot, lettres, i, j, plateau, plateauBonus):
	global usedLetter
	score = 0
	scoreAdj = 0
	iTmp = i-len(mot)+1
	jTmp = 0
	k = 0
	multMot = 1
	while iTmp <= i:
		if plateau[iTmp][j] == -1:
			multMotAdj = 1
			scoreMotAdj = 0
			if plateauBonus[iTmp][j] == "lct":
				score += lettres[ord(mot[k])-64][2]*3			# lettre compte triple
				scoreMotAdj += lettres[ord(mot[k])-64][2]*3
			elif plateauBonus[iTmp][j] == "lcd":
				score += lettres[ord(mot[k])-64][2]*2        # lettre compte double
				scoreMotAdj += lettres[ord(mot[k])-64][2]*2
			elif plateauBonus[iTmp][j] == "mcd":
				multMot *= 2        # mot compte double
				multMotAdj *= 2
				score += lettres[ord(mot[k])-64][2]
				scoreMotAdj += lettres[ord(mot[k])-64][2]
			elif plateauBonus[iTmp][j] == "mct":
				multMot *= 3         # mot compte triple
				multMotAdj *= 3
				score += lettres[ord(mot[k])-64][2]
				scoreMotAdj += lettres[ord(mot[k])-64][2]
			else:
				score += lettres[ord(mot[k])-64][2]
				scoreMotAdj += lettres[ord(mot[k])-64][2]
			tailleMotAdj = 0
			jTmp = j+1
			while jTmp <= 14 and plateau[iTmp][jTmp] != -1:
				scoreMotAdj += lettres[ord(plateau[iTmp][jTmp])-64][2]
				tailleMotAdj += 1
				jTmp += 1
			jTmp = j-1
			while jTmp >= 0 and plateau[iTmp][jTmp] != -1:
				scoreMotAdj += lettres[ord(plateau[iTmp][jTmp])-64][2]
				tailleMotAdj += 1
				jTmp -= 1
			scoreMotAdj *= multMotAdj
			if tailleMotAdj > 0:
				scoreAdj += scoreMotAdj
		if plateau[iTmp][j] != -1:
			score += lettres[ord(plateau[iTmp][j])-64][2]
		iTmp += 1
		k += 1
	score = score*multMot
	if usedLetter == 7:
		print(usedLetter, mot, i, j)
		score += 50
	score += scoreAdj
	return score

# transpose un plateau
def transposePlateau(plateau):
	trans = initPlateau()
	i = 0
	while i < 15:
		j = 0
		while j < 15:
			trans[i][j] = plateau[j][i]
			j += 1
		i += 1
	return trans

# transpose une liste d'ancres
def transposeAnchor(liste):
	trans = []
	for couple in liste:
		trans.append((couple[1], couple[0]))
	return trans

# détermine le cross check des cases du plateau
def crossChecking(plateau, dictionnaire, listeA):
	crossCheck = initPlateau()
	dicoCourant = dictionnaire
	i = 0
	while i < 15:
		j = 0
		while j < 15:			# initialise toutes les cases avec la liste de toutes les autres
			crossCheck[i][j] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
			j += 1
		i += 1
	for couple in listeA:			# si la case est une ancre on met une liste vide
		dicoCourant = dictionnaire
		crossCheck[couple[0]][couple[1]] = []
		x = couple[1]-1
		while x >= 0 and plateau[couple[0]][x] != -1:
			x -= 1
		x += 1
		while x < couple[1]:
			dicoCourant = dicoCourant[plateau[couple[0]][x]]
			x += 1
		for e in dicoCourant:
			if ((couple[1] < 14 and plateau[couple[0]][couple[1]+1] == -1) or couple[1] == 14) and '_fin_' in dicoCourant[e]:
				crossCheck[couple[0]][couple[1]].append(e)
			elif couple[1] < 14 and plateau[couple[0]][couple[1]+1] != -1:
				x = couple[1]+1
				dicoCourant2 = dicoCourant[e]
				while x <= 14 and plateau[couple[0]][x] != -1 and plateau[couple[0]][x] in dicoCourant2:
					dicoCourant2 = dicoCourant2[plateau[couple[0]][x]]
					x += 1
				if x > 14 or plateau[couple[0]][x] == -1:
					if '_fin_' in dicoCourant2:
							crossCheck[couple[0]][couple[1]].append(e)
		if (couple[1] == 14 or (couple[1] != 14 and plateau[couple[0]][couple[1]+1] == -1)) and (couple[1] == 0 or (couple[1] !=0 and plateau[couple[0]][couple[1]-1] == -1)):
			crossCheck[couple[0]][couple[1]] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	return crossCheck
	
# calcule la limite à gauche d'une ancre en (i, j)
def limitOfAnchor(i, j, listeA, plateau):
	k = 0
	cpt = i-1
	while (cpt, j) not in listeA and cpt >= 0 and plateau[cpt][j] == -1: 	# tant qu'on a pas atteint le bord du plateau, 
		cpt -= 1															# qu'on a pas rencontré une autre ancre ou une lettre // A CHANGER
		k += 1																# on incrémente le compteur 
	return k

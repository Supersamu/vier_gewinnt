import numpy as np

print(np.random.random())

"""

import numpy
list1 = []
b = 7
h = 6
for i in range(0,b*h):
	list1.append(1) #leer
	list1.append(0) #kugel spieler1
	list1.append(0)	#kugel spieler2

def zeigspielstand(liste,b,h): #liste ist der aktuelle spielstand
	for i in range(h,0,-1):
		liste1 = []
		for j in range(0,3*b):
			if liste[(i-1)*3*b+j] == 1:
				liste1.append(j%3)
		print(liste1)

def checkiflegalmove(liste,position,b,h):
	if position >= b: return False
	if liste[(h-1)*3*b+position*3] == 1: 
		return True
	return False

def makemove(liste,position,b,h,spielernr): #liste ist der aktuelle spielstand, position ist welche spaltenzahl(nummeriert von 0 bis b-1) die kugel reinkommt, spielernr ist 1 oder 2, je nachdem welcher spieler dran ist
	for i in range(0,h):
		if liste[i*3*b+position*3] == 1: #i*3*b: es gibt 3*b fächer pro zeile
			liste[i*3*b+position*3] = 0
			liste[i*3*b+position*3+spielernr] = 1
			break
	return liste

def checkliste(liste):#Liste von nullen und einsen, überprüfen, ob 4 einsen in einer reihe da sind
	test = 0
	for i in range(0,len(liste)-3):
		test = 1
		for j in range(0,4):
			test = test*liste[i+j]
		if test == 1: return True
	return False
		

def checkifwin(liste,b,h):#liste ist der aktuelle spielstand
	list1 = []
	list2 = []
	for i in range(0,3*b*h):
		if i%3 == 1: #Spieler1
			list1.append(liste[i])# einsen, falls spieler 1 kugeln da hat, nullen sonst
		if i%3 == 2: #Spieler2
			list2.append(liste[i])# einsen, falls spieler 2 kugeln da hat, nullen sonst

	for i in range (0,b-3): #zeilen überprüfen; i ist spaltennummer
		for j in range (0, h): #j ist zeilennumer
			liste1 = []
			liste2 = []
			for k in range(0,4): #vier in einer reihe
				liste1.append(list1[j*b+i+k])
				liste2.append(list2[j*b+i+k])
			if checkliste(liste1): return 1
			if checkliste(liste2): return 2

	for j in range (0,h-3): #spaltenweise überprüfen j ist zeilennumer
		for i in range (0, b):
			liste1 = []
			liste2 = []
			for k in range(0,4):
				liste1.append(list1[j*b+i+k*b])
				liste2.append(list2[j*b+i+k*b])
			if checkliste(liste1): return 1
			if checkliste(liste2): return 2

	for j in range(3,h): #diagonalen nach rechts unten, j ist zeilennumer
		for i in range(0,b-3): # i ist spaltennumer
			liste1 = []
			liste2 = []
			for k in range(0,4):
				liste1.append(list1[j*b+i-k*(b-1)])
				liste2.append(list2[j*b+i-k*(b-1)])
			if checkliste(liste1): return 1
			if checkliste(liste2): return 2

	for j in range(0,h-3): #diagonalen nach rechts oben, j ist zeilennumer
		for i in range(0,b-3): # i ist spaltennumer
			liste1 = []
			liste2 = []
			for k in range(0,4):
				liste1.append(list1[j*b+i+k*(b+1)])
				liste2.append(list1[j*b+i+k*(b+1)])
			if checkliste(liste1): return 1
			if checkliste(liste2): return 2
	return 0




zeigspielstand(list1,b,h)
ergebnis = checkifwin(list1,b,h)
j = 0
while ergebnis == 0:
	print("\n")
	if j%2 == 0:
		x = int(input("Spieler 1 ist an der Reihe, in welche Spalte wollen sie setzen? "))
		print("\n")
		if checkiflegalmove(list1,x-1,b,h):
			list1 = makemove(list1,x-1,b,h,1)
		else:
			print("Illegaler Zug")
			print("Spieler 2 hat gewonnen")
			ergebnis = 2
			break
	if j%2 == 1:
		x = int(input("Spieler 2 ist an der Reihe, in welche Spalte wollen sie setzen? "))
		if checkiflegalmove(list1,x-1,b,h):
			list1 = makemove(list1,x-1,b,h,2)
		else:
			print("Illegaler Zug")
			print("Spieler 1 hat gewonnen")
			ergebnis = 1
			break
	j += 1
	print("Dies ist der neue Spielstand:")
	print("\n")
	zeigspielstand(list1,b,h)
	ergebnis = checkifwin(list1,b,h)
	if ergebnis == 1:
		print("Spieler 1 hat gewonnen")
		break
	if ergebnis == 2:
		print("Spieler 2 hat gewonnen")
		break
	if j == 42:
		print("Das Spiel ist unentschieden")
		break
"""

#
#	MIKKO KOIVULA
#

import time
lista = list()
jarjestyslista = []		# Lista reiteistä korkeuden mukaan (ascending)
kaupungit = []			# VAKIO - Lista kaupungeista
kaupungit2 = []			# Muokattava kaupunkien kopio
reittilista = []		# Lista minimum span treen 
liitoslista = []
groups = []

yhdistelma = []			# Forestin haarautuvien puiden oma 2 ulotteinen lista
visited = []			# Kaupungit, joissa käyty jo

def main():
	with open("graph_ADS2018_70.txt") as data:
		k, tiet = [int(x) for x in next(data).split()] 		# Ensimmäiseltä riviltä 
		
		for line in data:
			line = line.rstrip('\n')
			lista.append([int(x) for x in line.split()])
		
		kohde = lista.pop()									# Listan viimeinen arvo on kohdekaupunki, eli otetaan se talteen

	jarjestyslista = sorted(lista, key=lambda y: y[-1])		# Laitetaan Annettu reittilista järjestykseen

	jaljella = []											# Pienten puiden jälkeen jääneiden reittien lista

	kaupungit = jarjestakaupungit(jarjestyslista)			# Kopioidaan kaupungit
	kaupungit2 = jarjestakaupungit(jarjestyslista)

	etsireitti(jarjestyslista, kaupungit2)					# Funktio, joka luo pikkupuita myöhemmin luotavaa Minimal Span Tree:tä varten
	yhdistaja(reittilista)									# Yhdistetään pikkupuiden reitit omiksi listoiksi (esim [1,3] ja [1,5] muunnetaan: [1, 3, 5])

	for i in jarjestyslista:
		if i not in reittilista:
			jaljella.append(i)

	ryhmat = reittilista + minimumspanningtree(jarjestyslista, jaljella)
	reitit = sorted(ryhmat, key=lambda y: y[-1])
	
	minimumspanningtree(jarjestyslista, jaljella)			# Yhdistetään kahta polkua yhdistävän polun avulla reittipari yhteen
	pienin_polku = doyouknowtheway(kohde, reitit)			# Pienin reitti
	
	if pienin_polku:
		korkeus = pienin_polku.pop()
		print(f"Pienin reitti: {pienin_polku}, korkein kohta: {korkeus}")
	else:
		print("Polkua ei löytynyt")

def jarjestakaupungit(jarjestyslista):						# Irroitetaan reiteistä kaikki kaupungit omaan listaansa
	for i in jarjestyslista:
		if i[0] not in kaupungit:
			kaupungit.append(i[0])
		if i[1] not in kaupungit:
			kaupungit.append(i[1])
	kaupungit.sort()

	return kaupungit


def etsireitti(jarjestyslista, kaupungit2):					# Funktio, joka luo pikkupuita myöhemmin luotavaa Minimal Span Tree:tä varten
	liitoslista = []
	
	for j in jarjestyslista:								# Luodaan alku minimum search treetä varten
		if ((j[0] in kaupungit2) and (j[1] in kaupungit2)):
			reittilista.append(j)
			kaupungit2.remove(j[1])


	for k in reittilista:
		for v in reittilista:
			if k[0] == v[1]:
				reittilista.remove(v) 						# Poistetaan huonot reitit
	for i in reittilista:
		if i[0] not in liitoslista:
			liitoslista.append(i)

	kaupungit2 = jarjestakaupungit(jarjestyslista)

def yhdistaja(lista):										# Yhdistetään pikkupuiden reitit omiksi listoiksi (esim [1,3] ja [1,5] muunnetaan: [1, 3, 5])
	k = 0
	for i in lista:
		if i[0] not in visited:

			yhdistelma.append([])
			visited.append(i[0])

			yhdistelma[k].append(i[0])
			yhdistelma[k].append(i[1])
			
			for num, j in enumerate(lista, start=0):
				if (j[0] == i[0]) and (j[1] != i[1]):
					yhdistelma[k].append(j[1])

			k = k + 1
	yhdistelma.sort()
	return yhdistelma


def minimumspanningtree(jarjestyslista, jaljella):			# Yhdistetään kahta polkua yhdistävän polun avulla reittipari yhteen
	k = 0
	for i in jaljella:
		for j in yhdistelma:
			if i[0] in j and i[1] not in j: 				# Tutkitaan, että onko reitin alku ja loppu samassa polussa. Jos ei, niin pienin yhdistävä reitti on i

				yhdistava = i
				groups.append(yhdistava)
				union(yhdistava, yhdistelma)
	return groups

def union(yhdistava, yhdistelma):							
	for i in yhdistelma:

		if yhdistava[0] in i:
			yhdistettava1 = i
		if yhdistava[1] in i:
			yhdistettava2 = i

	yhdistetty = yhdistettava1 + yhdistettava2
	yhdistelma.remove(yhdistettava1)
	yhdistelma.remove(yhdistettava2)
	yhdistelma.append(yhdistetty)

def doyouknowtheway(kohde, reitit):							# Varsinainen reitinhaku -funktio.
	laskuri = 0
	alku = [[1]]
	reitit2 = reitit[:]
	for i in reitit:
		if i[0] == 1:
			alku.append([1])
			alku[laskuri].append(i[1])
			alku[laskuri].append(i[2])
			reitit2.remove(i)

			laskuri = laskuri + 1

	alku.pop()
	for a in alku:
		for b in reitit:
			reitti = a[:]
			if a[-2] == b[0] and b[1] not in a:
				reitti.insert(-1, b[1])
				if b[-1] > reitti[-1]:
					reitti[-1] = b[-1]
				alku.append(reitti)
			elif a[-2] == b[1] and b[0] not in a:
				reitti.insert(-1, b[0])
				if b[-1] > reitti[-1]:
					reitti[-1] = b[-1]
				alku.append(reitti)
	for a in alku:
		if a[0] == 1 and a[-2] == kohde[0]:
			return a
	return False


start = time.perf_counter()

main()

stop = time.perf_counter()

print("aika: ", stop - start)






"""
⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠶⣿⣭⡧⡤⣤⣻⣛⣹⣿⣿⣿⣶⣄
⢀⢀⢀⢀⢀⢀⢀⢀⢀⣼⣊⣤⣶⣷⣶⣧⣤⣽⣿⣿⣿⣿⣿⣿⣷
⢀⢀⢀⢀⢀⢀⢀⢀⢀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⢀⢀⢀⢀⢀⢀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⢀⢀⢀⢀⢀⢀⠸⠿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣻⣿⣿⣿⣿⣿⡆
⢀⢀⢀⢀⢀⢀⢀⢸⣿⣿⡀⠘⣿⡿⢿⣿⣿⡟⣾⣿⣯⣽⣼⣿⣿⣿⣿⡀
⢀⢀⢀⢀⢀⢀⡠⠚⢛⣛⣃⢄⡁⢀⢀⢀⠈⠁⠛⠛⠛⠛⠚⠻⣿⣿⣿⣷
⢀⢀⣴⣶⣶⣶⣷⡄⠊⠉⢻⣟⠃⢀⢀⢀⢀⡠⠔⠒⢀⢀⢀⢀⢹⣿⣿⣿⣄⣀⣀⣀⣀⣀⣀
⢠⣾⣿⣿⣿⣿⣿⣿⣿⣶⣄⣙⠻⠿⠶⠒⠁⢀⢀⣀⣤⣰⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄
⢿⠟⠛⠋⣿⣿⣿⣿⣿⣿⣿⣟⡿⠷⣶⣶⣶⢶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⢀⢀⢀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠙⠻⠿⣿⣿⡿
⢀⢀⢀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⢀⢀⢀⠈⠁
⢀⢀⢀⢀⢸⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢀⢀⢀⢀⢸⣿⣿⣿⣿⣄⠈⠛⠿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣹⣿⣿⣿⣿⣿⣿⣿⣿⠇
⢀⢀⢀⢀⢀⢻⣿⣿⣿⣿⣧⣀⢀⢀⠉⠛⠛⠋⠉⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⠏
⢀⢀⢀⢀⢀⢀⢻⣿⣿⣿⣿⣿⣷⣤⣄⣀⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋
⢀⢀⢀⢀⢀⢀⢀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛
⢀⢀⢀⢀⢀⢀⢀⢀⢀⢹⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁
⢀⢀⢀⢀⢀⢀⢀⢀⢀⢸⣿⡇⢀⠈⠙⠛⠛⠛⠛⠛⠛⠻⣿⣿⣿⠇
⢀⢀⢀⢀⢀⢀⢀⢀⢀⣸⣿⡇⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢨⣿⣿
⢀⢀⢀⢀⢀⢀⢀⢀⣾⣿⡿⠃⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢸⣿⡏
⢀⢀⢀⢀⢀⢀⢀⢀⠻⠿⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢠⣿⣿⡇

"""
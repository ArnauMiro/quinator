#!/bin/env python
#
# Generador de cartrons per una quina musical
#
# Arnau Miro (2022)
from __future__ import print_function, division

import os, numpy as np, time
import matplotlib, matplotlib.pyplot as plt

# Fitxers
FITXER_LLISTA = 'llistat cançons - Llista.csv'
FITXER_EXTRA  = 'llistat cançons - Extres.csv'
CARPETA_DESTI = 'CARTRONS'
FIGURES       = ['angel','bou','caganer','gallina','mula','nen_jesus','ovella','pastor','pixaner','rentadora']
FONT          = 'Hey Comic'

# Dimensions del cartro
Npersones = 160 # nombre total de jugadors
nr        = 3   # nombre de files
nc        = 4   # nombre de columnes
nt        = nr*nc

# Programes extra
CONVERT  = 'convert'
PDFUNITE = 'pdfunite' 

def printCartro(name,l,mapa):
	'''
	Fancy print :)
	'''
	print("Cartro: %s"%name)
	for ii in range(l.shape[0]):
		for jj in range(l.shape[1]):
			#print(" %d"%l[ii,jj],end=' ')
			print(" %s"%mapa[l[ii,jj]],end=' ')
		print("")

def crearCartro(name,back,l,mapa,inici=[920.,1150],delta=[970.,710],wrap=400.,dpi=3000):
	'''
	Crea un cartro a partir de la plantilla
	'''
	# Primer converteixo el pdf a png
	os.system('%s -quality 100 -density %d %s front.png'%(CONVERT,dpi,os.path.join('PLANTILLA','bingo.pdf')))
	os.system('%s -quality 100 -density %d %s back.png'%(CONVERT,dpi,os.path.join('PLANTILLA','%s.pdf'%back)))
	img = plt.imread('front.png')
	# Crear la figura
	fig = plt.figure(figsize=(1.54,1.09),dpi=dpi)
	ax  = plt.axes((0,0,1,1),frame_on=False)
	ax.axis('off')
	# Posa la imatge de fons
	ax.imshow(img)
	# Escribim el text de les cancons en els quadrats
	for ii in range(l.shape[0]):
		for jj in range(l.shape[1]):
			text = ax.text(inici[0]+delta[0]*jj,inici[1]+delta[1]*ii,mapa[l[ii,jj]],fontsize=3.0,font=FONT,ha='center', va='center',wrap=True)
			text._get_wrap_line_width = lambda : wrap
	# Guardem i convertim a pdf
	plt.savefig('front.png',dpi=dpi,bbox_inches=None)
	plt.close()
	# Finalment ho ajuntem i ho posem als cartrons generals
	os.makedirs(CARPETA_DESTI,exist_ok=True)
	os.system('%s -quality 100 front.png back.png %s'%(CONVERT,os.path.join(CARPETA_DESTI,"%s.pdf"%(name))))

# Afegim la font
matplotlib.font_manager.fontManager.addfont('./%s.ttf'%FONT)

# Carregar les llistes i generar els diccionaris
# que mapejen els nombres amb els noms de les
# cancons. Assumim que les 12 primeres cancons
# de la llista 1 no estaran a la llista 2
llista = np.genfromtxt(FITXER_LLISTA,dtype=str,skip_header=1,delimiter=',')
llista_ordre   = llista[:,0].astype(int)
llista_cancons = llista[:,1]
# Reordenar les cancons segons l'ordre de la llista
iordre = np.argsort(llista_ordre)
llista_ordre   = llista_ordre[iordre]
llista_cancons = llista_cancons[iordre]
# Fem el mateix per la llista d'extra de cancons, no cal reordenar
llista = np.genfromtxt(FITXER_EXTRA,dtype=str,skip_header=1,delimiter=',')
llista_extra = llista[:,1]

N1 = len(llista_cancons) # Nombre de cancons en la llista per les linies
N2 = N1 - nt             # Nombre de cancons en la llista pel bingo en blanc (pot ser un subset de la N1)
N3 = len(llista_extra)   # Nombre de cancons en la llista de cancons que no apareixen

# Ara generem un diccionari per convertir els nombres
# en les canciones
num2str = {}
for icanco,canco in enumerate(llista_cancons):
	num2str[icanco+1] = canco
# I ara hi afegim les cancons extres
for icanco,canco in enumerate(llista_extra):
	num2str[icanco+N1+1] = canco

# Crear l'objecte generador de nombres aleatoris
g = np.random.default_rng( int(time.time()) ) # Usar la data com a seed

# 1: cartro bingo en blanc
# Ha de contenir les 12 primeres cancons de la 
# llista 1. ALERTA: no haurien de ser les primeres
# a sonar
l_nuvis = g.choice(np.arange(1,nt+1),size=(nr,nc),replace=False)
# Trec un nombre entre nr i nt de cancons
# que no apareixen a la llista
l_nollista = g.choice(np.arange(N1+1,N1+N3),size=(g.integers(low=1,high=nt),),replace=False).tolist()
# Coloco les cancons a la llista
while len(l_nollista) > 0:
	# Trio una posicio per linia i columna
	p_lin = g.choice(nr,size=(1,),replace=False)[0]
	p_col = g.choice(nc,size=(1,),replace=False)[0]
	# Faig el canvi i elimino de la llista
	l_nuvis[p_lin,p_col] = l_nollista.pop(0)
printCartro("nuvis",l_nuvis,num2str)
crearCartro("nuvis","nuvis",l_nuvis,num2str)

# 2: cartons guanyadors de linies
# Generar una combinacio guanyadora
# Poden fer qualsevol de les 3 linies
l_linia1 = g.choice(np.arange(nt+1,N1),size=(nr,nc),replace=False)
l_linia2 = g.choice(np.arange(nt+1,N1),size=(nr,nc),replace=False)
printCartro("linia1",l_linia1,num2str)
crearCartro("linia1","base",l_linia1,num2str)
printCartro("linia2",l_linia2,num2str)
crearCartro("linia2","base",l_linia2,num2str)

# 3: cartrons no guanyadors
# Trec els 2 guanyadors de linies i no
# hi considero els nuvis
for ii in range(1,Npersones-2+1): 
	# Genero com un cartro guanyador
	l_res = g.choice(np.arange(nt+1,N1),size=(nr,nc),replace=False)
	# Trec un nombre entre nr i nt-min(nc,nr) de cancons
	# que no apareixen a la llista
	# N'ha d'apareixer alguna si no pot guanyar el bingo en blanc!
	l_nollista = g.choice(np.arange(N1+1,N1+N3),size=(g.integers(low=nr,high=nt-min(nc,nr)),),replace=False).tolist()
	# Canvio almenys 1 canco per linia
	for jj in range(nr):
		# Trio una posicio per columna
		p_col = g.choice(nc,size=(1,),replace=False)[0]
		# Trio una canco de la llista que no apareix
		p_can = g.choice(len(l_nollista),size=(1,),replace=False)[0]
		# Faig el canvi i elimino de la llista
		l_res[jj,p_col] = l_nollista.pop(p_can)
	# Encara pot ser que ens quedin cancons a colocar
	while len(l_nollista) > 0:
		# Trio una posicio per linia i columna
		p_lin = g.choice(nr,size=(1,),replace=False)[0]
		p_col = g.choice(nc,size=(1,),replace=False)[0]
		# Miro si realment puc fer el canvi
		# es a dir el seu numero esta per sota o
		# igual a N1
		if l_res[p_lin,p_col] > N1: continue
		# Faig el canvi i elimino de la llista
		l_res[p_lin,p_col] = l_nollista.pop(0)
	printCartro("no guanyador %d"%ii,l_res,num2str)
	crearCartro("no_guanyador_%d"%ii,FIGURES.pop(0) if len(FIGURES) > 0 else "base",l_res,num2str)

# Ajunta-ho tot en un sol PDF
os.system('%s %s cartrons.pdf'%(PDFUNITE,os.path.join(CARPETA_DESTI,'*.pdf')))
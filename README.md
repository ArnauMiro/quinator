# Quinator Musical

Petit codi Python per generar cartrons a partir d'unes plantilles per fer una quina (bingo) musical.

## Requeriments

Pensat per usuaris de Linux i possiblement IOS, així que bye bye Windows. Almenys jo no el suporto. Es requereixen els següents paquets:
- Python 3
- convert que forma part de ImageMagick
- pdfunite que forma part de Poppler

### Paquets de Python
- os
- numpy
- time
- matplotlib

## Funcionament del joc

El joc està pensat per fer 2 linies i un bingo en blanc. Només hi ha un cartró que pugui guanyar el bingo en blanc i dos cartrons que poden guanyar les linies. La resta de cartrons no poden guanyar cap joc, tot i que participen.

### Primer joc: les 2 primeres linies

Les dues primeres linies es fan com una quina normal. Sonen cançons i els jugadors han d'anar marcant les que van sonant. Guanya linia el primer jugador que es capaç de marcar una linia sencera amb les cançons que han sonat. Un cop s'ha cantant una linia el joc segueix fins a que es canta una segona linia, amb les mateixes condicions que la primera.

### Segon joc: el bingo en blanc

Per anar a pel bingo el joc canvia. Primerament es treuen totes les marques i tots els jugadors s'aixequen. Van sonant cançons i els jugadors s'asseuen a mesura que sonen cançons que tenen al cartró. Finalment guanya el jugador que es queda de peu i tothom està sentat.

## Funcionament del programa

El programa està pensat per funcionar amb dues llistes:
```python
FITXER_LLISTA = 'llistat cançons - Llista.csv'
FITXER_EXTRA  = 'llistat cançons - Extres.csv'
```
El *FITXER_LLISTA* conté les cançons que sonaran durant la quina on les 12 primeres (assumint un cartro de 3x4) no sonaran al bingo en blanc. El fitxer *FITXER_EXTRA* conté cançons per omplir buits i que no sonaràn mai. El joc esta pensat per generar 
```python
Npersones = 160 # nombre total de jugadors
```
cartrons d'on un guanya el bingo en blanc i dos guanyen linies. La resta contenen cançons extra col·locades tal que mai poden guanyar cap dels dos jocs. Els cartrons s'esperen de 
```python
nr = 3 # nombre de files
nc = 4 # nombre de columnes
```
El programa agafa les plantilles de quina de davant i darrere de la carpeta **PLANTILLES**. La variable
```python
FIGURES = ['angel','bou','caganer','gallina','mula','nen_jesus','ovella','pastor','pixaner','rentadora']
```
Controla el tipus de dorsos que hi han a part del dors *base.pdf*. El frontal es diu *bingo.pdf*. Les plantilles es poden canviar, es recomana seguir la mateixa distribució i dimensions, si no s'haurà d'ajustar els paràmetres de la funció
```python
crearCartro(name,back,l,mapa,inici=[920.,1150],delta=[970.,710],wrap=400.,dpi=3000)
```
*inici*, *delta* i *wrap* per tal d'acomodar la nova plantilla. Un bon programa per generar plantilles és [canva](https://www.canva.com/en_gb/). La font es pot canviar amb la variable
```python
FONT = 'Hey Comic'
```
i ha de ser una font tipus *ttf*. Es poden trobar fonts a [DaFont](https://www.dafont.com/es/). Els programes extra es poden setejar a 
```python
# Programes extra
CONVERT  = 'convert'
PDFUNITE = 'pdfunite' 
```
El programa **convert** es fa servir per generar *png* dels *pdf* de les plantilles i *pdf* dels *png* un cop escrits pel Python. El programa **pdfunite** ajunta tots els cartrons que s'hauran generat a
```python
CARPETA_DESTI = 'CARTRONS'
```
en un sol document per tal de que sigui més fàcil d'imprimir.

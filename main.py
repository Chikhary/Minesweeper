### Section HTML

'''
Ce programme a pout but de reproduire, à l'aide du language HTML et du
language de programmation python, le célèbre jeu démineur. Le programme
et l'affichage sont conçus dans la même page et le jeu répond aux mêmes
règles que le jeu original

Conception:
Les différents paramètres du code sont générés par des sous-fonctions et
l'affichage du code est maintenu par le css et les appels aux fonctions
inner.HTML et document.querySelector modifient le css pour afficher les
différentes étapes du jeu.
'''

### Section HTML
# Initialisation du css

css = """
      <style>
          #main table {
              border: 1px solid black;
              margin: 10px;
          }
          #main table td {
              width: 30px;
              height: 30px;
              border: none;
          }
      </style>
      """

# Tableau regroupant le code des images affichées dans le jeu
images = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "blank",
          "flag", "mine", "mine-red", "mine-red-x"]


# Fonction reprise du code du tic tac toe vue en classe et prend en fonction
# un tableau et un numéro d'index et retourne le terme affiché à l'index de ce
# tableau.
def afficherTuile(tab, index):
    return tab[index]


'''
Cette fonction prend en compte 5 paramètres, la position en x, la position
en y ainsi que la hauteur, l'index, un tableau et le nombre de mines voulues
dans le jeu.Cette fonction crée la ligne HTML pour que l'affichage HTML
concorde avec le nombre de cases par ligne.La fonction prend aussi en compte
la case appuyée par la souris sur le clavier et enregistre dans une fonction
antérieure la démarche à appliquer après l'appui.
'''


def genererRangeeHTML(largeur, y, hauteur, index, nbMines):
    rangees = []
    lien = "\"http://codeboot.org/images/minesweeper/"
    for i in range(largeur * y, largeur * (y + 1)):
        # numéro de la tuile en question
        id = "tuile" + str(i)

        # image affichée pour chaque tuile
        image = afficherTuile(images, index) + ".png\" "

        # Ajout du "onclick" ainsi que de l'option "event.shiftKey
        # pour donner une seconde option au joueur expliquée plus tard
        onclick = "onclick=\"clic(" + str(i % largeur) + "," + \
                  str(y) + "," + "event.shiftKey" + "," + str(largeur) + \
                  "," + str(hauteur) + "," + str(nbMines) + ")\""

        # Remplissage du tableau vide "rangees" par les balises construites
        # avec les variables plus tôt
        rangees.append("<td id=\"" + id + "\" " + onclick +
                       "><img src=" + lien + image + "></td>")

    # Ajout des balises propres à HTML
    return "<tr>" + '\n'.join(rangees) + "</tr>"


'''
Cette fonction prend en compte 3 paramètres, qui sont la largeur, la hauteur,
ainsi que le nombre de mines voulues dans le jeu.Cette fonction rappelle la
fonction genererRangeeHTML et rallonge le code sur la hauteur de la grille pour
que toutes les tuiles aient leur balise.
'''


def genererGrilleHTML(largeur, hauteur, nbMines):
    rangees = []

    for i in range(hauteur):
        rangees.append(genererRangeeHTML(largeur,
                                         i, hauteur, 9, nbMines))  # index 9 pour init() == "blank"
    # Ajout des balises propres à HTML
    return "<table>" + '\n'.join(rangees) + "</table>"


# Fonction prenant comme paramètre un nombre n et retourne un chiffre entier
# entre 0 et n.

def randint(n):
    return int(n * random())


"""
Cette fonction prend en paramètre un tableau et retourne un tableau ayant les
mêmes termes, mais dans un ordre aléatoire.Cette fonction est reprise des 
notes de cours du cours de structures et tableaux.
"""


def shuffle(tab):
    for i in range(len(tab) - 1, 0, -1):
        j = randint(i)
        t = tab[i]
        tab[i] = tab[j]
        tab[j] = t
    return tab


"""
Cette fonction prend 3 paramètres en compte, une variable x, une variable y
et une variable largeur et retourne le multiple de y et la largeur additionné
à x.
"""


def index(x, y, largeur):
    return y * largeur + x


"""
Cette fonction prend en compte 2 paramètres, la longueur et la largeur.
Elle retourne une matrice avec les longueurs et les largeurs choisies avec
des cases contenant uniquement "False".
"""


def minesInit(largeur, hauteur):
    global mines

    mines = [0] * hauteur

    for y in range(hauteur):
        mines[y] = [False] * largeur

    return mines


"""
Cette fonction prend 4 paramètres en facteur. Elle prend en facteur la 
largeur, la hauteur, le nombre de mines ainsi que les variables de position 
x et y.Cette fonction permet de placer de façon aléatoire les mines dans le
"""


def placerMines(largeur, hauteur, nbMines, x, y):
    n = largeur * hauteur  # nombres de cases

    random = shuffle(list(range(n - 1)))  # n-1 car le premier clic est entré
    # et on lance le programme avec n-1
    # cases

    i = index(x, y, largeur)

    if i < len(random):
        # On deplace (x, y) a la fin de la liste aleatoire
        random.append(random[i])
        random[i] = n - 1

    else:
        random.append(n - 1)

    mines = [0] * hauteur
    for y in range(hauteur):
        mines[y] = [0] * largeur
        for x in range(largeur):
            i = index(x, y, largeur)
            # True or False, s'il y a une mine?
            mines[y][x] = random[i] < nbMines
    return mines


"""
Cette fonction prend en compte 2 paramètres, la longueur et la largeur.
Elle retourne une matrice avec les longueurs et les largeurs choisies avec
des cases contenant uniquement "False".Cette fonction, contrairement à
mineInit, n'utilise pas la variable globale mines.
"""


def grilleBooleenne(largeur, hauteur):
    grille = [0] * hauteur
    for i in range(hauteur):
        grille[i] = [False] * largeur
    return grille


"""
Cette fonction calcule le nombre de mines voisines à partir de la position en
x et en y de la mine. Cette fonction prend aussi en compte le nombre de
cases à vérifier dépendant de la position de la case. Par exemple, il n'y
a que 3 cases à vérifier pour la tuile en bas à droite alors que pour une mine
au milieu, il y a 8 cases à vérifier.
"""


def nbMinesVoisines(x, y, mines):
    compteur = 0
    for dy in range(-1, 2):
        j = y + dy
        if j >= 0 and j < len(mines):
            for dx in range(-1, 2):
                i = x + dx
                if i >= 0 and i < len(mines[0]):
                    compteur += mines[j][i]
    return compteur


"""
Cette procedure ne fait qu'ouvrir une seule case, elle est uniquement appelee 
lorsque la tuile cliquee par le joueur possede au moins une mine comme voisin. 
"""


def openOneCase(x, y, mines, drapeaux, devoilees, largeur):
    if drapeaux[y][x] or devoilees[y][x]:  # verifie si la tuile est deja
        # connu par le joueur
        pass
    else:
        tuile = nbMinesVoisines(x, y, mines)  # Pour identifier la tuile
        mettreAJourHTML(afficherTuile(images, tuile), x, y, largeur)
        devoilees[y][x] = True  # Change la valeur dans la grille booleenne


"""
Cette procedure permet d'ouvrir toutes les cases autour de la tuile cliquee par
le joueur(donc elle n'a pas de mines voisines). Toutefois, il peut arriver que
ses tuiles voisines ne contiennent, elles aussi, aucunes mines voisines. 
Dans ce cas, on fait appelle a une recursion pour analyser cette nouvelle 
tuile. Au moment qu'une tuile possede au moins une mine voisine, la recursion 
est terminale.
"""


def open(x, y, mines, drapeaux, devoilees, largeur):
    if drapeaux[y][x] or devoilees[y][x]:
        pass
    else:
        tuile = nbMinesVoisines(x, y, mines)
        if tuile == 0:
            analyse(x, y, mines, drapeaux, devoilees, largeur)  # recursion
        else:
            mettreAJourHTML(afficherTuile(images, tuile), x, y, largeur)
            devoilees[y][x] = True


'''
Cette fonction prend en compte 4 paramètres. Elle prend en compte une tuile,
la position de la tuile en x et y ainsi que la largeur de la grille. Cette
fonction met à jour le code HTML en haut pendant que le jeu est lancé.
'''


def mettreAJourHTML(tuile, x, y, largeur):
    id = str(index(x, y, largeur))
    update = document.querySelector('#tuile' + id)
    update.innerHTML = '<img src="http://codeboot.org/images/minesweeper/' + \
                       tuile + ".png\">"


"""
Cette fonction permet de verifier le nombre de tuile devoilees. Elle est
essentielle car le joueur gagne si toutes les tuiles devoilees ne sont pas
des mines.
"""


def checkOpened(devoilees, largeur, hauteur):
    compteur = 0
    for y in range(hauteur):
        for x in range(largeur):
            if devoilees[y][x] == True:
                compteur += 1
            else:
                continue
    return compteur


"""
Cette fonction permet au joueur de jouer au jeu. Elle est appelee lorsque le 
joueur interagit dans l'interface par un clic. Elle s'occupe de creer le jeu,
verifier l'etat du joueur et retourne la victoire ou la defaite du joueur.
Elle doit prendre en parametre '(x,y)' pour connaitre la position de la tuile,
'evenement' pour traiter l'etat du clic, 'largeur, hauteur' pour connaitre les
dimensions du jeu afin de bien positionner les mines et les tuiles et 'nbMines'
afin de placer le nombre de mines souhaitees par le joueur.
"""


def clic(x, y, evenement, largeur, hauteur, nbMines):
    global nbDevoilees, mines, devoilees, drapeaux
    if not devoilees[y][x]:
        if evenement:  # Drapeau
            d = not drapeaux[y][x]
            drapeaux[y][x] = d
            mettreAJourHTML(afficherTuile(images, 10 if d else 9),
                            x, y, largeur)
        elif not drapeaux[y][x]:
            if nbDevoilees == 0:  # premier clic car aucune case devoilee
                mines = placerMines(largeur, hauteur, nbMines, x, y)  # pose de
                # mines
            else:
                if mines[y][x]:  # clic sur une mine
                    for yy in range(hauteur):
                        for xx in range(largeur):
                            if not devoilees[yy][xx]:
                                if mines[yy][xx] != drapeaux[yy][xx]:
                                    if mines[yy][xx]:
                                        if x == xx and y == yy:
                                            tuile = 12  # images[12]
                                        else:
                                            tuile = 11  # images[11]
                                    else:
                                        tuile = 13  # images[13]
                                    mettreAJourHTML(afficherTuile(images,
                                                                  tuile), xx,
                                                    yy, largeur)
                    sleep(0.1)  # rafraichir l'écran pour le joueur
                    alert('Vous avez perdu :(')
                    return fin(largeur, hauteur, nbMines)

            analyse(x, y, mines, drapeaux, devoilees, largeur)
            nbDevoilees = checkOpened(devoilees, largeur, hauteur)
            if largeur * hauteur == nbDevoilees + nbMines:  # toutes les tuiles
                for yy in range(hauteur):
                    for xx in range(largeur):
                        if not devoilees[yy][xx] and not drapeaux[yy][xx]:
                            mettreAJourHTML(afficherTuile(images, 11), xx, yy,
                                            largeur)  # on affiche les mines
                            # restantes (images[11])

                sleep(0.1)  # rafraichir l'écran pour le joueur
                alert('Vous avez gagné :)')
                return fin(largeur, hauteur, nbMines)


"""
Cette procedure permet d'analyser le clic du joueur. Elle est essentielle car
sans elle, il est impossible d'identifier la tuile dans laquelle le joueur
clique. Elle appelera differentes fonctions/procedures lui permettant
d'identifier les tuiles. 

"""


def analyse(x, y, mines, drapeaux, devoilees, largeur):
    minesVoisines = nbMinesVoisines(x, y, mines)
    openOneCase(x, y, mines, drapeaux, devoilees, largeur)  # ouvrir la tuile
    # cliquee
    if minesVoisines == 0:
        for dy in range(-1, 2):
            j = y + dy
            if j >= 0 and j < len(mines):
                for dx in range(-1, 2):
                    i = x + dx
                    if i >= 0 and i < len(mines[0]):
                        # Ouvre toutes les tuiles autour car 0 mines
                        open(i, j, mines, drapeaux, devoilees, largeur)


'''
Cette fonction est lancée lorsque le jeu arrive à une conclusion.La fonction
affiche un alert demandant au joueur s'il veut continuer la partie et lui
propose les boutons à appuer s'il veut rejouer une partie ou non. Si oui,
la fonction init défine plus tard est appellée, sinon le jeu est arrêté
'''


def fin(largeur, hauteur, nbMines):
    msg = "Nouvelle partie? Si oui, appuyer sur OK.\
    Si non, appuyer sur Cancel."
    request = prompt(msg)
    if request != None:
        init(largeur, hauteur, nbMines)


""" 
La procédure init est la fonction démarrant le jeu à la base. Cette fonction
affiche le jeu et s'occupe du changement de la grille HTML pendant que le
jeu est lancé par l'appel de la fonction genererGrilleHTML
"""


def init(largeur, hauteur, nbMines):
    global nbDevoilees, devoilees, drapeaux
    nbDevoilees = 0
    devoilees = grilleBooleenne(largeur, hauteur)
    drapeaux = grilleBooleenne(largeur, hauteur)
    main = document.querySelector('#main')
    main.innerHTML = css
    main.innerHTML += genererGrilleHTML(largeur, hauteur, nbMines)


"""
Voici les tests unitaires. Pour faciliter la compréhension du correcteur, nous
avons negligé la limite de 80 caractères. :) 
"""


def testDemineur():
    assert afficherTuile([1, 24, 6], 2) == 6

    assert afficherTuile([3, 45, 6, 7, 7, 7], 4) == 7

    assert afficherTuile([2, 4, 3, 5], -1) == 5

    assert afficherTuile([1, 2, 3, 5, 6], 3) == 5

    assert afficherTuile([1, 2, 3, 4, 5], -2) == 4

    assert genererRangeeHTML(2, 0, 2, 4, 1) == """<tr><td id="tuile0" onclick="clic(0,0,event.shiftKey,2,2,1)"><img src="http://codeboot.org/images/minesweeper/4.png" ></td>
<td id="tuile1" onclick="clic(1,0,event.shiftKey,2,2,1)"><img src="http://codeboot.org/images/minesweeper/4.png" ></td></tr>"""

    assert genererRangeeHTML(0, 0, 0, None, 0) == """<tr></tr>"""

    assert genererRangeeHTML(0, 0, 0, 0, 0) == """<tr></tr>"""

    assert genererRangeeHTML(3, 1, 4, -1, 4) == """<tr><td id="tuile3" onclick="clic(0,1,event.shiftKey,3,4,4)"><img src="http://codeboot.org/images/minesweeper/mine-red-x.png" ></td>
<td id="tuile4" onclick="clic(1,1,event.shiftKey,3,4,4)"><img src="http://codeboot.org/images/minesweeper/mine-red-x.png" ></td>
<td id="tuile5" onclick="clic(2,1,event.shiftKey,3,4,4)"><img src="http://codeboot.org/images/minesweeper/mine-red-x.png" ></td></tr>"""

    assert genererGrilleHTML(2, 2, 1) == """<table><tr><td id="tuile0" onclick="clic(0,0,event.shiftKey,2,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile1" onclick="clic(1,0,event.shiftKey,2,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td></tr>
<tr><td id="tuile2" onclick="clic(0,1,event.shiftKey,2,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile3" onclick="clic(1,1,event.shiftKey,2,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td></tr></table>"""

    assert genererGrilleHTML(2, 1, 1) == """<table><tr><td id="tuile0" onclick="clic(0,0,event.shiftKey,2,1,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile1" onclick="clic(1,0,event.shiftKey,2,1,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td></tr></table>"""

    assert genererGrilleHTML(3, 1, 1) == """<table><tr><td id="tuile0" onclick="clic(0,0,event.shiftKey,3,1,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile1" onclick="clic(1,0,event.shiftKey,3,1,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile2" onclick="clic(2,0,event.shiftKey,3,1,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td></tr></table>"""

    assert genererGrilleHTML(3, 2, 1) == """<table><tr><td id="tuile0" onclick="clic(0,0,event.shiftKey,3,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile1" onclick="clic(1,0,event.shiftKey,3,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile2" onclick="clic(2,0,event.shiftKey,3,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td></tr>
<tr><td id="tuile3" onclick="clic(0,1,event.shiftKey,3,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile4" onclick="clic(1,1,event.shiftKey,3,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile5" onclick="clic(2,1,event.shiftKey,3,2,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td></tr></table>"""

    assert genererGrilleHTML(3, 3, 1) == """<table><tr><td id="tuile0" onclick="clic(0,0,event.shiftKey,3,3,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile1" onclick="clic(1,0,event.shiftKey,3,3,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile2" onclick="clic(2,0,event.shiftKey,3,3,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td></tr>
<tr><td id="tuile3" onclick="clic(0,1,event.shiftKey,3,3,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile4" onclick="clic(1,1,event.shiftKey,3,3,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile5" onclick="clic(2,1,event.shiftKey,3,3,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td></tr>
<tr><td id="tuile6" onclick="clic(0,2,event.shiftKey,3,3,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile7" onclick="clic(1,2,event.shiftKey,3,3,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td>
<td id="tuile8" onclick="clic(2,2,event.shiftKey,3,3,1)"><img src="http://codeboot.org/images/minesweeper/blank.png" ></td></tr></table>"""

    assert index(1, 1, 2) == 3

    assert index(1, 2, 2) == 5

    assert index(1, 2, 3) == 7

    assert index(-1, -2, 3) == -7

    assert index(0, 0, 0) == 0

    assert grilleBooleenne(1, 1) == [[False]]

    assert grilleBooleenne(2, 1) == [[False, False]]

    assert grilleBooleenne(0, 1) == [[]]

    assert grilleBooleenne(0, 0) == []

    assert grilleBooleenne(3, 3) == [[False, False, False],
                                     [False, False, False], [False, False, False]]
    assert nbMinesVoisines(1, 2, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]) == 3

    assert nbMinesVoisines(1, 1, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]) == 6

    assert nbMinesVoisines(0, 0, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]) == 4

    assert nbMinesVoisines(1, 5, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]) == 0

    assert nbMinesVoisines(0, 0, [[], []]) == 0

    assert checkOpened([[False, False], [True, False]], 2, 2) == 1

    assert checkOpened([[False, False], [False, False]], 2, 2) == 0

    assert checkOpened([[True, True], [True, True]], 2, 2) == 4

    assert checkOpened([[], []], 0, 0) == 0

    assert minesInit(2, 2) == [[False, False], [False, False]]

    assert minesInit(3, 2) == [[False, False, False], [False, False, False]]

    assert minesInit(0, 1) == [[]]

    assert minesInit(1, 0) == []

    assert minesInit(0, 0) == []


testDemineur()
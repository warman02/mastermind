#!/usr/bin/env python
# -*- coding: utf-8 -*-

from initialisations import GAME_PARAMS

MESSAGE_COULEUR_ERREUR='Erreur : Couleur ne correspond pas'
MESSAGE_TAILLE_ERREUR='Erreur : Taille ne correspond pas'



def demander_liste():
    '''
    Fonction qui demande à l'utilisateur d'entrer une liste de couleur
    Elle transforme la chaine de caractére en un Set
    '''

    '''
    Version 1
    liste_couleur = list(input('Entrez de la liste de couleur:'))
    for i in range(len(liste_couleur)) :
        liste_couleur[i]=int(liste_couleur[i])
    return liste_couleur
    '''

    return [int(element) for element in list(input('Entrez la liste de couleur : '))]

def choix_suite_couleur(nb_couleurs, lng_suite):
    couleurs = list(range(1, nb_couleurs + 1))
    #print ('nos couleurs : ', couleurs)
    resultat = demander_liste()
    while len(resultat) != lng_suite or not set(resultat) <= set(couleurs) :

        not set(resultat) <= set(couleurs) and print(MESSAGE_COULEUR_ERREUR)
        len(resultat)!= lng_suite and print(MESSAGE_TAILLE_ERREUR)

        resultat = demander_liste()

    return resultat



def placement(code_choisi, code_a_deviner):
    '''
    Fonction qui retourne le nombre d'éléments bien placés et
    le nombre d'éléments mal placés de la liste choisie par
    rapport à la liste à deviner
    HYPOTHESE : l1 et l2 méme longueur
    '''

    # copie locale de la couleur a deviner et la couleur choisie
    # on l'utilise pour éviter de changer les variables par défaut

    copie_code_a_deviner = []
    for code in code_a_deviner:
        copie_code_a_deviner.append(code)

    copie_code_choisi = []
    for code in code_choisi:
        copie_code_choisi.append(code)

    placeTrue = 0
    placeFalse = 0


    # On parcours le code à deviner et caclule le nombre de couleurs bien placées
    for i in range(0, GAME_PARAMS['LNG_SUITE']):
        if code_a_deviner[i] == code_choisi[i]:
            placeTrue = placeTrue + 1

            # On masque les couleurs bien placées déja trouvées
            copie_code_a_deviner[i] = 42
            copie_code_choisi[i] = 4242


    #import ipdb; ipdb.set_trace()
    # On parcours le code à deviner et caclule le nombre de couleurs mal placées
    for code in copie_code_choisi:
        if code in copie_code_a_deviner:
            placeFalse = placeFalse + 1

            # On masque les couleurs mal placées qu'on a déja trouvé
            for i in range(0, GAME_PARAMS['LNG_SUITE']):
                if copie_code_a_deviner[i] == code:
                    copie_code_a_deviner[i] = 42
                    #copie_code_choisi[i] = 4242


    return (placeTrue,placeFalse)


def affichage_resultat_essai(placeTrue,placeFalse):
    print('Il y a',placeTrue,'elements bien placés et', end=' ')
    print(placeFalse,'elements mal placés')

def affichage_liste_vers_entier(liste):
    print(''.join([str(element) for element in liste]))




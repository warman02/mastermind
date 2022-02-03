#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Faycal'
import random


from itertools import product

MESSAGE_NOMBRE_COULEURS='Saisir le nombre de couleurs: '
MESSAGE_LONGUEUR_SUITE='Saisir la longueur de la suite a deviner: '
MESSAGE_NOMBRE_ESSAI='Saisir le nombre d\'essais: '
GAME_PARAMS = {
    'NB_COULEURS': 0,
    'LNG_SUITE': 0,
    'NB_ESSAI': 0
}


def get_random_code():
    '''
    Fonction qui retourne un code aléatoire (suite de couleurs)
    '''
    random_color_code = []
    for i in range(GAME_PARAMS['LNG_SUITE']):
        color = random.randint(1, GAME_PARAMS['NB_COULEURS'])
        random_color_code.append(color)

    return random_color_code

def askGameParams():
    """Cette fonction demande a l'utilisateur de saisir les parametres pour le début de partie (Le nombre de couleurs, la longueur de la suite et le nombre d'essais)"""
    GAME_PARAMS['NB_COULEURS'] = int(input(MESSAGE_NOMBRE_COULEURS + '>>> '))
    GAME_PARAMS['LNG_SUITE'] = int(input(MESSAGE_LONGUEUR_SUITE + '>>> '))
    GAME_PARAMS['NB_ESSAI'] = int(input(MESSAGE_NOMBRE_ESSAI + '>>> '))


def getGameParams():
    """docstring for getGameParams"""
    return GAME_PARAMS

def initGame(nb_couleurs, lng_suite):
    """docstring for initGame"""
    couleurs = list(range(1, nb_couleurs + 1))
    #Generer toutes les possibilites de suites de couleurs
    produits = list(product(couleurs, repeat=lng_suite))

    #Choisir une suite au hasard
    result = random.choice(produits)

    return result


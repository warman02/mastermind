#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random

from initialisations import GAME_PARAMS
from initialisations import askGameParams
from initialisations import get_random_code
from tourDeJeu import placement


MAX_POP_SIZE = 60 # Taille maximale de la population
MAX_GENERATIONS = 80 # Nombre maximum de générations

# Les probabilités des différentes fonctions de stratégie de séléction naturelle
CROSSOVER_PROBABILITY = 0.5
CROSSOVER_THEN_MUTATION_PROBABILITY = 0.03
PERMUTATION_PROBABILITY = 0.03
INVERSION_PROBABILITY = 0.02
ELITE_RATIO=0.3 # Paramétre de séléction de l'élite des chromosomes (suites de couleurs)


# Notre premier choix de suite de couleurs
# A generer avec une fonction


def first_guess():
    '''
    Fonction qui genère le premier coup à tester suivant la définition
    de l'algorithme génétique

    pour une suite de 4 ->>>  1,1,2,3
    pour une suite de 6 ->>>  1,1,2,2,3,4
    pour une suite de 8 ->>>  1,1,2,2,3,3,4,5

    2 ----> 0
    4 ----> 1
    6 ----> 2
    8 ----> 3
    10----> 4

    (0 - (1)) --> 0
    (2 - (2)) --> 0
    (4 - (3) --- >1
    (6 - (4) --- >2
    (8 - (5) --> 3
    (10 - (6) --> 4
    '''

    # trouver le nombre de repetition
    j = 1
    for i in range(0, GAME_PARAMS['LNG_SUITE']):
        if i % 2 == 0:
            j = j + 1

    if GAME_PARAMS['LNG_SUITE'] % 2 == 0:
        repeat = GAME_PARAMS['LNG_SUITE'] - j
    else:
        repeat = GAME_PARAMS['LNG_SUITE'] - j + 1

    first_guess= []
    for i in range(1, repeat + 1):
        first_guess.append(i)
        first_guess.append(i)


    if GAME_PARAMS['LNG_SUITE'] % 2 == 0:
        last_color = first_guess[GAME_PARAMS['LNG_SUITE'] - 3]
    else:
        last_color = first_guess[GAME_PARAMS['LNG_SUITE'] - 2]
    first_guess.append(last_color + 1)
    first_guess.append(last_color + 2)

    return first_guess



def fitness_score(choix_en_cours, dernier_choix, guesses):
        '''
        fonction de score (fitness) qui prend une couleur (chromosme)
        on retoune un score en fonction de sa qualité en tant que réponse
        probable
        '''



        # Retourne la différence entre le resultat de la couleur choix_en_cours
        # et le resultat de la couleur guess, si guess était considérée
        # comme la couleur à deviner
        def get_difference(choix_en_cours, guess):
            guess_result = guess[1]
            guess_dernier_choix = guess[0]

            # On suppose que guess est le couleur a deviner
            # et on calcul le score que notre couleur choix_en_cours aurait eu
            choix_en_cours_result = placement(choix_en_cours, guess_dernier_choix)

            # On calcule la difference des scores
            dif = [0,0]
            for i in range(2):
                dif[i] = abs(choix_en_cours_result[i] - guess_result[i])

            return tuple(dif)


        # On construit une liste de tuple qui contient les couples
        # de difference on le score de choix_en_cours et le score original de guess
        differences = []
        for guess in guesses:
            differences.append(get_difference(choix_en_cours, guess))

        # On calcul la somme des score de couleur bien placées
        sum_black_pin_differences = 0
        # On calcul la somme des score de couleur mal placées
        sum_white_pin_differences = 0

        for dif in differences:
            sum_black_pin_differences += dif[0]
            sum_white_pin_differences += dif[1]

        # On calcule le score final
        score = sum_black_pin_differences + sum_white_pin_differences
        return score

def genetic_evolution(dernier_choix, last_guesses, eliteratio=ELITE_RATIO):
        '''
        Fonction qui implémente l'algorithme génétique pour trouver la bonne
        réponse au code couleur à rouver.

        Elle génere plusieurs populations on utilisant des stratégies de
        séléction naturelle tel que le croisement, la mutation et la permutation

        Dans cette fonction, on considere la couleur à trouver comme un chromosme
        Les populations qui sont donc construites ressembles à des ensembles
        de chromosomes dont les code d'acides aminés sont des codes couleur

        MAX_POP_SIZE: represente la taille maximale de la population
        generations: represente le nombre maximum de générations de popualtion
        scorefitness: fonction de calcul de fitness du chromosome
        '''

        def crossover(code1, code2):
            '''
            Fonction de croisement
            '''
            newcode = []
            for i in range(GAME_PARAMS['LNG_SUITE']):
                if random.random() > CROSSOVER_PROBABILITY:
                    newcode.append(code1[i])
                else:
                    newcode.append(code2[i])
            return newcode

        def mutate(code):
            '''
            Fonction de mutation
            '''
            i = random.randint(0, GAME_PARAMS['LNG_SUITE']-1)
            v = random.randint(1, GAME_PARAMS['NB_COULEURS'])
            code[i] = v
            return code

        def permute(code):
            '''
            Fonction de permutation
            '''
            for i in range(GAME_PARAMS['LNG_SUITE']):
                if random.random() <= PERMUTATION_PROBABILITY:
                    random_color_position_a = random.randint(0, GAME_PARAMS['LNG_SUITE']-1)
                    random_color_position_b = random.randint(0, GAME_PARAMS['LNG_SUITE']-1)

                    save_color_a = code[random_color_position_a]

                    code[random_color_position_a] = code[random_color_position_b]
                    code[random_color_position_b] = save_color_a
            return code




        def random_population():
            '''
            Fonction qui génère une liste de couleur aléatoires dont la taille
            respecte les parametres du programme LNG_SUITE
            '''

            list_color_codes = []
            for i in range(MAX_POP_SIZE):
                random_color_code = get_random_code() # Obetenir un code aleatoire
                list_color_codes.append(random_color_code) # Ajoute le code a notre lite

            return list_color_codes


        ## On génère la premiere population de codes, de façon aléatoire pour
        ## donner le plus de chance à éviter les doublons dans la population

        population = random_population()



        ###################
        # Ensembles des choix de couleurs favoris à notre prochain coup (Ei)
        chosens = []
        ##################


        generation_en_cours = 1 # Compteur de générations

        while len(chosens) <= MAX_POP_SIZE and generation_en_cours <= MAX_GENERATIONS:

                # Préparer la population des chromosomes fils qui vont hériter
                # de la popualtion parente en passant par la séléction naturelle
                sons = []

                for i in range(MAX_POP_SIZE):

                        # Si on trouve pas deux parents au fils on sort de la boucle
                        if i == len(population) - 1:
                            sons.append(population[i])
                            break

                        # On applique un croisement au fils
                        son = crossover(population[i], population[i+1])


                        # On applique une mutation aprés croisement au fils
                        if random.random() <= CROSSOVER_THEN_MUTATION_PROBABILITY:
                                son = mutate(son)

                        # On applique une mutation au fils
                        son = permute(son)

                        # On rajoute le fils au nouvel ensemble de la population des fils
                        sons.append(son)



                # On lie chaque fils à un score qui décrit la qualité du score
                # Plus le score est proche de zéro, plus le code est favoris
                pop_score = []
                for i in range(MAX_POP_SIZE):
                    son = sons[i]
                    son_score = fitness_score(son, dernier_choix, last_guesses)
                    son_with_score = (son_score, son)
                    pop_score.append(son_with_score)

                # On ordone notre la population fils par rapport au score du
                # plus petit au plus grand
                pop_score = sorted(pop_score, key=lambda x: x[0])
                #print [score for (score, c) in pop_score]



                # On construit la liste des codes favoris
                # On utilise le parametre eliteration pour choisir une elite
                # de code parmis tout les choix possibles, répliquant la stratégie
                # de sélection naturalle

                # D'abord on selectionne une elite
                eligibles = [(score, e) for (score, e) in pop_score if score == 0]


                # Si on trouve aucune elite dans la génération en crous
                # on abondonne la génération en cours
                if len(eligibles) == 0:
                    generation_en_cours = generation_en_cours + 1
                    continue


                # En suite on elimine la partie score de nos choix favoris
                new_eligibles = []
                for (score, code) in eligibles:
                    new_eligibles.append(code)
                eligibles = new_eligibles


                # On élimine tout les codes dans eligibles qui existent déja
                # dans notre ensemble de choix favoris Ei
                for code in eligibles:
                    if code in chosens:
                        chosens.remove(code)

                        # En remplace le code supprimé par un code aléatoire
                        random_code = get_random_code()
                        chosens.append(random_code)


                # On rajoute les éléments favoris dans notre ensemble de code
                # favoris Ei
                for eligible in eligibles:
                    # On fait attention à ne pas dépasser la taille MAX_POP_SIZE
                    # on remplissant l'ensemble Ei (Ei <= MAX_POP_SIZE)
                    if len(chosens) == MAX_POP_SIZE:
                        break

                    # Si le code favoris n'est pas déja dans l'ensemble des favoris
                    # Ei on le rajoute
                    if not eligible in chosens:
                        chosens.append(eligible)


                # On prépare la popualtion parente de la prochaine génération
                # à partir de la génération actuelle
                population=[]
                population.extend(eligibles)


                # On remplit le reste de la population jusqu'a MAX_POP_SIZE avec
                # des codes couleur aléatoirs
                j = len(eligibles)
                while j < MAX_POP_SIZE:
                    random_code = get_random_code()
                    population.append(random_code)
                    j = j + 1



                # A chaque génération, on devient plus aggressifs de la séléction
                # des codes favoris, c'est à dire plus séléctifs
                #if not eliteratio < 0.01:
                    #eliteratio -= 0.01

                generation_en_cours = generation_en_cours + 1

        # On retourne notre ensemble de choix favoris Ei
        return chosens



# Jouer un tours avec l'IA
def play_with_IA(choix, code_a_deviner, turn):



    choix_a_imprimer = ''
    for color in choix:
        choix_a_imprimer += str(color)
    #print('|||>>||||>>>>>>>>>>>>>>>>>> PLAYING: ', choix, ' Turn : ', turn)
    print('\nessai: ', turn)
    print('Proposition de l\'ordinateur: ', choix_a_imprimer)
    res =  placement(choix, code_a_deviner)
    print(res[0], ' bien placé(s), et ', res[1], ' mal placé(s)')
    return res



def main():

        # Permet d'avoir des nombres trés aléatoires
        random.seed(os.urandom(32))


        # Initialiser la partie et proposer un code à deviner
        askGameParams()
        code_a_deviner = get_random_code()
        code_a_deviner_imprimer = ''
        for color in code_a_deviner:
            code_a_deviner_imprimer += str(color)

        print('L\'ordinateur à choisi le code ', code_a_deviner_imprimer, 'à deviner')

        G1 = first_guess() # Générer le premier coup
        prochain_coup = G1
        turn = 1


        # Liste de tout nos précédents choix avec leurs résultats
        guesses = []


        # Proposer un coup
        result=play_with_IA(prochain_coup, code_a_deviner, turn)

        # Rajouter le coup a notre liste de choix précédents
        guesses.append((prochain_coup, result))


        while result != (GAME_PARAMS['LNG_SUITE'],0):

            # Incrementer la partie
            turn += 1

            if turn > GAME_PARAMS['NB_ESSAI']:
                print('\nL\'IA a perdu à deviner ', code_a_deviner_imprimer)
                break

            eligibles = genetic_evolution(prochain_coup, guesses)
            #print('Ei', len(eligibles))


            # Si on a aucun favoris, demander à nouveau
            while len(eligibles) == 0:
                eligibles = genetic_evolution(prochain_coup, guesses)
                #print(guesses)


            # Choisir un coup a jouer de la liste des choix favoris
            prochain_coup = eligibles.pop()

            # Si on a deja jouer le coup, choisir un autre coup
            while prochain_coup in [coup for (coup, res) in guesses]:
                prochain_coup = eligibles.pop()

            # Jouer le coup qu'on a choisi de la liste des favoris
            result = play_with_IA(prochain_coup, code_a_deviner, turn)

            # Enregistrer le coup et son resultat
            guesses.append((prochain_coup, result))


            if result == (GAME_PARAMS['LNG_SUITE'],0):
                print('\nL\'IA a gagné à deviner ', code_a_deviner_imprimer)
                #print(prochain_coup, result)


if __name__ == '__main__':
        main()

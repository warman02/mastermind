from initialisations import *
from tourDeJeu import *

def faire_un_essai(game,deviner):
    print('')
    print('essai: ', game, '/', GAME_PARAMS['NB_ESSAI'])
    user_choix = choix_suite_couleur(GAME_PARAMS['NB_COULEURS'], GAME_PARAMS['LNG_SUITE'])
    resultat_placement = placement(user_choix, deviner)
    affichage_resultat_essai(resultat_placement[0], resultat_placement[1])
    return resultat_placement


def main():
    #print  'argv >>> {0}'.format(sys.argv)
    print('Explication jeu : http://fr.wikipedia.org/wiki/Mastermind')
    askGameParams()
    #print(getGameParams())
    #print(initGame(GAME_PARAMS['NB_ESSAI'], GAME_PARAMS['LNG_SUITE']))
    deviner = initGame(GAME_PARAMS['NB_COULEURS'], GAME_PARAMS['LNG_SUITE'])
    #print('a deviner : ', deviner)
    game = 1
    resultat_placement = faire_un_essai(game,deviner)
    while resultat_placement != (4,0) and game != GAME_PARAMS['NB_ESSAI']:
        resultat_placement = faire_un_essai(game + 1,deviner)
        game = game + 1
    print('Le nombre à deviner est : ',deviner)
    sys.exit(0)       
    


if __name__ == '__main__':
    main()
    
    

    
    

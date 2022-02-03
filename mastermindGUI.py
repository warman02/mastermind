#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
import random
from symbols import COLOR_SPACE
from symbols import SYMBOLS
from pygame.locals import *

from tourDeJeu import placement

pygame.init()

######### COULEUR  ##########
WHITE = (255,255,255)
GREEN = (200,255,200)
BG_COLOR = [0,13,1]
ZONE_BG_COLOR = [0,13,1,100]
#############################


##### FENETRE PARAM #####
WINDOWS_SIZE = (800, 600)
FENETRE = pygame.display.set_mode(WINDOWS_SIZE, RESIZABLE)
TEXT_WIDTH = 25
FPS = 60
#############################

######## GAME PARAM #########
COLORS_TO_SYMBOLS = {} # Lier des couleurs aux symboles à cracker
KEYS_TO_SYMBOLS = {} # Lier des touches clavier aux symboles à deviner
GAME_COLOR_SPACE= []
OVERLAY_PARAM = [20,20,0,230]
GAME_PARAMS = {
    'LNG_SUITE': 4,
    'NB_ESSAI': 4,
    'NB_COULEURS': 6
}
#############################


ZONE_JEU_GAUCHE = 5/100
ZONE_JEU_HAUT = 5/100
ZONE_JEU_LARGEUR = 70/100
ZONE_JEU_HAUTEUR = 65/100



ZONE_CHOIX_COULEUR_GAUCHE = 85/100
ZONE_CHOIX_COULEUR_HAUT = 5/100
ZONE_CHOIX_COULEUR_LARGEUR = 10/100
ZONE_CHOIX_COULEUR_HAUTEUR = 65/100



ZONE_SELECTION_COULEUR_GAUCHE = 5/100
ZONE_SELECTION_COULEUR_HAUT = 80/100
ZONE_SELECTION_COULEUR_LARGEUR = 70/100
ZONE_SELECTION_COULEUR_HAUTEUR = 11/100


#ZONE_JEU = [WINDOWS_SIZE[0]*ZONE_JEU_GAUCHE, WINDOWS_SIZE[1]*ZONE_JEU_HAUT, WINDOWS_SIZE[0]*ZONE_JEU_LARGEUR, WINDOWS_SIZE[1]*ZONE_JEU_HAUTEUR]
ZONE_JEU_POSITION = [WINDOWS_SIZE[0]*ZONE_JEU_GAUCHE, WINDOWS_SIZE[1]*ZONE_JEU_HAUT]
ZONE_JEU_TAILLE = [WINDOWS_SIZE[0]*ZONE_JEU_LARGEUR, WINDOWS_SIZE[1]*ZONE_JEU_HAUTEUR]


#ZONE_SELECTION_COULEUR = [WINDOWS_SIZE[0]*ZONE_SELECTION_COULEUR_GAUCHE, WINDOWS_SIZE[1]*ZONE_SELECTION_COULEUR_HAUT, WINDOWS_SIZE[0]*ZONE_SELECTION_COULEUR_LARGEUR, WINDOWS_SIZE[1]*ZONE_SELECTION_COULEUR_HAUTEUR]
ZONE_SELECTION_COULEUR_POSITION = [WINDOWS_SIZE[0]*ZONE_SELECTION_COULEUR_GAUCHE, WINDOWS_SIZE[1]*ZONE_SELECTION_COULEUR_HAUT]
ZONE_SELECTION_COULEUR_TAILLE = [WINDOWS_SIZE[0]*ZONE_SELECTION_COULEUR_LARGEUR, WINDOWS_SIZE[1]*ZONE_SELECTION_COULEUR_HAUTEUR]

#ZONE_CHOIX_COULEUR = [WINDOWS_SIZE[0]*ZONE_CHOIX_COULEUR_GAUCHE, WINDOWS_SIZE[1]*ZONE_CHOIX_COULEUR_HAUT, WINDOWS_SIZE[0]*ZONE_CHOIX_COULEUR_LARGEUR, WINDOWS_SIZE[1]*ZONE_CHOIX_COULEUR_HAUTEUR]
ZONE_CHOIX_COULEUR_POSITION = [WINDOWS_SIZE[0]*ZONE_CHOIX_COULEUR_GAUCHE, WINDOWS_SIZE[1]*ZONE_CHOIX_COULEUR_HAUT]
ZONE_CHOIX_COULEUR_TAILLE = [WINDOWS_SIZE[0]*ZONE_CHOIX_COULEUR_LARGEUR, WINDOWS_SIZE[1]*ZONE_CHOIX_COULEUR_HAUTEUR]





############ FONCTIONS  ####################


def get_random_code():
    '''
    Fonction qui retourne un code aléatoire (suite de couleurs)
    '''
    random_color_code = []
    for i in range(GAME_PARAMS['LNG_SUITE']):
        color = random.randint(1, GAME_PARAMS['NB_COULEURS'])
        random_color_code.append(color)

    return random_color_code

def get_vert_symbol_position(pos, symbol_font_size, zone_surface):
    '''
    Retourne la position du symbole dans la zone
    '''
    #import ipdb; ipdb.set_trace()
    zone_height = zone_surface.get_size()[1]
    zone_width = zone_surface.get_size()[0]

    symbol_height = zone_height / GAME_PARAMS['LNG_SUITE']
    symbol_width = zone_width

    symbol_pos_x = (symbol_width / 2) - (symbol_width / 4)
    #symbol_pos_x = 0
    symbol_pos_y_top = (pos - 1) * symbol_height
    symbol_pos_y = symbol_pos_y_top + (symbol_height / 8)
    #symbol_pos_y = (symbol_pos_y_top / 2) - (symbol_pos_y_top / 4)


    return [symbol_pos_x, symbol_pos_y]


def draw_vert_symbol(pos, zone_surface):
    '''
    Dessine le symbole qui correspond a la position et donc au code couleur
    passe en parametre
    '''
    symbol_font_size = zone_surface.get_size()[0]
    font = pygame.font.Font('fonts/matrix_code_nfi.otf', symbol_font_size)

    symbol_pos = get_vert_symbol_position(pos, symbol_font_size, zone_surface)

    symbol = KEYS_TO_SYMBOLS[pos]

    symbol_color = COLORS_TO_SYMBOLS[symbol]

    symbol_draw = font.render(symbol, True, pygame.color.Color(symbol_color))

    zone_surface.blit(symbol_draw, symbol_pos)




def get_horz_symbol_position(pos, symbol_font_size, zone_surface):
    '''
    Retourne la position du symbole dans la zone
    '''
    #import ipdb; ipdb.set_trace()
    zone_height = zone_surface.get_size()[1]
    zone_width = zone_surface.get_size()[0]

    symbol_height = zone_height
    symbol_width = zone_width / GAME_PARAMS['LNG_SUITE']


    symbol_pos_x_left = (pos - 1) * symbol_width
    symbol_pos_x = symbol_pos_x_left + (symbol_width / 4)
    symbol_pos_y = (symbol_height / 2) - (symbol_height / 2)



    return [symbol_pos_x, symbol_pos_y]



def draw_horz_symbol(pos, zone_surface, symbol):
    '''
    Dessine le symbole qui correspond a la position et donc au code couleur
    passe en parametre
    '''
    symbol_font_size = zone_surface.get_size()[1]
    font = pygame.font.Font('fonts/matrix_code_nfi.otf', symbol_font_size)

    symbol_pos = get_horz_symbol_position(pos, symbol_font_size, zone_surface)

    symbol_color = COLORS_TO_SYMBOLS[symbol]

    symbol_draw = font.render(symbol, True, pygame.color.Color(symbol_color))

    zone_surface.blit(symbol_draw, symbol_pos)










def map_colors_to_symbols():
    '''
    Fonction qui lie des couleurs aux symboles qui représentes le coder
    à cracker
    '''

    color_space = COLOR_SPACE[:GAME_PARAMS['LNG_SUITE']]

    GAME_COLOR_SPACE = color_space

    random.shuffle(SYMBOLS)

    symbols = SYMBOLS[:GAME_PARAMS['LNG_SUITE']]

    for i, symbol in enumerate(symbols):
        COLORS_TO_SYMBOLS[symbol] = GAME_COLOR_SPACE[i]


def map_keys_to_symbols():
    '''
    Fonction qui attribue des touches du clavier aux symboles qui representent
    le code à cracker
    '''

    symbols = list(COLORS_TO_SYMBOLS.keys())
    for i in range(0, GAME_PARAMS['LNG_SUITE']):
        KEYS_TO_SYMBOLS[i+1] = symbols[i-1]

    print(KEYS_TO_SYMBOLS)



def evenement_clavier(event, selections, compteur_choix):

    validate = False
    for i in range(0, GAME_PARAMS['LNG_SUITE'] + 1):
        if event.unicode == str(i):
            if len(selections) < GAME_PARAMS['LNG_SUITE']:
                selections.append(i)
                compteur_choix += 1
                print(selections)

        if event.key == K_BACKSPACE: #If backspace
            if len(selections) != 0:
                selections.pop()
                compteur_choix -= 1

        if event.key == K_RETURN:
            if len(selections) == GAME_PARAMS['LNG_SUITE']:
                validate = True


    return [selections, compteur_choix, validate]

    #if event.key == K_1 or event.key == K_KP1:
        #print('On gere la touche 1')
    #elif event.key == K_2 or event.key == K_KP2:
        #print('On gere la touche 2')
    #elif event.key == K_3 or event.key == K_KP3:
        #print('On gere la touche 3')
    #elif event.key == K_4 or event.key == K_KP4:
        #print('On gere la touche 4')
    #else:
        #print('On ne gere pas la touche')

def draw_turn_score(score, turn_score_surface):

    width = turn_score_surface.get_size()[0]
    height = turn_score_surface.get_size()[1]

    # Areas to show scores (4 squares )
    score_area_width = width / 2
    score_area_height = height / 2
    score_areas = []

    for i in range(0, GAME_PARAMS['LNG_SUITE']):
        if i == 0:
            area = [0,0,score_area_width,score_area_height]
        elif i == 1:
            area = [score_area_width, 0, width, score_area_height]
        elif i == 2:
            area = [0, score_area_height, score_area_width, height]
        elif i == 3:
            area = [score_area_width, score_area_height, width, height]

        score_areas.append(area)

    score_areas = list(reversed(score_areas))

    # Draw good answer scores
    for i in range(score[0]):
        pygame.draw.rect(turn_score_surface, [0,152,5, 100], score_areas.pop())

    # Draw bad answer scores
    for i in range(score[1]):
        pygame.draw.rect(turn_score_surface, [0,74,2, 100], score_areas.pop())


def ajouter_reponse(turn, code, result, game_surface):
    surface_width = game_surface.get_size()[0]
    surface_height = game_surface.get_size()[1]

    turn_height = surface_height / GAME_PARAMS['NB_ESSAI']

    # Surface for turn score left
    turn_score_area = [surface_width * 20 / 100, turn_height]
    turn_score_surface = pygame.Surface(turn_score_area, flags=SRCALPHA)

    # Surface for turn answer right
    turn_answer_area = [surface_width * 80 / 100, turn_height]
    turn_answer_surface = pygame.Surface(turn_answer_area, flags=SRCALPHA)

    # Surface of the turn
    turn_global_surface = pygame.Surface([surface_width, turn_height], flags=SRCALPHA)
    turn_global_surface.fill(ZONE_BG_COLOR)

    # Draw answer in answer area
    for i, c in enumerate(code):
        draw_horz_symbol(i+1, turn_answer_surface, KEYS_TO_SYMBOLS[c])

    # Draw turn score
    draw_turn_score(result, turn_score_surface)

    # Blit answer to global surface
    turn_global_surface.blit(turn_score_surface, [0,0])

    # Blit score to global surface
    turn_global_surface.blit(turn_answer_surface, [surface_width * 20 / 100, 0])


    game_surface.blit(turn_global_surface, [0, game_surface.get_size()[1] - turn_height])








def afficher_interface():

    SURFACE_CHOIX = pygame.Surface(ZONE_CHOIX_COULEUR_TAILLE, flags=SRCALPHA)
    SURFACE_CHOIX.fill(ZONE_BG_COLOR)

    SURFACE_SELECTION = pygame.Surface(ZONE_SELECTION_COULEUR_TAILLE, flags=SRCALPHA)
    SURFACE_SELECTION.fill(ZONE_BG_COLOR)

    SURFACE_JEU = pygame.Surface(ZONE_JEU_TAILLE, flags=SRCALPHA)
    SURFACE_JEU.fill(ZONE_BG_COLOR)


    return (SURFACE_CHOIX, SURFACE_SELECTION, SURFACE_JEU)






#######################################
############# MAIN ####################

def main():

    pygame.display.set_caption('Mastermind')

    #SETUP FRAME CLOCK
    clock = pygame.time.Clock()

    ###### BACKGROUND VIDEO
    background_movie = pygame.movie.Movie('./videos/Digital_Rain.mpg')
    background_movie.set_display(FENETRE)
    movie_screen = pygame.Surface(background_movie.get_size()).convert()


    background_movie.set_display(movie_screen)
    background_movie.play()
    ######################################################################


    ###### BACKGROUND SOUND

    pygame.mixer.music.load('musique.wav')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.75) #Met le volume à 0.75
    #####################################################################

    ########### VIDEO OVERLAY
    video_overlay = pygame.Surface(FENETRE.get_size(), flags=SRCALPHA)
    video_overlay.fill(OVERLAY_PARAM)



    ########### TEXT PROPERTIES

    text_width=TEXT_WIDTH
    try:
        font = pygame.font.Font('fonts/matrix_code_nfi.otf', text_width)
    except:
        raise "You need to have Ocra font on your computer to run this program."


    ########### IGNORE MOUSE EVENTS
    pygame.event.set_blocked(pygame.MOUSEMOTION)

    map_colors_to_symbols()
    map_keys_to_symbols()





    # Code a deviner
    to_guess = get_random_code()



    compteur_choix = 0
    selection = []
    validate = False
    turn = 1
    print(to_guess)

    while True:

        #####################################
        # 1- EVENEMENTS
        #####################################

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
            if event.type == KEYDOWN:
               [selection, compteur_choix, validate] = evenement_clavier(event, selection, compteur_choix)



        #####################################
        # 2- LOGIQUE DU JEU
        #####################################

        if not background_movie.get_busy():
            background_movie.rewind()
            background_movie.play()




        #####################################
        # 3- LOGIQUE DE DESSIN
        #####################################


        FENETRE.fill(BG_COLOR)

        FENETRE.blit(movie_screen, [0,0])
        FENETRE.blit(video_overlay, [0,0])



        (zone_choix, zone_selection, zone_jeu) = afficher_interface()

        text = font.render("Hello World !", True, [0,0,0])
        zone_jeu.blit(text, [200, 200])


        for  i in range(0, GAME_PARAMS['LNG_SUITE']):
            draw_vert_symbol(i+1, zone_choix)


        for i in range(0, compteur_choix):
            draw_horz_symbol(i + 1, zone_selection, KEYS_TO_SYMBOLS[selection[i]])


        if validate:
            print(selection)
            print(to_guess)
            result = placement(selection, to_guess)
            print(result)
            ajouter_reponse(turn, selection, result, zone_jeu)
            turn += 1
            selection = []
            compteur_choix = 0



        #ajouter_reponse(1, [3,2,2,1], (3,1), zone_jeu)

        FENETRE.blit(zone_choix, ZONE_CHOIX_COULEUR_POSITION)
        FENETRE.blit(zone_selection, ZONE_SELECTION_COULEUR_POSITION)
        FENETRE.blit(zone_jeu, ZONE_JEU_POSITION)











        #####################################
        # 4-MAJ ECRAN ET FPS
        #####################################

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

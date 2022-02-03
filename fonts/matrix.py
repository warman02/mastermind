#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import*
import time
import random
import sys
from symbols import COLOR_SPACE
from symbols import SYMBOLS
pygame.init()


## General window params
WINDOW_SIZE = [800,600]
BG_COLOR = [0,13,1]
TEXT_WIDTH = 25

## Game speed params
FRAME_RATE = 30


## COLORS
GREEN = [200,255,200]


COLORS_TO_SYMBOLS = {} # Lier des couleurs aux symboles à cracker




def map_keys_to_symbols(nb_colors):
    '''
    Fonction qui attribue des touches du clavier aux symboles qui representent
    le code à cracker
    '''



def map_colors_to_symbols(nb_colors):
    '''
    Fonction qui lie des couleurs aux symboles qui représentes le coder
    à cracker
    '''

    color_space = [random.choice(COLOR_SPACE) for color in range(nb_colors)]
    symbols = [random.choice(SYMBOLS) for color in range(nb_colors)]

    COLORS_TO_SYMBOLS = dict(zip(symbols, color_space))


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#



def main():
    size = WINDOW_SIZE
    screen = pygame.display.set_mode(size)


    # Setup frame clock
    clock = pygame.time.Clock()



    ###### Background Video
    background_movie = pygame.movie.Movie('./videos/Digital_Rain.mpg')
    background_movie.set_display(screen)
    movie_screen = pygame.Surface(background_movie.get_size()).convert()


    background_movie.set_display(movie_screen)
    background_movie.play()
    ######################################################################


    ########### Video Overlay
    video_overlay = pygame.Surface(screen.get_size(), flags=SRCALPHA)
    video_overlay.fill([20,20,0,230])



    #### Text Properties
    random_color= pygame.Color(map_colors_to_symbols(10))

    text_width=TEXT_WIDTH
    try:
        font = pygame.font.Font('fonts/matrix_code_nfi.otf', text_width)
    except:
        raise "You need to have Ocra font on your computer to run this program."

    print('before loop')


    quit = False


    while not quit:

        ## Handle events
        quit = pygame.event.get(pygame.QUIT)



        # Game logic goes here

        if not background_movie.get_busy():
            print('movie finished')
            background_movie.rewind()
            background_movie.play()


        ##### Drawing logic goes here
        # First clear the screen
        screen.fill(BG_COLOR)


        text = font.render("Hello World !", True, random_color)


        screen.blit(movie_screen, [0,0])
        screen.blit(video_overlay, [0,0])


        screen.blit(text, [250,250])



        ## End drawing
        ###############################

        ## Update screen with drawn objects
        pygame.display.flip()


        ## Limit time frame
        clock.tick(FRAME_RATE)



############################
############################

if __name__ == "__main__":
    main()
    sys.exit(0)

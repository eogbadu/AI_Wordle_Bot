# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 13:25:36 2022

@author: johnny

This code was heavily influenced by a design published in youtube under 
this url: https://www.youtube.com/watch?v=mJ2hPj3kURg

Github repository: https://github.com/baraltech/Wordle-PyGame

Baral, H. (n.d.). GitHub - baraltech/Wordle-PyGame: 
    A clone of the ever-popular Wordle game made in Python using 
    PyGame for my YouTube tutorial. GitHub. Retrieved November 5, 
    2022, 
    from https://github.com/baraltech/Wordle-PyGame 
    Author is Harsit, a 9th grade student in Canada. 
    He loves programming and making tutorials about it. 
    He's from Nepal (not India). Wordle interface using pygame.

Harsit's code fills most of our requirements except that it is bound to 
keyboard inputs and we need an interface for our AI agents to interact with.  
So this code will be refactored to provide inserts for agent interactions.

Harsit's code will be tagged #H

"""
import pygame  #H
import sys     #H
import random  #H
# from words import * #H this fails rewritten next line
from words import WORDS
print(WORDS[1])
pygame.init()  #H


# Constants  #H

WIDTH, HEIGHT = 633, 900  #H

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) #H
BACKGROUND = pygame.image.load("assets/Starting Tiles.png") #H
BACKGROUND_RECT = BACKGROUND.get_rect(center=(317, 300)) #H
ICON = pygame.image.load("assets/Icon.png") #H

# pygame.display.set_caption("Wordle!") #H
pygame.display.set_caption("CMSC671 Project Machine Learning Wordle solver!")

pygame.display.set_icon(ICON) #H

GREEN = "#6aaa64"  #H
YELLOW = "#c9b458"  #H
GREY = "#787c7e"  #H
OUTLINE = "#d3d6da"  #H
FILLED_OUTLINE = "#878a8c"  #H

CORRECT_WORD = "coder"  #H

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]  #H

GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)  #H
AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)  #H

SCREEN.fill("white")  #H
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)  #H
pygame.display.update()  #H

LETTER_X_SPACING = 85  #H
LETTER_Y_SPACING = 12  #H
LETTER_SIZE = 75  #H

# Global variables  #H

guesses_count = 0  #H

# guesses is a 2D list that will store guesses. A guess will be a list of letters.  #H
# The list will be iterated through and each letter in each guess will be drawn on the screen.  #H
guesses = [[]] * 6  #H

current_guess = []  #H
current_guess_string = ""  #H
current_letter_bg_x = 110  #H

# Indicators is a list storing all the Indicator object. An indicator is 
# that button thing with all the letters you see.  #H
indicators = []  #H

game_result = ""  #H

class Letter:  #H
    def __init__(self, text, bg_position):  #H
        # Initializes all the variables, including text, color, position, size, etc.  #H
        self.bg_color = "white"  #H
        self.text_color = "black"  #H
        self.bg_position = bg_position  #H
        self.bg_x = bg_position[0]  #H
        self.bg_y = bg_position[1]  #H
        self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)  #H
        self.text = text  #H
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)  #H
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)  #H
        self.text_rect = self.text_surface.get_rect(center=self.text_position)  #H

    def draw(self):  #H
        # Puts the letter and text on the screen at the desired positions.  #H
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)  #H
        if self.bg_color == "white":  #H
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)  #H
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)  #H
        SCREEN.blit(self.text_surface, self.text_rect)  #H
        pygame.display.update()  #H

    def delete(self):  #H
        # Fills the letter's spot with the default square, emptying it.  #H
        pygame.draw.rect(SCREEN, "white", self.bg_rect)  #H
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)  #H
        pygame.display.update()  #H

class Indicator:  #H
    def __init__(self, x, y, letter):  #H
        # Initializes variables such as color, size, position, and letter.  #H
        self.x = x  #H
        self.y = y  #H
        self.text = letter  #H
        self.rect = (self.x, self.y, 57, 75)  #H
        self.bg_color = OUTLINE  #H

    def draw(self):  #H
        # Puts the indicator and its text on the screen at the desired position.  #H
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)  #H
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")  #H
        self.text_rect = self.text_surface.get_rect(center=(self.x+27, self.y+30))  #H
        SCREEN.blit(self.text_surface, self.text_rect)  #H
        pygame.display.update()  #H

# Drawing the indicators on the screen.  #H

indicator_x, indicator_y = 20, 600  #H

for i in range(3):  #H
    for letter in ALPHABET[i]:  #H
        new_indicator = Indicator(indicator_x, indicator_y, letter)  #H
        indicators.append(new_indicator)  #H
        new_indicator.draw()  #H
        indicator_x += 60  #H
    indicator_y += 100  #H
    if i == 0:  #H
        indicator_x = 50  #H
    elif i == 1:  #H
        indicator_x = 105  #H

def check_guess(guess_to_check):  #H
    # Goes through each letter and checks if it should be green, yellow, or grey.  #H
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result   #H
    game_decided = False  #H
    for i in range(5):  #H
        lowercase_letter = guess_to_check[i].text.lower()  #H
        if lowercase_letter in CORRECT_WORD:  #H
            if lowercase_letter == CORRECT_WORD[i]:  #H
                guess_to_check[i].bg_color = GREEN  #H
                for indicator in indicators:  #H
                    if indicator.text == lowercase_letter.upper():  #H
                        indicator.bg_color = GREEN  #H
                        indicator.draw()  #H
                guess_to_check[i].text_color = "white"  #H
                if not game_decided:  #H
                    game_result = "W"  #H
            else:  #H
                guess_to_check[i].bg_color = YELLOW  #H
                for indicator in indicators:  #H
                    if indicator.text == lowercase_letter.upper():  #H
                        indicator.bg_color = YELLOW  #H
                        indicator.draw()  #H
                guess_to_check[i].text_color = "white"  #H
                game_result = ""  #H
                game_decided = True  #H
        else:  #H
            guess_to_check[i].bg_color = GREY  #H
            for indicator in indicators:  #H
                if indicator.text == lowercase_letter.upper():  #H
                    indicator.bg_color = GREY  #H
                    indicator.draw()  #H
            guess_to_check[i].text_color = "white"  #H
            game_result = ""  #H
            game_decided = True  #H
        guess_to_check[i].draw()  #H
        pygame.display.update()  #H
    
    guesses_count += 1  #H
    current_guess = []  #H
    current_guess_string = ""  #H
    current_letter_bg_x = 110  #H

    if guesses_count == 6 and game_result == "":  #H
        game_result = "L"  #H

def play_again():  #H
    # Puts the play again text on the screen.  #H
    pygame.draw.rect(SCREEN, "white", (10, 600, 1000, 600))  #H
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)  #H
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")  #H
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 700))  #H
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "black")  #H
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 650))  #H
    SCREEN.blit(word_was_text, word_was_rect)  #H
    SCREEN.blit(play_again_text, play_again_rect)  #H
    pygame.display.update()  #H

def reset():  #H
    # Resets all global variables to their default states.  #H
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result  #H
    SCREEN.fill("white")  #H
    SCREEN.blit(BACKGROUND, BACKGROUND_RECT)  #H
    guesses_count = 0  #H
    CORRECT_WORD = random.choice(WORDS)  #H
    guesses = [[]] * 6  #H
    current_guess = []  #H
    current_guess_string = ""  #H
    game_result = ""  #H
    pygame.display.update()  #H
    for indicator in indicators:  #H
        indicator.bg_color = OUTLINE  #H
        indicator.draw()  #H

def create_new_letter():  #H
    # Creates a new letter and adds it to the guess.  #H
    global current_guess_string, current_letter_bg_x  #H
    current_guess_string += key_pressed  #H
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count*100+LETTER_Y_SPACING))  #H
    current_letter_bg_x += LETTER_X_SPACING  #H
    guesses[guesses_count].append(new_letter)   #H
    current_guess.append(new_letter)  #H
    for guess in guesses:  #H
        for letter in guess:  #H
            letter.draw()  #H

def delete_letter():  #H
    # Deletes the last letter from the guess.  #H
    global current_guess_string, current_letter_bg_x  #H
    guesses[guesses_count][-1].delete()  #H
    guesses[guesses_count].pop()  #H
    current_guess_string = current_guess_string[:-1]  #H
    current_guess.pop()  #H
    current_letter_bg_x -= LETTER_X_SPACING   #H

while True:  #H
    if game_result != "":  #H
        play_again()  #H
    for event in pygame.event.get():  #H
        if event.type == pygame.QUIT:  #H
            pygame.quit()  #H
            sys.exit()  #H
        if event.type == pygame.KEYDOWN:  #H
            if event.key == pygame.K_RETURN:  #H
                if game_result != "":  #H
                    reset()  #H
                else:  #H
                    if len(current_guess_string) == 5 and current_guess_string.lower() in WORDS:  #H
                        check_guess(current_guess)  #H
            elif event.key == pygame.K_BACKSPACE:  #H
                if len(current_guess_string) > 0:  #H
                    delete_letter()  #H
            else:  #H
                key_pressed = event.unicode.upper()  #H
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":  #H
                    if len(current_guess_string) < 5:  #H
                        create_new_letter()  #H
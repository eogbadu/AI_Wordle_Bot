# Wordle Wiz
This project is for the CMSC671 fall class at UMBC.
This is comprised of code from the pixegami author found on YouTube and GitHub (see citations below).

### Tools Needed
1. The submitted zipped folder
2. Tool to run Jupyter notebook file. Google Colab can be used but Jupyter Notebook is highly recommended. [Download Jupyter here.](https://jupyter.org/)
3. The love of wordle and ability to enjoy impressive coding skills


### To play the game;
1. Download the zipped wordle pixiegami folder.
2. Unzip the downloaded folder.
3. Step into the "wordle pixiegami/python-wordle-main" folder. 
4. Launch the **pixigame_modified_play_wordle_with_agent_loop.ipynb** jupyter notebook file.
..* Ensure that the "Rich" python module is installed. Use pip to install. Use `pip install rich`
5. Run all cells in Jupyter Notebook.

    ###### On Win/Linux:
        Esc (unselect potential cells or edit modes)
        Ctrl + A (select all cells)
        Shift + Enter (run all selected)
    ###### On Mac:
        Esc (unselect potential cells or edit modes)
        ⌘ + A (select all cells)
        Shift + Enter (run all selected)

### Overvue
* The game is interactive currently for a human player using the python input feature in the notebook.
* The game is also interactive for an agent through a file implementation where the agent can write guesses to a file.  
* The main loop reads the guesses and provides visual feedback. Visual feedback features containing statistics is shown as well.  
* The code has been modified and scripts added to provide an interface for an agent to play the game.
* This is done by writing guesses to the agent_guesses file. The main loop is run from the "pixigame_modified_play_wordle_with_agent_loop.ipynb" script.  
* There is a data directory where the data files are stored.  
* These files were code written by this team and includes code from the play_wordle.py file that was written by the original author.

### Highlighted Files
**Agent_guess_writer.ipynb:** This script provides an interface for the agent to write guesses into a file.  That file is embedded in the game loop and the master agent pulls these guesses into the game.
  
**create_5_letter_word_text.ipynb:** This file creates a 5 letter word list from the nltk words data file, extracting the 5 letter words and writing these to a file in the data directory.
    
**pixigame_modified_play_wordle_with_agent_loop.ipynb:** This script includes code from the original author that has been included, augmented, and modified to support the game interface as well as providing a game loop where the agent software can connect.  

### The files below are original from the pixegami author
* **convert_words.py**
* **letter_state.py**
* **play_wordle.py**
* **word_source.txt**
* **wordle.py**
* **convert_words.py:** This is a script from the original author that creates the word list.
* **The Data directory**
* **word_source.txt:** This is the author's word list.

### These files were written as part of this project
* **agent_guesses.txt:** This is a file that provides the agent input to the game.
* **wordle_words.txt:** This is a file of the words used in this script.

### Citations
This work was significantly informed by code from this YouTube site and corresponding GitHub repository.  

Created on Sat Nov 5 13:25:36 2022
@Author: johnny
This code was heavily influenced by a design published in YouTube under 
this url: https://www.youtube.com/watch?v=SyWeex-S6d0

YouTube citation:
pixegami. (2022b, February 6). Build Wordle in Python • Word Game Python Project for Beginners. 
YouTube. https://www.youtube.com/watch?v=SyWeex-S6d0

GitHub citation:
PIXEGAMI. (n.d.). GitHub - pixegami/python-wordle: 
An implementation of Wordle in Python than can be played via the terminal. 
GitHub. https://github.com/pixegami/python-wordle





# Below is the original readme from the pixegami author
----------------------------------------------------------------------------------------------------------
# python-wordle
An implementation of Wordle in Python than can be played via the terminal.

## Bug Fix Update

It was pointed out to me that the game didn't behave like Wordle does when two identical letters
are in a 'guess', but only one copy of that letter is in the word.

### Problem

For example, if the guess is HELLO and the secret is APPLE, then the previous behavior causes
the first occurrence of the L to be yellow (because it does appear in the word), but then the second
L will be green (because it is in the right position).

On a letter-by-letter basis, this behavior appears fine. But when the entire word is considered, that
first L shouldn't appear yellow. Instead, it should appear grey. That's because there is already another
L in the guess that 'claims' the occurrence of the L in the secret.

### Solution

* Instead of resolving all the letter results in one-pass, we now first initialize it as an array and
default all guess letters to grey (not in the word).
* We create an list, which is a copy of the secret. Each element corresponds to the letter in the string. 
For example `["A", "P", "P", "L", "E"]`.
* We then do a first pass through the guess, and identify any letters in the correct position. If we find one,
then that letter becomes 'green', and the secret list is updated to void out that letter so it can't be used
in a subsequent comparison. So if we guess "HELLO", the remaining secret becomes something like this:
`["A", "P", "P", "*", "E"]`.
* We then do another loop this time identify the guessed letters which are in the word (by using a nested loop),
but not in position.

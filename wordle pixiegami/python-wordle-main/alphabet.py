# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:34:59 2022

@author: johnny
"""
import string
import numpy as np
#from functools import cache

import random
from wordle import Wordle
import re
from collections import namedtuple
import pandas as pd

alphabet = string.ascii_uppercase

def load_word_set(path: str):
    word_set = []
    with open(path, "r") as f:
        for line in f.readlines():
            word = line.strip().upper()
            word_set.append(word)
            word_set.sort()
    return word_set

# feedback function

# word_set = load_word_set("data/wordle_words.txt") # this is a 10k 5-letter word list 
#                                                     this is not representative of actual wordle game play
#
word_set = load_word_set("data/wordle_la.txt") # this is the reduced possible wordle word list

np_word_list = np.array(list(word_set))  # this makes the word_set into an np.array for my processing

secret = random.choice(list(word_set))
wordle = Wordle(secret)  # this launches the wordle game and provides the secret to the game
print(secret)  # this shows us the secret word

my_secret = wordle.secret  # this is the actual secret word from the wordle game instance that is running
my_guess = "STINT"  # this is my guess word for the feedback function

# this function needs to be provided a guess that is 5 letters 
# and a word set that is a numpy array list of 5 letter words. 
# This function can be provided a secret which is the secret word it is comparing the guess to
# The default for this function can get this secret from wordle.secret  secret=wordle.secret
# 
# this function has been written with default settings that can be overridden
# these function are the secret,np_word_list, printing, and my_return_complex
# 
# secret is used in the master agent game play to provide the game: secret=wordle.secret
# 
# np_word_list is the vocabulary list the function is working with: np_word_list=np_word_list 
#      you can provide a different list by specifying a new list: np_word_list=np_other_list
# 
# printing controls whether the debuging printing is done or not: printing =False can be set to true: printing=True
#
# my_return_complex controls the return function of the function: my_return_complex=False
# the default returns a size integer.  This is leveraged by an np.vectorize function that requires a simple output
# 


# the my_return_complex=True setting will return a namedtuple
# in this mode the return is a named tuple with these named tuples: 
# green_result,yellow_result,grey_list,not_green_list,regexstring_out,mylength,myregexresult
#
# 
# this is run like this:
# np_vocab_reduction = np.vectorize(feedback)
# mylengtharray = np_vocab_reduction(np_word_list,secret = my_secret,printing=False)
# mylengtharray[0:50]
#
# array([  1, 524,  59,   5, 172,  53, 207,  36, 284,  78, 357,  26,  12,
#          5, 459, 970,  76,  19, 208, 159, 237,   4, 169,  98, 103, 290,
#         53,  21, 212, 238,  68,  16, 126, 129, 172, 218, 145,  11, 228,
#          2,  84, 302, 116,  15,  13,  19, 146, 285,  24,  19])
#
# np_word_list[mylengtharray == 1]
# array(['SATIN', 'STERN', 'SALON', 'SLAIN', 'STRIP', 'STAIR', 'STEIN',
#        'PATSY', 'STINT', 'BASIC', 'SCANT', 'PATIO', 'STONE', 'FAINT',
#        'TRAIN', 'STANK', 'STAIN', 'SATYR', 'PAINT', 'SLANT', 'STAND',
#        'WAIST', 'STING', 'STONY', 'UNTIE', 'BASIS', 'STUNT', 'BASIL',
#        'BASIN', 'SAINT', 'STINK', 'STAID', 'UNTIL', 'TAINT', 'MASON',
#        'RATIO', 'ARTSY', 'TITAN', 'SNAIL', 'ANTIC', 'CABIN'], dtype='<U5')
#
# running this function in this way is done like this:
# my_results = feedback('bread',secret = my_secret,np_word_list=np_word_list,printing=True,my_return_complex=True)
#
# this provides the capability to run this kind of command:
# print(my_results.myregexresult)
# each of these results can be used: 
#      my_results.green_result                00100 
#      my_results.yellow_result               00001
#      my_results.grey_list                   ['B', 'R', 'E', 'D']
#      my_results.not_green_list              [0, 1, 2, 3, 4]
#      my_results.regexstring_out             (?=[^BRED][^BRED][^BRED][^ABRED][^BRED])(?=.*A.*)
#      my_results.mylength                    235
#      my_results.myregexresult               ['SATIN' 'FLASK' 'TAUNT' 'FLANK' 'SALVO' 'FAITH' 'AMITY' 'CAULK' 'LOAMY'
#                                             ...
#                                             'CANNY']

#@cache
copy_wordlist = np_word_list.copy()
def feedback(guess ,secret=my_secret, np_word_list=copy_wordlist,printing=False,my_return_complex=False):
    guess = guess.upper()
    if printing == True: 
        print("Top of the feedback function\n")
        print("secret",secret)
        print("guess",guess)
        print("np_word_list Hi Johnny",np_word_list)
        print("wordle.attempts",wordle.attempts ) 
    #secret = wordle.secret
            
    # this makes green results
    green_result = ""
    maskedword = ""
    myregexstring = [[],[],[],[],[]]

    for i in range(len(secret)):
        same = (guess[i] in secret[i])
        green_result += str(int(same))
        if same:
            maskedword += "*"
            myregexstring[i] = guess[i]
        else:
            maskedword += secret[i]
    if printing == True: print("maskedword",maskedword)
    if printing == True: print("green result",green_result)

    # This makes yellow results
    yellow_result = ""
    myisinstring = ""
    #myisinfstring = '(?=.*{}.*)'

    for i in range(len(maskedword)):
        isin = (guess[i] in maskedword)
        if isin:
            if printing == True: print(i,isin,guess,guess[i], myregexstring[i],type(myregexstring[i]))
            #myregexstring[i].append(guess[i])
            myregexstring[i] += guess[i]
            myisinstring += f'(?=.*{guess[i]}.*)'

        yellow_result += str(int(isin))
    if printing == True: print("yellow_result",yellow_result)

    # greylist is a list of letters that are not green and are not yellow
    # the idea is that the letter has not been filtered out
    # not_green_list is a list of positions that are not green

    grey_list = []
    not_green_list = []
    for i in range(len(yellow_result)):
        #print(green_result[i]== "0", yellow_result[i] == "0")
        if green_result[i] == "0":
            not_green_list.append(i)
        if green_result[i] == "0" and yellow_result[i] == "0" and guess[i] not in grey_list:
            if printing == True: print(guess[i])
            grey_list.append(guess[i])
        if printing == True: print(i,secret[i],guess[i],green_result[i],yellow_result[i],grey_list,not_green_list)
    if printing == True: print("grey_list",grey_list)
    if printing == True: print("not_green_list",not_green_list)


    # this builds a myregexstring that is used to produce a regular expression string
    # that is used to filter out words from the vocabulary list based on the restrictions of the wordle feedback

    for i in not_green_list:
        for grey in grey_list:
            if not grey in myregexstring[i]:
                myregexstring[i].append(grey)
    if printing == True: print("myregexstring",myregexstring)
    if printing == True: print("myisinstring",myisinstring)

    #wordlist_five

    finalregexstring = ""
    for i in myregexstring:
        if type(i) == list:
            list_string = "".join(i)
            f_list_string = "[^{}]".format(list_string)
            if printing == True: print("list_string",list_string,f_list_string)
            finalregexstring += f_list_string
        elif type(i) == str:
            finalregexstring += i
        if printing == True: print(i,type(i),str(i),finalregexstring)
    regexstring_out = "(?={}){}".format(finalregexstring,myisinstring)
    if printing == True: print("regexstring_out",regexstring_out)
    
    ### this is the original word set as a np array.
    ### the first use of this is to evaluate the reduction of the entire word set
    ### i'm commenting this out so that the word set can be provided to the function
    ### This provides a way to pass in a reduced data set
    #np_word_list = np.array(list(word_set))
    
    if printing == True: print("196 np_word_list",np_word_list,"type np_word_list",type(np_word_list))
    myregexresult = np_word_list[(list(map(lambda x: bool(re.match(regexstring_out,x)),np_word_list)))]
    if printing == True: print("198 myregexresult", myregexresult)
    mylength = len(myregexresult)
    if printing == True: print(mylength)
    #return(green_result,yellow_result,grey_list,not_green_list,regexstring_out,mylength,myregexresult)


    myresults = namedtuple("myresults",["green_result","yellow_result","grey_list","not_green_list","regexstring_out","mylength","myregexresult"])
    results = myresults(green_result,yellow_result,grey_list,not_green_list,regexstring_out,mylength,myregexresult)
    if my_return_complex == True:
        return(results)
    else:
        return(mylength)

alphabet = string.ascii_uppercase    
listabc=[c for c in alphabet]
npabc = np.array(listabc)

# alphabet frequency of vocabulary
# This function takes in a word list of vocabulary and returns a dataframe 
# with the frequency of each letter in the vocabulary by position
def alphabet_frequency(wordlist=np_word_list):
    global npabc
    global newdf
    newdf = pd.DataFrame(0, index=npabc, columns=range(5))

    for word in wordlist:
        for pos in range(len(word)):
            char = word[pos]
            newdf.at[char,pos] += 1
    return(newdf)

mydf = alphabet_frequency()


# Information Value iv function
# This function takes in a guess and evaluates the frequency value of each letter in the word 
# compared to the frequency of that letter in that position in the entire vocabulary, 
# returning the sum of the frequencies of the letters
# this function requires a guess and an input dataframe of the frequencies of letters in the vocabulary
def iv(guess,inputdf,printing=False):
    if printing == True: print(guess)
    if printing == True: print(inputdf)
    ivsum = 0
    for pos in range(len(guess)):
        char = guess[pos]
        val = inputdf.at[char,pos]
        if printing == True: print("char",char,"val",val)
        ivsum += val
    if printing == True: print("ivsumi",ivsum)
    return(ivsum)


# vocab_value 
# this function takes in a list of vocabulary words and a dataframe of letter frequencies
# this function creates a myIV_value_array numoy array which is a value score for every word in the vocabulary list
# the function then reads the words in the vocabulary list and looks the character and position up in the frequency df
# these scores are added up and stopred in a numpy array as a value score for each word in the vocabulary
# 
# this function returns results as a named tuple with four numpy arrays
# "myIV_value_array","sorter","sorted_myIV_value_array","sorted_np_word_list"
#
# myIV_value_array: an unsorted numpy array of the sum of frequency values of the words
# 
# Sorter is a sorted list of indexes.  This is used to sort the numpy array in descending order highest value first
#
# sorted_myIV_value_array is a sorted array of the sum of frequency values of the words
#
# sorted_np_word_list is a sorted array of teh vocabulary words based on the sum of frequency values
#
# this is an example of how to run this function
# myresults = vocab_value(np_word_list,mydf)
# print(myresults.sorter)
# print(myresults.sorted_myIV_value_array)
# print(myresults.sorted_np_word_list)
#
#



def vocab_value(np_word_list,inputdf=mydf,printing=False):
    myIV_value_array = np.zeros(len(np_word_list))
    if printing == True: print("myIV_value_array",myIV_value_array)
    for i in range(len(np_word_list)):
        word = np_word_list[i]
        val = iv(word,inputdf,printing=False)
        myIV_value_array[i]=val
    if printing == True: print(myIV_value_array)
    if printing == True: print(myIV_value_array.max())
    sorter = myIV_value_array.argsort()[::-1]
    sorted_myIV_value_array = myIV_value_array[sorter]
    sorted_np_word_list = np_word_list[sorter]
#    return(sorted_myIV_value_array,sorted_np_word_list)

    myresults = namedtuple("myresults",["myIV_value_array","sorter","sorted_myIV_value_array","sorted_np_word_list"])
    results = myresults(myIV_value_array,sorter,sorted_myIV_value_array,sorted_np_word_list)
    return(results)



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
#from collections import Counter

import time

import pickle

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
my_color_code_list = [] # this is a pass through color code list that provides a game history of color codes.  This is appended in the loop and is used to chain the decision tree game loops together
my_guess_list = [] # this is a pass through list of guesses.  This is appended in teh loop and returned in the complex results.

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
file_path = "data/dummy_file.txt"

myresults = namedtuple("myresults",["green_result","yellow_result",
                                    "regexstring_out","mylength","myregexresult","my_alphabet_df","zipped_lists","filecontent","my_color_code",
                                    "guess","secret","my_color_code_list","my_guess_list"])

def feedback(guess ,secret=my_secret, np_word_list=copy_wordlist,printing=False,my_return_complex=False,
             my_file_path = file_path, my_write = False,  mywrite_init = False,my_color_code_list = my_color_code_list,my_guess_list = my_guess_list):
    guess = guess.upper()
    my_guess_list = list(my_guess_list)
    my_guess_list.append(guess) 
    
    print("my_guess_list",my_guess_list,type(my_guess_list))

    secret = secret.upper()
    if printing == True: 
        print("Top of the feedback function\n")
        print("secret",secret)
        print("guess",guess)
        print("np_word_list Hi Johnny",np_word_list,len(np_word_list))
        print("wordle.attempts",wordle.attempts ) 
        print("my_file_path",my_file_path)
        print("my_write",my_write)
        print("mywrite_init",mywrite_init)
        print("my_color_code_list",my_color_code_list)
    #secret = wordle.secret
    '''         
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

    #for i in range(len(maskedword)):

    count = {}
    for i in range(len(secret)):
      count[guess[i]] = secret.count(guess[i])  
      
    for i in range(len(secret)):
        isin = (guess[i] in maskedword)
        #if isin:
        if guess[i] in maskedword:
            
            
            if printing == True: print("150",i,isin,guess,guess[i], myregexstring[i],type(myregexstring[i]))
            #myregexstring[i].append(guess[i])
            if guess[i] not in myregexstring[i]:
                myregexstring[i] += guess[i]
            if printing == True: print("153",i,isin,guess,guess[i], myregexstring[i],type(myregexstring[i]))
            myisinstring += f'(?=.*{guess[i]}.*)'
        # this is where the yellow result is built
        if isin and count[guess[i]] > 0:
            yellow_result += "1"
            count[guess[i]] -= 1
        else:
            yellow_result += "0"
        
    if printing == True: print("yellow_result",yellow_result)


    my_color_code = ""
    for i in range(len(green_result)):
        my_y = int(yellow_result[i])
        my_g = int(green_result[i])
        my_calc = my_y + my_g * 2
        if my_calc == 3: my_calc = 2
        my_code = str(my_calc)
        my_color_code += my_code
    if printing == True: print("my_color_code",my_color_code)
    
    my_color_code_list.append(my_color_code)

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
        if printing == True: print("for i in myregexstring: i",i)
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
    '''
    
    #(green_result,yellow_result,regexstring_out,my_color_code,my_color_code_list) = color_codes_regular_expressions(guess,secret,my_color_code_list,printing=printing)
    
    #regexstring_out = color_codes_regular_expressions(guess,secret,printing == printing)
    
    
    
    
    
    if printing == True: print("inside color_codes_regular_expressions","my_color_code_list",my_color_code_list)
    yellow_result = ""
    grey   = ""
    green_result  = ""
    guess_count = {}
    secret_count = {}
    yellow_count = {}
    myregexstring = [["^"],["^"],["^"],["^"],["^"]]
    myisinstring = ""
    if printing == True: print("1 myregexstring",myregexstring)
    for letter in set(guess):
        guess_count[letter] = guess.count(letter)
        yellow_count[letter] = 0
    if printing == True: print("guess_count",guess_count)   
    for letter in set(secret):
        secret_count[letter] = secret.count(letter)
    if printing == True:    
        print("secret_count",secret_count)
        print("yellow_count",yellow_count )
    for i in range(len(secret)):
        #green
        if printing == True: print("2 myregexstring",myregexstring)
        if guess[i] == secret[i] :
            green_result += "1"
            if guess[i] not in myregexstring[i]:
                myregexstring[i] = guess[i]  # this places the green letter in the regex string if the letter is green
        else:
            green_result += "0"
        if printing == True: print("3 myregexstring",myregexstring)
        #yellow
        yellow_count[guess[i]] += 1  # this solves the double letter yellow problem
        if guess[i] in secret and yellow_count[guess[i]] <= secret_count[guess[i]] :
            yellow_result += "1"
            myisinstring += f'(?=.*{guess[i]}.*)'
            if guess[i] not in myregexstring[i]:
                myregexstring[i] += guess[i]
        else:
            yellow_result += "0"
        if printing == True: print("4 myregexstring",myregexstring)
        #grey
        if guess[i] not in secret and guess[i] not in grey:
            grey += guess[i]


    for letter in grey:
        for i in range(len(guess)):
            if "^" in myregexstring[i]:
                myregexstring[i] += letter
    if printing == True: print("5 myregexstring",myregexstring)
    #regexstring_out = "(?={}){}".format(myregexstring,myisinstring)


    if printing == True:
        print(i,secret[i],guess[i],green_result[i],yellow_result[i])
        print("yellow_count",yellow_count )  
        print("green_result",green_result)
        print("yellow_result",yellow_result)
        print("grey", grey)
        print("myregexstring",myregexstring)
        print("myisinstring",myisinstring)
        #print("regexstring_out",regexstring_out)
    finalregexstring = ""
    for i in myregexstring:
        if printing == True: print("for i in myregexstring: i",i)
        if type(i) == list:
            list_string = "".join(i)
            f_list_string = "[{}]".format(list_string)        # this puts the hat in the regular expression
            if printing == True: print("list_string",list_string,f_list_string)
            finalregexstring += f_list_string
        elif type(i) == str:
            finalregexstring += i
        if printing == True: print(i,type(i),str(i),finalregexstring)
    regexstring_out = "(?={}){}".format(finalregexstring,myisinstring)
    if printing == True: print("regexstring_out",regexstring_out)

    regexstring_out = regexstring_out.replace('[^]','[\S]')
    if printing == True: print("regexstring_out",regexstring_out)
    
    # color_code_processing
    my_color_code = ""
    for i in range(len(green_result)):
        my_y = int(yellow_result[i])
        my_g = int(green_result[i])
        my_calc = my_y + my_g * 2
        if my_calc == 3: my_calc = 2
        my_code = str(my_calc)
        my_color_code += my_code
    if printing == True: print("my_color_code",my_color_code,type(my_color_code))
    
    if printing == True: print("my_color_code_list",my_color_code_list,type(my_color_code_list),len(my_color_code_list))
    
    my_color_code_list.append(my_color_code)
    
    
    
    
    
    ### this is the original word set as a np array.
    ### the first use of this is to evaluate the reduction of the entire word set
    ### i'm commenting this out so that the word set can be provided to the function
    ### This provides a way to pass in a reduced data set
    #np_word_list = np.array(list(word_set))
    
    if printing == True: print("np_word_list",np_word_list,"type np_word_list",type(np_word_list))
    if printing == True: print("regexstring_out",regexstring_out)
    if printing == True: print("np_word_list",np_word_list,len(np_word_list))
    myregexresult = np_word_list[(list(map(lambda x: bool(re.match(regexstring_out,x)),np_word_list)))]
    if printing == True: print("myregexresult", myregexresult)
    mylength = len(myregexresult)
    if printing == True: print(mylength)
    #return(green_result,yellow_result,grey_list,not_green_list,regexstring_out,mylength,myregexresult)

    # This section works the alphabet frequency result set
    # my_alphabet_df is a dataframe of the alphabet frequency of the word list by character position
    my_alphabet_df = alphabet_frequency(myregexresult)
    # my_vocab_value_results is a named tuple from the vocab value function returning a sorted list of words with the highest letter value first
    my_vocab_value_results = vocab_value(myregexresult,my_alphabet_df)
    # the zipped list is a sorted list in a dictionary format of the words in letter value order
    zipped_lists = my_vocab_value_results.zipped_lists
    if printing == True: print("zipped_lists",list(zipped_lists.items())[:10])
    
    # this secti0on establishes the named tuple content for the return results
    
    # myresults = namedtuple("myresults",["green_result","yellow_result","grey_list","not_green_list","regexstring_out","mylength","myregexresult","filecontent"])
    # this named tupple was moved outside the function because it has to be outside to use it in the pickle function otherwise the pickle breaks
    filecontent =  ""
    results = myresults(green_result,yellow_result,regexstring_out,mylength,myregexresult,my_alphabet_df,zipped_lists,filecontent,my_color_code,guess,secret,my_color_code_list,my_guess_list)
    
    # file processing for feedback file
    
    if printing == True: print(results)
    
    # This section writes the data to the my_file_path file
    if my_write == True:
        if mywrite_init == True:
            filecontent = write_guessing_agent_feedback_file(my_file_path,results,initialize =True)
            print("init loop")
        else:
            print("append loop")
            filecontent = write_guessing_agent_feedback_file(my_file_path,results,initialize =False)
        
        #results = myresults(green_result,yellow_result,grey_list,not_green_list,regexstring_out,mylength,myregexresult,filecontent)
        results = myresults(green_result,yellow_result,regexstring_out,mylength,myregexresult,my_alphabet_df,zipped_lists,filecontent,my_color_code,guess,secret,my_color_code_list,my_guess_list)
    
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
    zipped_lists = dict(zip(sorted_np_word_list,sorted_myIV_value_array))

    myresults = namedtuple("myresults",["myIV_value_array","sorter","sorted_myIV_value_array","sorted_np_word_list","zipped_lists"])
    results = myresults(myIV_value_array,sorter,sorted_myIV_value_array,sorted_np_word_list,zipped_lists)
    return(results)

def write_guessing_agent_feedback_file(File_path,my_results,initialize =False):
    solved = int(my_results.guess == my_results.secret)
       
    my_guess_list = my_results.my_guess_list
    my_color_code_list = my_results.my_color_code_list
    guess_color_dict = dict(zip(my_guess_list, my_color_code_list))
    
    row = {"guess":my_results.guess,"secret":my_results.secret,"length_of_results":my_results.mylength,"colorcode":my_results.my_color_code,"guess_list":my_results.my_guess_list,"my_color_code_list":my_results.my_color_code_list,"guess_color_dict":guess_color_dict,"solved":solved}
    #row = {"guess":my_results.guess,"secret":my_results.secret,"length_of_results":my_results.mylength,"colorcode":my_results.my_color_code,"guess_list":my_results.my_guess_list,"solved":solved}
    my_columns = list(row.keys())
    dfline = pd.DataFrame([row],columns=my_columns)
    if initialize == True:
        dfline.to_pickle(File_path)
        #f = open(File_path , "wb")
        #pickle.dump(dfline, f)
        #f.close()
        print("initial loop write",dfline)
    else:
        unpickled_df = pd.read_pickle(File_path)
        #unpickled_df = unpickled_df.append(row,ignore_index=True)
        unpickled_df = pd.concat([unpickled_df,dfline], axis=0, ignore_index=True)
        unpickled_df.to_pickle(File_path)
        #f = open(File_path , "ab+")
        #pickle.dump(dfline, f)
        #f.close()
        print("append loop write",dfline)
    #time.sleep(.001)
    #unpickled_df = pd.read_pickle(File_path)
    #my_data = read_guessing_agent_feedback_file(File_path)
    return("thanks")
    
    


def read_guessing_agent_feedback_file(File_path):
    my_data = []
    with open(File_path, "rb")as f:
        try:
            while True:
                my_data.append(pickle.load(f))
        except EOFError:
            pass
    return(my_data)


output_word_list = []
file_name = ""

def vocab_length(my_word_list = output_word_list,save_to_file = False, my_filename = file_name,printing = False):
    my_df = pd.DataFrame()
    if printing == True : 
        print(my_word_list)
        print(type(my_word_list))
        print()
    
    for i in range(len(my_word_list)):
        my_secret = my_word_list[i]
        if printing == True : print(my_secret)
        #mylengtharray = np_vocab_reduction(wordlist, my_secret,copy_wordlist, True,False)

        # This is breaking. This is supposed to provide an array of all of the guesses against the secret word.  
        # but the np.vectorize is bringing in the np_word list as the guess as a single element array
        # rather than the full list
        #mylengtharray = np_vocab_reduction(output_word_list,secret = my_secret,np_word_list=output_word_list,printing=True)
        mylengthlist = []
        for my_guess in my_word_list:

            my_result = feedback(my_guess,secret = my_secret,np_word_list=my_word_list,printing=False,my_return_complex=False)
            #if printing == True : print(my_result)
            mylengthlist.append(my_result)
        if printing == True : print(mylengthlist)
        
        dfline = pd.DataFrame([mylengthlist],index=[my_secret],columns=my_word_list)
        if printing == True: print(dfline)
        my_df = pd.concat([my_df,dfline])
        if printing == True : print(my_df)
        if printing == True :  print("len mylengthlist",len(mylengthlist),"dfline",dfline)
        if save_to_file == True:
            if i == 0:
                dfline.to_csv(file_name, mode='w')
            else:
                dfline.to_csv(file_name, mode='a',header=False)
            
    return(my_df)

import json

with open('data/decision_trees/slate.tree.total.js') as dataFile:
    data = dataFile.read()
    obj = data[data.find('{') : data.rfind('}')+1]
    jsonObj = json.loads(obj)

my_color_code_list = []

def decision_tree_jsonObj(my_color_code_list):
    if not "22222" in my_color_code_list:
        my_color_code_list_length = len(my_color_code_list)
        print("my_color_code_list",my_color_code_list,"my_color_code_list_length",my_color_code_list_length)
        if my_color_code_list_length == 1:
            print("inside 1")
            color_code1 = my_color_code_list[0]
            if type(jsonObj["map"][color_code1]) == dict:
                guess = jsonObj["map"][color_code1]['guess']
            elif type(jsonObj["map"][color_code1]) == str:
                guess = jsonObj["map"][color_code1]
        elif my_color_code_list_length == 2:
            color_code1 = my_color_code_list[0]
            color_code2 = my_color_code_list[1]
            if type(jsonObj["map"][color_code1]["map"][color_code2]) == dict:
                guess = jsonObj["map"][color_code1]["map"][color_code2]['guess']
            elif type(jsonObj["map"][color_code1]["map"][color_code2]) == str:
                guess = jsonObj["map"][color_code1]["map"][color_code2]
        elif my_color_code_list_length == 3:
            color_code1 = my_color_code_list[0]
            color_code2 = my_color_code_list[1]
            color_code3 = my_color_code_list[2]
            if type(jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]) == dict:
                guess = jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]['guess']
            elif type(jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]) == str:
                guess = jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]
        elif my_color_code_list_length == 4:
            color_code1 = my_color_code_list[0]
            color_code2 = my_color_code_list[1]
            color_code3 = my_color_code_list[2]
            color_code4 = my_color_code_list[3]
            if type(jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]) == dict:
                guess = jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]['guess']
            elif type(jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]) == str:
                guess = jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]
        elif my_color_code_list_length == 5:
            color_code1 = my_color_code_list[0]
            color_code2 = my_color_code_list[1]
            color_code3 = my_color_code_list[2]
            color_code4 = my_color_code_list[3]
            color_code5 = my_color_code_list[4]
            if type(jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]["map"][color_code5]) == dict:
                guess = jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]["map"][color_code5]['guess']
            elif type(jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]["map"][color_code5]) == str:
                guess = jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]["map"][color_code5]
        elif my_color_code_list_length == 6:
            color_code1 = my_color_code_list[0]
            color_code2 = my_color_code_list[1]
            color_code3 = my_color_code_list[2]
            color_code4 = my_color_code_list[3]
            color_code5 = my_color_code_list[4]
            color_code6 = my_color_code_list[5]
            if type(jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]["map"][color_code5]["map"][color_code6]) == dict:
                guess = jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]["map"][color_code5]["map"][color_code6]['guess']
            elif type(jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]["map"][color_code5]["map"][color_code6]) == str:
                guess = jsonObj["map"][color_code1]["map"][color_code2]["map"][color_code3]["map"][color_code4]["map"][color_code5]["map"][color_code6]
        else:
            guess = "not_found"
        guess = guess.upper()
    else:
        guess = "Game_won"
    return(guess)

def color_codes_regular_expressions(guess,secret,my_color_code_list,printing=False):
    #global    green_result,yellow_result,grey_list,not_green_list,regexstring_out,my_color_code,my_color_code_list,guess,secret 
    my_color_code_list.append("wilma")
    if printing == True: print("inside color_codes_regular_expressions","my_color_code_list",my_color_code_list)
    yellow_result = ""
    grey   = ""
    green_result  = ""
    guess_count = {}
    secret_count = {}
    yellow_count = {}
    myregexstring = [[],[],[],[],[]]
    myisinstring = ""

    for letter in set(guess):
        guess_count[letter] = guess.count(letter)
        yellow_count[letter] = 0
    if printing == True: print("guess_count",guess_count)   
    for letter in set(secret):
        secret_count[letter] = secret.count(letter)
    if printing == True:    
        print("secret_count",secret_count)
        print("yellow_count",yellow_count )
    for i in range(len(secret)):
        #green
        if guess[i] == secret[i] :
            green_result += "1"
            myregexstring[i] = guess[i]  # this places the green letter in the regex string if the letter is green
        else:
            green_result += "0"
        #yellow
        yellow_count[guess[i]] += 1  # this solves the double letter yellow problem
        if guess[i] in secret and yellow_count[guess[i]] <= secret_count[guess[i]] :
            yellow_result += "1"
            myisinstring += f'(?=.*{guess[i]}.*)'
            myregexstring[i] += guess[i]
        else:
            yellow_result += "0"
        #grey
        if guess[i] not in secret and guess[i] not in grey:
            grey += guess[i]


    for letter in grey:
        for i in range(len(guess)):
            myregexstring[i] += letter

    #regexstring_out = "(?={}){}".format(myregexstring,myisinstring)


    if printing == True:
        print(i,secret[i],guess[i],green_result[i],yellow_result[i])
        print("yellow_count",yellow_count )  
        print("green_result",green_result)
        print("yellow_result",yellow_result)
        print("grey", grey)
        print("myregexstring",myregexstring)
        print("myisinstring",myisinstring)
        #print("regexstring_out",regexstring_out)
    finalregexstring = ""
    for i in myregexstring:
        if printing == True: print("for i in myregexstring: i",i)
        if type(i) == list:
            list_string = "".join(i)
            f_list_string = "[^{}]".format(list_string)        # this puts the hat in the regular expression
            if printing == True: print("list_string",list_string,f_list_string)
            finalregexstring += f_list_string
        elif type(i) == str:
            finalregexstring += i
        if printing == True: print(i,type(i),str(i),finalregexstring)
    regexstring_out = "(?={}){}".format(finalregexstring,myisinstring)
    if printing == True: print("regexstring_out",regexstring_out)
    
    # color_code_processing
    my_color_code = ""
    for i in range(len(green_result)):
        my_y = int(yellow_result[i])
        my_g = int(green_result[i])
        my_calc = my_y + my_g * 2
        if my_calc == 3: my_calc = 2
        my_code = str(my_calc)
        my_color_code += my_code
    if printing == True: print("my_color_code",my_color_code,type(my_color_code))
    
    my_color_code_list.append("pebbles")
    if printing == True: print("my_color_code_list",my_color_code_list,type(my_color_code_list),len(my_color_code_list))
    
    my_color_code_list.append(my_color_code)
    
    return(green_result,yellow_result,regexstring_out,my_color_code,my_color_code_list)
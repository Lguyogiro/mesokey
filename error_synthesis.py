
import random
import re
import torch

# The samples below are from the K'iche' treebank to be used in trouble shooting
quc_sent_sample = ["man katkowin taj katchakunik we man k'o ta ri ajilab'al", "chiq'ij kchukun ri lu' ruk' ratz", "ri ajtij kyajon chi kech ri ak'alab'"]
quc_char_list = ["b","k","c","h","l","m","n","o","q","r","s","t","z","w","x","y","a","e","i","o","u","'"]

'''
This scipt includes 6 functions for generating errors - deletion, insertion, transposition
random_substitution, word_fussing, word_splitting.
There's a 7th error generation function, bigram substitution, which is in a separate script. 
Each function take a list of "gold standard" sentences. 
Insertion, random substitution, and bigram substitution require a character list.
The character list can be generated from the input (not included in this script).
Each function creates one error per sentence.
Each sentence will be run through all the functions, 
meaning there's multiple copies of each sentence in the output, 
but each with a different error type in a new random location within the sentence.
There is an issue that some of the random errors can create other legal words 
also know as real-word errors, which means that down the line
the error detection function (not included in this script) 
will not find any errors within the sentence.
Note that spell checkers based on edit distance cannot handle word fussing or word splitting errors.
'''

def deletion(txt):
    '''
    Function to randomly choose a character in a random word to delete
    '''
    # create list to store sentences after a charcter has been deleted
    noisy_sents = []
    # iterate through the sentences in the input list of sentences
    for s in txt:
        # generate random number within the range of the sentence length to use as character index
        random_sent_index = random.randrange(len(s))
        # if the random char is a space try another index until false
        while s[random_sent_index].isspace():
            random_sent_index = random.randrange(len(s))
        # slice at index, then rejoin without char to delete that character
        noisy_sent = s[: random_sent_index] + s[random_sent_index + 1:]
        # add the sentence with added noise to list of noisy sentences
        noisy_sents.append(noisy_sent)
    # print list of noisy sentences
    #print("deletion error:", noisy_sents)

    # return list with noisy sentences
    return noisy_sents

#deletion(quc_sent_sample) 

def insertion(txt, char_list):
    '''
    Function to insert random character from character list into random word with random placement
    '''
    # create list to store sentences after a charcter has been deleted
    noisy_sents = []
    # iterate through the sentences in the input list of sentences
    for s in txt:
        # generate random number within the range of the sentence length to use as character index
        random_sent_index = random.randrange(len(s))
        # randomly choose letter from the list of characters for that language
        random_char = random.choice(char_list)
        # slice at index, then rejoin with inserted char
        noisy_sent = s[: random_sent_index] + random_char + s[random_sent_index:]
        # append list with noise to noisy sentence list
        noisy_sents.append(noisy_sent)
    # print list of noisy sentences
    #print("insertion errors:", noisy_sents)

    # return list with noisy sentences
    return noisy_sents

#insertion(quc_sent_sample, quc_char_list)

def transposition(txt):
    '''
    Function to randomly choose 2 consecutive letters in a random word
    to switch places, aka transposition
    '''
    # create list to store sentences with added noise
    noisy_sents = []
    # iterate through the sentences in the input list of sentences
    for s in txt: 
        # get sentence range minus 1 to avoid "string index out of range" for adjacent character 
        sent_range = len(s) - 1
        # generate random number within the range of the sentence length to use as character index
        random_sent_index = random.randrange(sent_range)
        # check that random character and the following characters are not spaces
        # try until false
        while s[random_sent_index].isspace() or s[random_sent_index + 1].isspace():
            random_sent_index = random.randrange(sent_range) 
        # assign variable to adjacent char
        adjacent_char = random_sent_index + 1
        # swap the two characters
        transposed_chars = (s[adjacent_char] + s[random_sent_index])
        # slice at index, then rejoin with the tansposed charaters
        noisy_sent = s[: random_sent_index] + transposed_chars + s[random_sent_index + 2:]
        # add noisy sentence to list 
        noisy_sents.append(noisy_sent)
    # print list of noisy sentences
    #print("transposition errors:", noisy_sents)

    # return list of noisy sentences
    return noisy_sents

#transposition(quc_sent_sample)

def random_substitution(txt, char_list):
    '''
    Function to randomly substitute a letter in one word per sentence with a random 
    character from a list of language specific characters
    '''
    # create list to store sentences after a character has been substituted
    noisy_sents = []
    # iterate through the sentences in input list of sentences
    for s in txt:
        # randomly choose a character from the list of language specific characters
        random_char = random.choice(char_list)
        # generate random number within the range of the sentence length to use as index
        random_sent_index = random.randrange(len(s))
        # if the random char index in the sentence is a space or if it's the same character
        # as the random replacement character chosen from the character list, rerun until both are false 
        while s[random_sent_index].isspace() or s[random_sent_index] == random_char:
            random_sent_index = random.randrange(len(s)) 
        # slice at index, then rejoin with substituted char
        noisy_sent = s[: random_sent_index] + random_char + s[random_sent_index + 1:]
        # add sentence with noise to the list of noisy sentences
        noisy_sents.append(noisy_sent)
    # print list of noisy sentences
    #print("random substitution errors:", noisy_sents)
    # return list of noisy sentences
    return noisy_sents

#random_substitution(quc_sent_sample, quc_char_list)

def word_fussing(txt):
    '''
    Function to remove space between two words to fuse them
    '''
    # create list to store noisy sentences
    noisy_sents = []
    # iterate through the sentences in the input list of sentences
    for s in txt:
        # generate random number within the range of the sentence length for index
        random_sent_index = random.randrange(len(s))
        # if the random char not a space (False) rerun for randon index until isspace is true 
        while s[random_sent_index].isspace() is False:
            random_sent_index = random.randrange(len(s))
        # slice at index, then rejoin without space
        noisy_sent = s[: random_sent_index] + s[random_sent_index + 1:]
        # append sentence with noise to list
        noisy_sents.append(noisy_sent)
    # print list of noisy sentences
    #print("word fussing errors:", noisy_sents)

    # return list of noisy sentences
    return noisy_sents

#word_fussing(quc_sent_sample)

def word_splitting(txt):
    '''
    Function to insert a space in one word per sentence to make a word splitting error
    '''
    # make list to store noisy sentences
    noisy_sents = []
    # iterate through the list of input sentences
    for s in txt:
        '''
        give variable name to the character length of the sentence
        don't include final character of the sentence 
        since that would add a space to the end of the sentence instead of splitting word
        '''
        sent_range = len(s) - 1
        # generate random number within the range of the sentence length for index
        random_sent_index = random.randrange(sent_range)
        # check that random character and the following characters are not spaces
        while s[random_sent_index].isspace() or s[random_sent_index + 1].isspace():
            # if .isspance is true keep trying new index
            random_sent_index = random.randrange(sent_range)
        # slice at index, then rejoin with inserted space
        noisy_sent = s[:random_sent_index] + " " + s[random_sent_index:]
        # append list with noise to list
        noisy_sents.append(noisy_sent)
    # print list of noisy sentences
    #print("word splitting errors:", noisy_sents)

    # return list of noisy sentences
    return noisy_sents

#word_splitting(quc_sent_sample)

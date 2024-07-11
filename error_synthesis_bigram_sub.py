import random

# the following 3 lines are data samples used during development
#treebank_toks = open("/Users/wing/Dropbox/dissertation/data/quc_treebank/quc_treebank_toks.txt", "r").readlines()
#sent_sample = ["man katkowin taj katchakunik we man k'o ta ri ajilab'al", "chiq'ij kchukun ri lu' ruk' ratz", "ri ajtij kyajon chi kech ri ak'alab'"]
#quc_character_list = ["b","k","c","h","l","m","n","o","q","r","s","t","z","w","x","y","a","e","i","o","u","'"]

'''
This script includes has two functions one for creating a probability dictionary, which contains the probabilities 
of each letter given the previous letter, and one for error synthesis based on bigram substitution. 
'''


def probability_dict(toks, char_list):
    '''
    Function to create probability dictionary for each letter given the preceding letter
    The function takes a list of tokens and a list of characters
    '''

    # create dictionary for bigram frequencies
    bigram_dict = {}
    # create dictionary for bigram probabilities
    bigram_prob_dict = {}

    # iterate through tokens and remove trailing spaces
    for t in toks:
        # strip trailing spaces in list of toks
        t = t.strip()
    
        # get bigrams and bigram count
        # get sentence range minus 1 to avoid "string index out of range" for adjacent character 
        for i in range(len(t) - 1):
            # get adjacent character for character bigram
            bigram = t[i], t[i + 1]
            # check if bigram in bigram_dict
            if bigram not in bigram_dict:
                # if bigram not in bigram_dict add bigram to dict with a count of 1
                bigram_dict[bigram] = 1
            else:
                # if bigram is in bigram_dict add 1 to count
                bigram_dict[bigram] += 1
    #print(bigram_dict)

    # iterate through character list
    for char in char_list:
        # create a dictionary to temp hold the bigrams for the given character
        temp_bigram_dict = {}
        #create dictionary to temp hold the prob of the given character
        temp_prob_dict = {}
        #iterate through the keys in the bigram dict
        for bi in bigram_dict.keys():
            # if the char from the list is the same as the initial char in a bigram add that bigram to temp bigram dict
            if char == bi[0]:
                temp_bigram_dict[bi[1]] = bigram_dict.get(bi)
                #print("char",char)
                #print("bi", bi)
                #print("bigram", bigram_dict.get(bi))
        # get the char frequency by getting the sum of the values from the temp_bigram_dict
        char_freq = sum(temp_bigram_dict.values())
        #print("unigram freq", char_freq)
        #print(temp_bigram_dict)
        # iterate through temp_bigram_dict
        for key, value in temp_bigram_dict.items():
            # divide the freq of each key by the total freq
            temp_prob_dict[key] =  round(value / char_freq, 4)
        #print(temp_prob_dict)
        '''
        append the character as the key and a dictionary of bigrams 
        for that give character with the probability of said bigram
        as the value
        '''
        bigram_prob_dict[char] = temp_prob_dict  
    #print(bigram_prob_dict) 
    return bigram_prob_dict

#b_prob_dict = probability_dict(treebank_toks, quc_character_list)

def substitution_with_bigrams(txt, bigram_probability_dict, char_list):
    '''
    Function to create substitution errors in gold standard text based on bigram probabilities 
    '''
    # create list to store noisy sentences
    noisy_sents = []
    # iterate through the sentences in the input list of sentences
    for s in txt: 
        # get sentence range minus 1 to avoid "string index out of range" for adjacent character 
        sent_range = len(s) - 1
        # generate random number within the range of the sentence length to use as character index
        random_sent_index = random.randrange(sent_range)
        # check that random character and the following character is also not a space
        # otherwise try again
        while s[random_sent_index].isspace() or s[random_sent_index + 1].isspace():
            random_sent_index = random.randrange(sent_range) 
        # assign bigram variable for the randomly chosen char and its adjacent char aka the bigram
        bigram = s[random_sent_index], s[random_sent_index + 1]
        #print(bigram)
        # pull the embedded dictionary of bigrams for a given character (first character in the chosen bigram)
        possible_bigram_sub_dict = bigram_probability_dict.get(bigram[0])
        # create a list to temp hold the qualifiying bigram substitutions for a give bigram
        possible_bigram_sub_list = []
        #print(possible_bigram_sub_dict)

        # iterate through entries
        for i in possible_bigram_sub_dict:
            #print(i)
                # find bigram sub above 5% possibility that's not the current bigram
                if possible_bigram_sub_dict[i] >= .05 and i is not bigram[1]:
                    # if they meet criteria append to list of possible bigram substitutions 
                    possible_bigram_sub_list.append(i)
                # if a bigram sub above 5% accept any bigram that's not the current bigram
                elif i is not bigram[1]:
                    possible_bigram_sub_list.append(i)
                else:
                    # if the bigram has no alternatives then randomly choose a char from the char list
                    # this is to avoid errors from special characters in the sents that make it through processing
                    random_char = random.choice(char_list)
                    possible_bigram_sub_list.append(random_char)
        #print(possible_bigram_sub_list)
        # name variable for new bigram
        bigram_sub_choice = bigram[0] + random.choice(possible_bigram_sub_list)
 
        #print(bigram_sub_choice)
        #slice sentence at index and rejoin with new bigram
        noisy_sent = s[: random_sent_index] + bigram_sub_choice + s[random_sent_index + 2:]
        noisy_sents.append(noisy_sent)
    #print(noisy_sents)
    return noisy_sents

#substitution_with_bigrams(sent_sample, b_prob_dict, quc_character_list)        

    
'''
Synonym Text Parser
By Connal De Souza and David Wang
The performance using the two novels is : 70.0%
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 2.
    
    Parameters: vec -- a vector (string)
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:       
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity of sparse vectors vec1 and vec2,
    stored as dictionaries as described in the handout for Project 2.
    
    Parameters: vec1, vec2 -- vectors (strings)
    '''
    
    dot_product = 0.0  # floating point to handle large numbers
    for x in vec1:
        if x in vec2:
            dot_product += vec1[x] * vec2[x]
    
    return dot_product / (norm(vec1) * norm(vec2))


def get_sentence_lists(text):
    
    '''Return a list containing lists of strings; each list corresponds to each
    sentence, and contains the individual words in each sentence. All elements
    are returned lower case.
    
    Parameters: text -- a string containing a sentence
    '''    
    
    
    sentences = []          # empty list; we we append the elements of the sentences here
    
    text = text.lower()     # we need everything to be lower case
    word = ''               # empty string; we'll be looking at this below to see between words
    s = []                  # another empty list; work space
    word_breaks = [' ', ',', '-', ':', ';', '\'', '\"', '\n', '(', ')']     # indicates what breaks a word
    sent_breaks = ['.', '?', '!']                                           # indicates what breaks a sentence 
    for i in range (len(text)):                                             # we loop through the string given
        
        char = text[i]                                                      # through every element
        
        if char in word_breaks:                                             
        #if text[i] == ' ' or text[i] == ',' or text[i] == '-' or text[i] == ':'\
        #   or text[i] == ';' or text[i] == '\n' or text[i] == '\'' \
        #   or text[i] == '\"':
            if word != '':                                                  # if not empty. add the word into s
                s.append(word)                                              
                word = ''                                                   # reset empty string
        
        elif char in sent_breaks:                                           # elements in sentence breaks
            if word != '':                                                  # see above
                s.append(word)                                              # append into word
            word = ''
            if s != []:                                                     # above
                sentences.append(s)                                         # into s again
            s = []
            
        else:
            word += char                                                    # elongate; adds char to existing word
            
                
        
    return sentences                                                        # result
        


def get_sentence_lists_from_files(filenames):
    
    '''Return (in order) a list of every sentence contained in all the text 
    files in filenames. Format is the same as list returned from 
    "get_sentence_lists(text)".
    
    Parameters: filenames -- a list of strings, each one the name of a text file
    '''
    
    all_sentences = []                          #empty list; we'll add elements to this VIA a loop after reading

    for i in range (len(filenames)):                                        # this loops through all the files
        
        file = open(filenames[i], 'r')                                      # open files
        words = str(file.read())                                            # read; conversion
        all_sentences.append(get_sentence_lists(words))                     # append the list 
        
    return all_sentences                                                    # result


def build_semantic_descriptors(sentences):
    
    '''Return a dictionary d. Every key, w, is a word that appears in one of the 
    sentences, and has a corresponding value d[w], which itself is a dictionary 
    representing the semantic descriptor of w (see assignment page).
    
    Parameters: sentences -- a list containing lists of strings representing 
    sentences
    '''
    
    d = {}                                                                  # create empty dictionary; elements appended later
    
    for i in range (len(sentences)):                                        # loop for all sentence
        #print('i' + str(i))
        for j in range(len(sentences[i])):      # nest loop; this goes through the elements within the elements of the sentence list
            #print(j)
            #word = sentences[i][j]
            if not(sentences[i][j] in d):       # if it's not in
                
                d2 = {}                         # empty dictionary (second one)
                for k in range (len(sentences)):                            # loop through all elements; nested loop
                    if(sentences[i][j] in sentences[k]):                    # if the element looped through i/j and in element for k
                      
                        for l in range(len(sentences[k])):                  # nested loop; check for length of previous loop; arg l
                        
                        #word2 = sentences[k][l]
                        
                            #if sentences[i][j] != sentences[k][l]:
                            if not(sentences[k][l] in d2):                  # if the element if not in d2
                                d2[sentences[k][l]] = 1                     # we set to 1; keep
                            else:                                           # otherwise
                                d2[sentences[k][l]] += 1                    # count +1
                        
                if sentences[i][j] in d2:                                   # if itès already there,
                    del[d2[sentences[i][j]]]                                # delete
                           
                d[sentences[i][j]] = d2                                     # 
            
               
                
    return d
    
    
    
def most_similar_word(word, choices, semantic_descriptors):
    
    '''Return an element of choices with the largest semantic 
    similarity (computed using the above function) to word. If the similarity 
    cannot be computed, return -1. In the case of a tie, return the element of 
    choices with the smallest index. 
    
    Parameters: word -- a string
                choices -- a list of string
                semantic_descriptors -- a dictionary
    '''    
    
    d = {}          # empty dictionary
    if not(word in semantic_descriptors):   # 
        return choices[0]                   # first element in choices list
    
    for i in range (len(choices)):
        if choices[i] in semantic_descriptors:
            d[choices[i]] = cosine_similarity(semantic_descriptors[word],\
                                              semantic_descriptors[choices[i]])
        else:
            d[choices[i]] = -1
            
    keys = list(d.keys())                   # create a list of keys from dict.
    values = list(d.values())               # create a list of values from dict.
    
    high_score = 0                          # set start = 0
    high_score_index = 0                    # set start = 0
    
    for i in range (len(choices)):          
        
        if values[i] > high_score:          # if the element is > h.s
            high_score_index = i            # make it the new h.s
            high_score = values[i]          # cont above
            
    return keys[high_score_index]           # returns the key corresponding to 
                                            # the h.s
    
    

def run_similarity_test(filename, semantic_descriptors):
    
    '''Return a percentage of questions on which most_similar_word() guesses the 
    answer correctly using the semantic descriptors stored in 
    semantic_descriptors.

    Parameters: filename -- a string in the form of a file in the format .txt
                semantic_descriptors -- a dictionary as described above
    '''
    
    file = open(filename, 'r')          #
    total = 0                           # setting up base lines (0) and 
    correct = 0                         # setting up file; read format
    lines = file.readlines()            #
    
    for i in range (len(lines)):
        
        total += 1
        
        words = lines[i].split()
        choices = words[2: len(words)]
        answer = most_similar_word(words[0], choices, semantic_descriptors)
        if answer == words[1]:              # if comparison True
            correct += 1                    # count += 1
    return (correct / total) * 100          # rudimentary fraction; count over total amount                                      

'''if __name__ == '__main__':
    
    b1 = open('War and Peace.txt', 'r')
    b2 = open('Swan\'s Way.txt', 'r')
    text = 'Hello, Jack. How is it going? Not bad; pretty good actually...\
    Very very good in fact .'
    
    text2 = 'I am a sick man. I am a spiteful man. I am an unattractive man. \
    I believe my liver is diseased.\
    However, I know nothing at all about my disease, and do not know for certain \
    what ails me.'
    
    textt = b1.read() + b2.read()
    
    #d = build_semantic_descriptors(get_sentence_lists_from_files\
    #                               (['War and Peace.txt', 'Swan\'s Way.txt']))
    d = build_semantic_descriptors(get_sentence_lists(textt))                             
    
    #print(type(get_sentence_lists(textt)))
    #print(get_sentence_lists(text))
    print(run_similarity_test('test.txt', d))
    #print(d['man'])

    #print(get_sentence_lists_from_files(["Samuel L. Jacksons whale.txt",\
    #                                'making ice cream.txt', 'Xbox One.txt']))
    
'''

# Test cases:


# 1. a )

if __name__ == '__main__':
    
    print (get_sentence_lists('.!?.!'))
    print (get_sentence_lists('Hi. Hi! Why are oranges orange?!'))
    print (get_sentence_lists('THE CAT IS FRIENDLY.'))
    print (get_sentence_lists('ThE c"at i.s friendly'))
    print (get_sentence_lists('How"s it going? It.s good.'))
    print (get_sentence_lists(' .So, I hear St. George station is ... flooding.'))
    print (get_sentence_lists('Don.t do that.'))
    print (get_sentence_lists('. . . .'))
    print (get_sentence_lists('. " . "'))
    print (get_sentence_lists('h.e.l,l!o'))
    print (get_sentence_lists('That, was. fantastic!'))

# 1. b )

print (get_sentence_lists_from_files('aaaa.txt'))
print (get_sentence_lists_from_files([aaaa.txt, bbbb.txt, cccc.txt]))

# 1. c )

'''
'Oranges are tasty.'
'Oranges. Oranges. Oranges.'
'Orange. ORANGES! Orange juice. Orange cake!'
'There was once a steak. Steaks are good. Steaks are good.'
'There is a lot of craze. Crazed mania. A lot of mania.'
'Hi. High. Higher.'
'''


# 1. d )

# 1. e )


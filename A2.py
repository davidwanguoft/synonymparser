'''Semantic Similarity: starter code
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 2.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity of sparse vectors vec1 and vec2,
    stored as dictionaries as described in the handout for Project 2.
    '''
    
    dot_product = 0.0  # floating point to handle large numbers
    for x in vec1:
        if x in vec2:
            dot_product += vec1[x] * vec2[x]
    
    return dot_product / (norm(vec1) * norm(vec2))


def get_sentence_lists(text):
    
    sentences = []
    
    for i in range(len(text)):
        word = ''
        w = 0
        
        if text == ' ':
            w += 1
            


def get_sentence_lists_from_files(filenames):
    
    filenames = 
    


def build_semantic_descriptors(sentences):
    
    for i in range(len


def most_similar_word(word, choices, semantic_descriptors):
    pass


def run_similarity_test(filename, semantic_descriptors):
    pass
import functions as fn
import numpy as np
import re
import binascii
import matplotlib.pyplot as plt
import itertools

real_text = 'ADD THE ABILITY TO DECIPHER ANY KIND OF POLYALPHABETIC SUBSTITUTION CIPHERS. THE ONE USED IN THE CIPHER TEXTS HERE HAS TWENTY SIX INDEPENDENT RANDOMLY CHOSEN MONOALPHABETIC SUBSTITUTION PATTERNS FOR EACH LETTER FROM ENGLISH ALPHABET. IT IS CLEAR THAT YOU CAN NO MORE RELY ON THE SAME SIMPLE ROUTINE OF GUESSING THE KEY BY EXHAUSTIVE SEARCH WHICH YOU PROBABLY USED TO DECIPHER THIS PARAGRAPH. WILL THE INDEX OF COINCIDENCE STILL WORK. AS A SUGGESTION YOU CAN TRYTO DIVIDE THE MESSAGE IN PARTS BY THE NUMBER OF CHARACTERS IN A KEY AND APPLY FREQUENCY ANALYSIS TO EACH OF THEM. CAN YOU FIND A WAY TO USE HIGHER ORDER FREQUENCY STATISTICS WITH THIS TYPE OF CIPHER. THE NEXT PARAGRAPH CONTAINS SOME PRETTY INTERESTING INFORMATION ABOUT SOME ADDITIONAL REWARD.'
test4 = 'CKRCHMICNJQUBZTNBJFHHJYYHPEHQMIEQLFPBTBKDYIKTMJUGRUNCZWUCZFCCMIKZIEQGLMEHBZTDYYEZUMRTUDUGTICDFZRFKUNALMIZUFSZYLHOXTCLIETDFIKZZESBBIUBXZRSFMWZLYCHXFQYJDHQMBUBZHLITDUWQTLHJXLGZDMHKDUDAQUBZTNWBHQHZETAJZEOJRKDIEGBXBYFZTNOTYYABEGZQMHOEEYJJDXGACUCJYYDYMTLZTNALMIZZTCFOFQHJSGBXBYZIINRZMQQOUUFZIKZPFSLJYYIKLGQFPNHQMYJMMDAOEEDOCLONTLKJICGUMEJJHQTZLYTOMIZMYUNJINGPSCEREQHKJSTWEYJJWSINILCTDMHBWLYTCRBKUYJJHCPPIOTLEGHBZTNBYQAJDHZIRUBIYDQFLLOOCGJTSPZIWKQLFGHJHQKJQUBJETGLCEHBZTNJFTTFPHZMYGDHGCCTICDFYUWOEYHJHQTFWHSIEOKRIYJJBSDSHLNZZOZUMEJJHYJBYYZCILSZZDQZMGQODMYBIKDRIKSHFTJJDEYBDHBJWNTWEYJLENNKHNAKMTHMMTFZELLKQUCJCUSHFMYTSYHKYNQLWKWKHLYTCYDRYNUFZZCNDLTFINRZFYHTWAQMCUSUFTPREQFMZDZQZSLMZSZWETAPHLFJYRBKUYJJDLFZBLBTPSQNTEBKNCLBSPHPEEBKPSQHRCHPBUFMMJOJBHQBSYZCIEJLFQZMJUZMSUHHFAZBITDZFXHKULHBWLCIYUNJBSZNHUGJYQTFPZDFIKSLILFQEHO'

frequency_alphabet = 'etaoinshrdlcumwfgypbvkjxqz'
plain_alphabet = 'abcdefghijklmnopqrstuvwxyz'
plain_alphabet_cap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

key_length = 4
small_strings = fn.substrings(test4, key_length)
assumed_similar = fn.createKeyDistributedStrings(small_strings, key_length)
frequencies = fn.createFrequencyDict(assumed_similar)

possible_letter_keys = fn.createLetterKeyPatterns(frequencies)

decode_dict = fn.createStartingDictionary(possible_letter_keys)


def runDecodingRoutine(message, starting_dictionary):
    fitness_level = -170
    change_amount = 22
    iteration = 0
    while True:
        decoded_message = fn.maybeDecode(message, starting_dictionary)
        current_fitness = fn.scoreOnBoth(decoded_message)
        if current_fitness + 10 > fitness_level:
            fitness_level += 10
            change_amount = change_amount - 3 if change_amount - 3 > 0 else 1
        if fitness_level > -120:
            print(current_fitness)
            print(decoded_message)
        fn.changeDictionary(starting_dictionary, possible_letter_keys)
        iteration += 1
        if iteration % 500 == 0:
            print('Running iteration {} with {} changes each time'.format(iteration, change_amount))
            print('Current fitness is {}'.format(current_fitness))

# runDecodingRoutine(test4, decode_dict)

# key_dictionary = {l: '0000' for l in list(plain_alphabet_cap)}
# key_dictionary['e'] = 'HJIU'
# key_dictionary['t'] = 'ZZEY'
# key_dictionary['h'] = 'JIWQ'

import numpy as np
import re
import matplotlib.pyplot as plt
import ngram_score as ns
import itertools


frequency_alphabet = 'etaoinshrdlcumwfgypbvkjxqz'
plain_alphabet = 'abcdefghijklmnopqrstuvwxyz'
plain_alphabet_cap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


trigram_fitness = ns.ngram_score(ns.trigrams)
quadgram_fitness = ns.ngram_score(ns.quadgrams)


def scoreOnTrigrams(text, sample_length=24, times=10):
    text_cap = text.upper()
    max_pos = len(text) - sample_length - 1
    acc = 0
    for i in range(times):
        pos = np.random.randint(0, max_pos)
        acc += trigram_fitness.score(text_cap[pos:pos+sample_length])
    return acc / times


def scoreOnQuadgrams(text, sample_length=24, times=10):
    text_cap = text.upper()
    max_pos = len(text) - sample_length - 1
    acc = 0
    for i in range(times):
        pos = np.random.randint(0, max_pos)
        acc += quadgram_fitness.score(text_cap[pos:pos+sample_length])
    return acc / times


def scoreOnBoth(text, sample_length=24, times=10):
    return (scoreOnTrigrams(text, sample_length, times) +
            scoreOnQuadgrams(text, sample_length, times) / 2)


def cleanupNoisyText(noisy_text):
    clean_text = []
    for l in noisy_text:
        if l.isalpha():
            clean_text.append(l)
    clean_string = ''.join(clean_text)
    return clean_string.upper()


def getTuples(l):
    tuples = []
    freq = []
    count = 0
    i = 0
    while i < len(l):
        elt = l[i:i + 3]
        long = len(elt)
        if long == 3:
            for j in range(i + 1, len(l)):
                if l[i:i + long] == l[j:j + long]:
                    while l[i:i + long] == l[j:j + long]:
                        long = long + 1
                    long = long - 1
                    elt = l[i:i + long]
                    tuples.append(''.join(elt))
                    diff = j - i
                    freq.extend(getDivisors(diff))
                    # print("%s\ti:%s\tj:%s\tdiff:%s\t\tDivisors:%s" % (elt, i, j, diff, getDivisors(
                    #       diff)))
                    count = count + 1
                    j = j + long + 1
            i = i + long - 3 + 1
        else:
            i = i + 1
    tuples_set = set(tuples)
    tuples_dict = {key: 0 for key in tuples_set}
    for t in tuples:
        tuples_dict[t] += 1
    return count, freq, tuples_dict


def createKeyDistributedStrings(strings, key_length):
    pairs = {key: '' for key in range(1, key_length + 1)}
    for string in strings:
        for i in range(len(string)):
            pairs[i+1] += string[i]
    return pairs


def createLetterKeyPatterns(key_distributed_letter_frequencies):
    dict_keys = list(key_distributed_letter_frequencies.keys())
    letters_list = []
    for dict_key in dict_keys:
        letter_frequencies = key_distributed_letter_frequencies[dict_key]
        letter_frequencies_list = sorted([[key, value] for key, value in letter_frequencies.items()], key=lambda l: -l[1])
        letters = [l[0] for l in letter_frequencies_list]
        letters_list.append(''.join(letters))
    for i in range(len(letters_list)):
        letter_pattern = letters_list[i]
        if len(letter_pattern) < 26:
            letter_pattern += ''.join(['0' for x in range(26 - len(letter_pattern))])
        letters_list[i] = letter_pattern
    possible_key_letters = {key: [] for key in frequency_alphabet}
    i = 0
    for letter in frequency_alphabet:
        range_start = i - 2 if i - 2 >= 0 else 0
        range_end = i + 3 if i + 3 <= 26 else 26
        key_letters = []
        for j in range(len(dict_keys)):
            letters_range = ''.join(letters_list[j][range_start:range_end])
            # letters_range = letters_range.replace('0', '')
            key_letters.append(letters_range)
        possible_key_letters[letter] = key_letters
        i += 1
    possible_letter_keys = {key: [] for key in frequency_alphabet}
    for letter in frequency_alphabet:
        code1 = possible_key_letters[letter][0]
        code2 = possible_key_letters[letter][1]
        code3 = possible_key_letters[letter][2]
        code4 = possible_key_letters[letter][3]
        possible_letter_keys[letter] = generateKeys(code1, code2, code3, code4)
    del letters_list, possible_key_letters
    return possible_letter_keys


def createStartingKey(length=26, letter=plain_alphabet):
    key = []
    for i in range(length):
        key.append(np.random.choice(letters))
    return ''.join(key)


def createStartingDictionary(all_possible_keys):
    sample_dict = {l: '' for l in list(plain_alphabet)}
    for l in plain_alphabet:
        sample_dict[l] = np.random.choice(all_possible_keys[l])
    return sample_dict


def changeDictionary(dict_to_change, dict_with_data, amount=3, do_not_touch=None):
    if do_not_touch is None:
        availiable_letters = list(plain_alphabet)
    else:
        availiable_letters = [letter for letter in list(plain_alphabet) if letter not in list(do_not_touch)]
    letters_to_change = np.random.choice(availiable_letters, amount)
    for l in letters_to_change:
        dict_to_change[l] = np.random.choice(dict_with_data[l])
    return letters_to_change


def substrings(string, length):
    substr = []
    substrs = []
    i = 0
    for l in string:
        substr.append(l)
        i += 1
        if i == length:
            substrs.append(''.join(substr))
            substr.clear()
            i = 0
    return substrs


def num_entries(string):
    symbols = set(string)
    d = {key: 0 for key in symbols}
    for s in string:
        d[s] = d[s] + 1
    return d


def frequencyAnalisis(string):
    entries = num_entries(string)
    frequencies = {key: (value * 100 / len(string))
                   for key, value in entries.items()}
    return frequencies


def createFrequencyDict(key_distributed_strings):
    frequencies = {key: {} for key in list(key_distributed_strings.keys())}
    for k in list(key_distributed_strings.keys()):
        frequencies[k] = frequencyAnalisis(key_distributed_strings[k])
    return frequencies


def createPlotData(frequency_dict):
    data_size = len(frequency_dict.keys())
    dict_items = [[key, value] for key, value in frequency_dict.items()]
    dict_items_sorted = sorted(dict_items, key=lambda x: -x[1])
    x = list(range(26))
    y = []
    labels = []
    for l in dict_items_sorted:
        labels.append(l[0])
        y.append(l[1])
    if data_size < 26:
        labels[data_size:25] = ['' for i in range(data_size, 26)]
        y[data_size:25] = [0 for i in range(data_size, 26)]
    return x, y, labels


def decypher(cipher, message, key=plain_alphabet):
    decr = dict(zip(cipher, key))
    print(decr)
    decoded = []
    for l in message:
        decoded.append(decr[l])
    return ''.join(decoded)


def shuffle(key):
    a = np.random.randint(0, len(key)-1)
    b = np.random.randint(0, len(key)-1)
    a_v = key[a]
    b_v = key[b]
    am = list(key)
    am[b] = a_v
    am[a] = b_v
    return ''.join(am)


def change(key, position, block):
    key_list = list(key)
    if position not in block:
        key_list[position] = np.random.choice(plain_alphabet)
    return ''.join(key_list)


def maybeDecode(message, keys_dict):
    maybe_decoded_mesage = []
    decoder_dict = {v: k for k, v in keys_dict.items()}
    pos = 0
    found = False
    for l in message:
        for key_string in list(decoder_dict.keys()):
            if not found and l == key_string[pos]:
                maybe_decoded_mesage.append(decoder_dict[key_string])
                found = True
        if not found:
            maybe_decoded_mesage.append(l)
        else:
            found = False
        pos += 1
        if pos == 4:
            pos = 0
    return ''.join(maybe_decoded_mesage)


def keyChecker(message, letter, key_candidates, current_dictionary, regexp):
    work_dictionary = current_dictionary.copy()
    decoded_texts_plain = {}
    for key_candidate in key_candidates:
        work_dictionary[letter] = key_candidate
        decoded_texts_plain[key_candidate] = maybeDecode(message, work_dictionary)
    decoded_texts_sorted = [[''.join(key), len(re.findall(regexp, text))] for key, text in decoded_texts_plain.items()]
    decoded_texts_sorted = sorted(decoded_texts_sorted, key=lambda x: x[1])
    return decoded_texts_sorted


def generateKeys(c0de_1, c0de_2, c0de_3, c0de_4):
    key_candidates = []
    for l1 in c0de_1:
        for l2 in c0de_2:
            for l3 in c0de_3:
                for l4 in c0de_4:
                    key_candidates.append(str(l1 + l2 + l3 + l4))
    return key_candidates

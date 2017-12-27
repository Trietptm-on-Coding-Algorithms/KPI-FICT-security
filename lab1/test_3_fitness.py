import numpy as np
import binascii
import matplotlib.pyplot as plt
import ngram_score as ns

full_test3 = 'EFFPQLEKVTVPCPYFLMVHQLUEWCNVWFYGHYTCETHQEKLPVMSAKSPVPAPVYWMVHQLUSPQLYWLASLFVWPQLMVHQLUPLRPSQLULQESPBLWPCSVRWVFLHLWFLWPUEWFYOTCMQYSLWOYWYETHQEKLPVMSAKSPVPAPVYWHEPPLUWSGYULEMQTLPPLUGUYOLWDTVSQETHQEKLPVPVSMTLEUPQEPCYAMEWWYOYULULTCYWPQLSEOLSVOHTLUYAPVWLYGDALSSVWDPQLNLCKCLRQEASPVILSLEUMQBQVMQCYAHUYKEKTCASLFPYFLMVHQLUPQVSHEUEDUEHQBVTTPQLVWFLRYGMYVWMVFLWMLSPVTTBYUNESESADDLSPVYWCYAMEWPUCPYFVIVFLPQLOLSSEDLVWHEUPSKCPQLWAOKLUYGMQEUEMPLUSVWENLCEWFEHHTCGULXALWMCEWETCSVSPYLEMQYGPQLOMEWCYAGVWFEBECPYASLQVDQLUYUFLUGULXALWMCSPEPVSPVMSBVPQPQVSPCHLYGMVHQLUPQLWLRPHEUEDUEHQMYWPEVWSSYOLHULPPCVWPLULSPVWDVWGYUOEPVYWEKYAPSYOLEFFVPVYWETULBEUF'
test3 = 'ADDTHEABILITYTODECIPHERANYKINDOFPOLYALPHABETICSUBSTITUTIONCIPHERSTHEONEUSEDINTHECIPHERTEXTSHEREHASTWENTYSIXNIDEPENDENTRANDOMLYCHOSENMONOALPHABETICSUBSTITUTIONPATTERNSFOREACHLETTERFROMENGLISHALPHABETITISCLEARTHATYOUCANNOMORERELYONTHESAMESIMPLEROUTINEOFGUESSINGTHEKEYBYEXHAUSTIVESEARCHWHICHYOUPROBABLYUSEDTODECIPHERTHISPARAGRAPHWILLTHEINDEXOFCOINCIDENCESTILLWORKASASUGGESTIONYOUCANTRYTODIVIDETHEMESSAGEINPARTSBYTHENUMBEROFCHARACTERSINAKEYANDAPPLYFREQUENCYANALYSISTOEACHOFTHEMCANYOUFINDAWAYTOUSEHIGHERORDERFREQUENCYSTATISTICSWITHTHISTYPEOFCIPHERTHENEXTPARAGRAPHCONTAINSSOMEPRETTYINTERESTINGINFORMATIONABOUTSOMEADDITIONALREWARD'

plain_alphabet = 'ETAOINSHRDLCUMWFGYPBVKXQ'
cipher_alphabet = 'LPVEWYSQUMCHFTAOGKDBRNIX'

trigram_fitness = ns.ngram_score(ns.trigrams)
quadgram_fitness = ns.ngram_score(ns.quadgrams)


def createDictionary(plain, cipher):
    dictionary = {}
    for i in range(len(cipher)):
        dictionary[cipher[i]] = plain[i]
    return dictionary


def decodeMessage(message, dictionary):
    decoded_message = []
    for l in message:
        decoded_message.extend(dictionary[l])
    return ''.join(decoded_message)


def getInts(length):
    i1 = 0
    i2 = 0
    while i1 == i2:
        i1 = np.random.randint(0, length)
        i2 = np.random.randint(0, length)
    return i1, i2


def swapItems(list):
    i1, i2 = getInts(len(list))
    item1, item2 = list[i1], list[i2]
    list[i1], list[i2] = item2, item1
    return list


def hillclimbDecoding(cipher):
    cipher_alphabet_current = list(cipher_alphabet)
    cipher_alphabet_prev = None
    fitness_current = -99999
    fitness_prev = 0
    fitness_delta = 1000
    # while fitness_current < -200:
    for i in range(10):
        cipher_alphabet_prev = cipher_alphabet_current
        fitness_prev = fitness_current
        cipher_alphabet_current = swapItems(cipher_alphabet_current)
        decoded_cypher = decodeMessage(cipher, createDictionary(plain_alphabet, cipher_alphabet_current))
        print(decoded_cypher)
        fitness_current = trigram_fitness.score(test3)
        if fitness_current < fitness_prev:
            fitness_current = fitness_prev
            cipher_alphabet_current = cipher_alphabet_prev
        else:
            fitness_delta = fitness_current - fitness_prev
        print('Fitness delta: {}; Current fitness: {}; Current alphabet: {}'
              .format(fitness_delta,
                      fitness_current,
                      ''.join(cipher_alphabet_current)))

fitness_current = quadgram_fitness.score(test3)
print(fitness_current)

hillclimbDecoding(test3)

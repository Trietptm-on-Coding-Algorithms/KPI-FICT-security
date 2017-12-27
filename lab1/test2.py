import numpy as np
import binascii
import matplotlib.pyplot as plt

test2 = '1b420538554c2d100f2354096c44036c511838510f27101f235d096c430521400029101f39521f385918394405235e4c2f591c24551e6210382310fe2954192f554c3858096c530321400029480538494c23564c3858053f100322554c3b554c3b59002010193f554c235e003510193c40093e530d3f554c20551838551e3f1c4c3f5f4c3858096c5b0935431c2d53096c591f6c5f0220494c7e064d6c64036c570938101824591f6c510229101e25570438100d39440321511825530d205c156c490339101b255c006c401e23520d2e5c156c5e0929544c385f4c3943096c430321554c3f5f1e3810032a100b295e0938590f6c51002b511e254404211c4c3f5901395c0d3855086c510222550d2059022b10033e100b3e510825550238100829430f295e1862103f29420523451f2049406c471e2544096c59186c42052b58186c5e033b1c4c355f196c4705205c4c2255092810053810182310082953053c58093e101824554c22551438100322554c2d434c3b5500201e4c0e550d3e1005221001255e0860101824551e29171f6c5e036c431c2d53093f1e'


def getDivisors(n):
    l = []
    for i in range(2, n):
        if n % i == 0:
            l.append(i)
    return l


# l argument should be a list containing all bytes of the file (read with toList)
def getTuples(l):
    tuples = []
    freq = []
    count = 0
    i = 0
    while i < len(l):  # Loop through all the list
        elt = l[i:i + 3]  # Take at least 3-character length for tuples
        long = len(elt)
        if long == 3:  # should be 3 if not means we are at the end of the list
            for j in range(i + 1, len(l)):  # Find further in the list for the same pattern
                if l[i:i + long] == l[j:j + long]:  # If match the 3-char check for more
                    while l[i:i + long] == l[j:j + long]:
                        long = long + 1
                    long = long - 1
                    elt = l[i:i + long]  # Now we have a tuple
                    tuples.append(''.join(elt))
                    diff = j - i  # Compute the distance
                    # Add the divisors to the list
                    freq.extend(getDivisors(diff))
                    # print("%s\ti:%s\tj:%s\tdiff:%s\t\tDivisors:%s" % (elt, i, j, diff, getDivisors(
                    #     diff)))  # Print information about the tuple (can be deleted)
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


def countOcc(l):  # return list with (decimal_char, occ)
    d = {}
    for elt in l:
        if elt in d:
            d[elt] += 1
        else:
            d[elt] = 1
    return sorted(d.items(), key=lambda x: x[1], reverse=True)


def explode(key, li):
    dic = {num: [] for num in range(1, key + 1)}
    i = 0
    for index in range(len(li)):
        if i == key:
            i = 0
        dic[i + 1].append(li[index])
        i = i + 1
    return dic


def recreate(dic):
    i = 0
    output = []
    try:
        while 1:
            for l in dic.values():
                output.append(l[i])
            i = i + 1
    except:
        pass
    return output


# def decodeString(str):
#     strings = {key: ''.join(chr(num ^ key) for num in str) for key in range(256)}
#     expected_string = max(list(strings.items()), key=lambda s: s.count(' '))
#     print(expected_string)
#     # key = list(strings.keys())[list(strings.values()).index(expected_string)]
#     # print(key)
#     return expected_string


def decodeString(str):
    strings = (''.join(chr(num ^ key) for num in str) for key in range(256))
    expected_string = max(strings, key=lambda s: s.count(' '))
    print(expected_string)
    return expected_string


def decodeStrings(dic):
    keys = list(dic.keys())
    newDic = {key: [] for key in keys}
    for key, value in dic.items():
        newDic[key] = decodeString(value)
    return newDic


print(len(test2))
encoded = binascii.unhexlify(test2)
print(len(encoded))

symbols = list(encoded)
# _, _, divisors = getTuples(symbols)
# print(countOcc(divisors))

exploded = explode(6, symbols)
decoded = decodeStrings(exploded)
final = recreate(decoded)

print(''.join(final))

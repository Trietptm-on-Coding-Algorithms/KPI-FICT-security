key_dictionary['e'] = 'HJIU'
key_dictionary['t'] = 'ZZEY'
key_dictionary['h'] = 'JIWQ'
key_dictionary['a'] = '0L00'

h_code_1, h_code_2, h_code_3, h_code_4 = 'JTCFG', 'LFTIO', 'DHZWB', 'TQEKH'
h_key_candidates = []
for l1 in h_code_1:
    for l2 in h_code_2:
        for l3 in h_code_3:
            for l4 in h_code_4:
                h_key_candidates.append(str(l1 + l2 + l3 + l4))
print(keyChecker(test4, 'h', h_key_candidates, key_dictionary, 'the'))

o_key_candidates = generateKeys('BDQT', 'MKBLF', 'MYFDH', 'LNCT')
print(keyChecker(test4, 'o', o_key_candidates, key_dictionary, 'to'))

a_key_candidates = generateKeys('BDQ', 'MKBL', 'MYFD', 'LNCT')
print(keyChecker(test4, 'a', a_key_candidates, key_dictionary, 'that')) 

print(fn.maybeDecode(test4, key_dictionary))

fig, axes = plt.subplots(key_length + 1, figsize=(6, 9))
width = 0.3
ind = np.arange(26)

y5 = [12.702, 9.056, 8.167, 7.507, 6.966, 6.749, 6.327, 6.094, 5.987, 4.253, 4.025, 2.782, 2.758, 2.406, 2.360, 2.228, 2.015, 1.974, 1.929, 1.492, 0.978, 0.772, 0.153, 0.150, 0.095, 0.074]
x5 = list(range(len(frequency_alphabet)))
labels5 = list(frequency_alphabet)
bars5 = axes[key_length].bar(x5, y5, width, color='g')
axes[key_length].set_title('Letter frequency in English')
axes[key_length].set_xticks(ind)
axes[key_length].set_xticklabels(labels5)

i = 0
for k in list(frequencies.keys()):
    x, y, labels = fn.createPlotData(frequencies[k])
    bars1 = axes[i].bar(x, y, width, color='r')
    axes[i].set_title('Letter frequency in {} key symbol'.format(i + 1))
    axes[i].set_xticks(ind)
    axes[i].set_xticklabels(labels)
    i += 1

plt.tight_layout(h_pad=0.25)
plt.show()

while True:
    new_key = fn.shuffle(key)
    keys += 1
    decyphered_text = fn.decypher(new_key, test3.lower())
    p = fn.scoreOnTrigrams(decyphered_text)
    if p > points:
        if p > max_points:
            max_points = p
            print("KEYS", keys)
            print("TEMPERATURE", t)
            print("POINTS", p)
            print("KEY", new_key)
            print(decyphered_text)
        key = new_key
        points = p
    else:
        if np.random.random() < t:
            points = p
            key = new_key
    t *= freezing


def decode(message):
    key = ''.join(list(set(test3))).lower()
    maybe_guessed = []

    keys = 0
    position = 0
    max_position = len(key)

    points = -200
    max_points = points

    t = 1.0
    freezing = 0.9999

    while True:
        new_key = fn.change(key, position, maybe_guessed)
        keys += 1
        decyphered_text = fn.decypher(new_key, test3.lower())
        p = fn.scoreOnBoth(decyphered_text)
        if p > points:
            if p > max_points:
                max_points = p
                print("KEYS", keys)
                print("TEMPERATURE", t)
                print("POINTS", p)
                print("KEY", new_key)
                print(decyphered_text)
            key = new_key
            points = p
        else:
            if np.random.random() < t:
                points = p
                key = new_key
        t *= freezing

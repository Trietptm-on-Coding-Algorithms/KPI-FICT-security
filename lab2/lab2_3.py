from Server import Server
from MT19937 import MT19937
from time import time


server = Server('http://ec2-35-159-11-170.eu-central-1.compute.amazonaws.com')
acc_id = 'yehorb_better_mt_' + str(time())
account = server.get('casino/createacc', {'id': acc_id})
print(account)


def unBitshiftRightXor(value, shift):
    i = 0
    result = 0
    while i * shift < 32:
        partMask = (-1 << (32 - shift)) >> (shift * i)
        part = value & partMask
        value ^= (part >> shift)
        if i == 0:
            result = part
        else:
            result |= part & ~((-1 << (32 - shift)) >> (shift * (i - 1)))
        i += 1
    return result


def unBitshiftLeftXor(value, shift, mask):
    i = 1
    result = 0
    while (i * shift < 32 + shift):
        partMask = 2 ** (shift * i) - 1 - (2 ** (shift * (i - 1)) - 1)
        part = value & partMask
        value ^= (part << shift) & mask
        result |= (part & partMask)
        i += 1
    return result


def undo_transformation(output):
    value = output
    value = unBitshiftRightXor(value, 18)
    value = unBitshiftLeftXor(value, 15, 0xefc60000)
    value = unBitshiftLeftXor(value, 7, 0x9d2c5680)
    value = unBitshiftRightXor(value, 11)
    return value


def play():
    seed = int(time())
    print(seed)

    print("collecting numbers...")
    numbers = []
    for i in range(623):
        if i % 25 == 0:
            print(i, '...')
        res = server.get('casino/playBetterMt', {'id': acc_id, 'bet': 1, 'number': 1})
        real_number = res['realNumber']
        numbers.append(real_number)
    res = server.get('casino/playBetterMt', {'id': acc_id, 'bet': 1, 'number': 1})
    real_number = res['realNumber']
    numbers.append(real_number)

    print("collected numbers, transforming...")
    transformed_numbers = list(map(lambda x: undo_transformation(x), numbers))

    print("transformed numbers, playing...")
    mt = MT19937(transformed_numbers, True)

    if 'account' in res:
        money = res['account']['money']

    while money < 1000000:
        next_number = mt.extract_number()
        print(next_number)
        res = server.get('casino/playBetterMt', {'id': acc_id, 'bet': int(money / 10), 'number': next_number})
        print(res)
        if 'account' in res:
            money = res['account']['money']

    final_res = server.get('casino/playBetterMt', {'id': acc_id, 'bet': 1, 'number': 1})
    print('Final results:', final_res)
    print('PWNED!')


play()

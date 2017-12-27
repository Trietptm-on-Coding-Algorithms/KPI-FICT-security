from Server import Server
from MT19937 import MT19937
from time import time


server = Server('http://ec2-35-159-11-170.eu-central-1.compute.amazonaws.com')
acc_id = 'yehorb_mt_' + str(time())
account = server.get('casino/createacc', {'id': acc_id})
print(account)


def play():
    seed = int(time())

    res = server.get('casino/playMt', {'id': acc_id, 'bet': 1, 'number': 1})
    print(res)
    real_number = res['realNumber']

    i = -2
    while True:
        i += 1
        mt = MT19937(seed + i)
        number = mt.extract_number()
        if number == real_number:
            print('seed is', seed + i)
            break

    if 'account' in res:
        money = res['account']['money']

    while money < 1000000:
        next_number = mt.extract_number()
        print(next_number)
        res = server.get('casino/playMt', {'id': acc_id, 'bet': int(money / 10), 'number': next_number})
        print(res)
        if 'account' in res:
            money = res['account']['money']

    final_res = server.get('casino/playMt', {'id': acc_id, 'bet': 1, 'number': 1})
    print('Final results:', final_res)
    print('PWNED!')


play()

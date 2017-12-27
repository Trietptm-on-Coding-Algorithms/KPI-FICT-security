from Server import Server
from LCG import LCG
from time import time


server = Server('http://ec2-35-159-11-170.eu-central-1.compute.amazonaws.com')
acc_id = 'yehorb_linear_' + str(time())
account = server.get('casino/createacc', {'id': acc_id})
print(account)


def play():
    res = server.get('casino/playLcg', {'id': acc_id, 'bet': 1, 'number': 1})
    print(res)
    real_number = res['realNumber']

    lcg = LCG(real_number)

    if 'account' in res:
        money = res['account']['money']

    while money < 1000000:
        next_number = lcg.extract_number()
        print(next_number)
        res = server.get('casino/playLcg', {'id': acc_id, 'bet': int(money / 10), 'number': next_number})
        print(res)
        if 'account' in res:
            money = res['account']['money']

    final_res = server.get('casino/playLcg', {'id': acc_id, 'bet': 1, 'number': 1})
    print('Final results:', final_res)
    print('PWNED!')


play()

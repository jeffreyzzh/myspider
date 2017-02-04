# -*- coding: utf-8 -*-
# 2017/1/24 0024
# JEFF


def change_price(price):
    if not price:
        return 0
    price = float(price)
    return price // 5 * 5


def price_rank(price):
    if not price:
        return 0
    price = float(price)
    return int(price // 5 + 1)


def make_rank(price):
    if not price:
        return 0
    price = float(price)
    rank = price // 5
    if rank >= 7:
        return '35万以上'
    rank_name = '{}-{}万'.format(rank * 5, rank * 5 + 4.99)
    return rank_name


def get_price_in_rank(rank):
    return int(rank[0:2].replace('.', ''))


if __name__ == '__main__':
    # p = change_price(15)
    # print(p)

    # name = make_rank(4)
    # print(name)

    ranklist = ['15.0-19.99万', '25.0-29.99万', '30.0-34.99万', '35万以上', '5.0-9.99万', '10.0-14.99万', '20.0-24.99万',
                '0.0-4.99万']

    for i in range(len(ranklist)):
        for count, each in enumerate(ranklist):
            try:
                if count >= len(ranklist) - 1:
                    break
                x = ranklist[count]
                y = ranklist[count + 1]
                a = get_price_in_rank(ranklist[count])
                b = get_price_in_rank(ranklist[count + 1])
                if a >= b:
                    ranklist[count] = y
                    ranklist[count + 1] = x
            except IndexError:
                print('index error')

    print(ranklist)

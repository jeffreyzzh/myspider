# -*- coding: utf-8 -*-
# 17/1/18

import asyncio

import time


async def compute(x, y):
    print('Compute {} + {} ...'.format(x, y))
    await asyncio.sleep(5)
    return x + y


async def print_sum(x, y):
    result = await compute(x, y)
    print('{} + {} = {}'.format(x, y, result))


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(print_sum(1, 3))
    # loop.close()
    loop = asyncio.get_event_loop()
    tasks = [print_sum(1, 3), print_sum(2, 6)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

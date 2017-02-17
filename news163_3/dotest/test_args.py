# -*- coding: utf-8 -*-
# 2017/2/17
# author = JEFF


import argparse


def parse_args():
    desc = """\
    啦啦啦\r
    德码西亚
    """

    parser = argparse.ArgumentParser(description=desc)

    help = 'how many threads to crawl, default 8'
    parser.add_argument('-t', dest='threadnums', help=help, default=8, type=int, metavar='nums')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args.threadnums)

#-*- coding: utf-8 -*-
from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()


def main():
    if len(args) != 1:
        print 'Incorrect number of arguments! Try again.'
    else:
        name = args[0]
        print name

if __name__ == '__main__':
    main()
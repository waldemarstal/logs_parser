#-*- coding: utf-8 -*-
import sys
from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()
from parser import run_parser


def main():
    if len(args) != 1:
        print 'Incorrect number of arguments! Try again.'
        sys.exit(0)
    file_name = args[0]
    try:
        run_parser(file_name)
    except Exception as e:
        print '%s!' % e


if __name__ == '__main__':
    main()
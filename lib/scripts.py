#-*- coding: utf-8 -*-
import sys
from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()
from parser import Parser


def main():
    if len(args) != 1:
        print 'Incorrect number of arguments! Try again.'
        sys.exit(0)
    file_name = args[0]
    try:
        logs_parser = Parser(file_name)
        logs_parser.run_parser()
    except Exception as e:
        print '%s!' % e


if __name__ == '__main__':
    main()
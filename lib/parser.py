#-*- coding: utf-8 -*-
from gzip import GzipFile


class ParseError(Exception):
    pass


def run_parser(file_name):
    try:
        if file_name.endswith('.gz'):
            fd = GzipFile(file_name, 'r')
        else:
            fd = open(file_name, 'r')
    except Exception as e:
        raise ParseError(e)
    else:
        print fd
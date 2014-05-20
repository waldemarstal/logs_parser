#-*- coding: utf-8 -*-
import re
from gzip import GzipFile
# from urlparse import urlparse


class ParseError(Exception):
    pass


def url_from_regexp(regexp):
    if regexp:
        return regexp[0][0]
    return ''



def run_parser(file_name):
    url_list = []
    try:
        if file_name.endswith('.gz'):
            fd = GzipFile(file_name, 'r')
        else:
            fd = open(file_name, 'r')
    except Exception as e:
        raise ParseError(e)
    else:
        files = fd.readlines()
        for line in files:
            # parseline = urlparse(line)
            # complete_url = parseline.geturl()
            line = line.replace('(', '')
            GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
            regexp = GRUBER_URLINTEXT_PAT.findall(line)
            url = url_from_regexp(regexp)
            if url:
                url_list.append(url)
        print 'DONE!'
        fd.close()
        return
#-*- coding: utf-8 -*-
import re
from gzip import GzipFile
from urlparse import urlparse


class ParseError(Exception):
    pass


def url_from_regexp(regexp):
    if regexp:
        return regexp[0][0]
    return ''


def is_selected_tld(parse):
    domain = parse.netloc.split('.')[-1]
    if domain == 'pl':
        return True
    return False


def run_parser(file_name):
    probability_tree = {}
    probability_tree['pl'] = {}
    # res = open('result.txt', 'w')
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
            line = line.replace('(', '')
            GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
            regexp = GRUBER_URLINTEXT_PAT.findall(line)
            url = url_from_regexp(regexp)
            if not url:
                continue
            parseurl = urlparse(url)
            url = parseurl.geturl().split('?')[0]
            # res.write(url)
            # res.write('\n')
            if not is_selected_tld(parseurl):
                continue
            before_domain = parseurl.netloc.split('.')[-2]
            if not probability_tree['pl'].get(before_domain):
                probability_tree['pl'][before_domain] = []
            probability_tree['pl'][before_domain].append(url)
        import ipdb;ipdb.set_trace()
        # res.close()
        print 'DONE!'
        fd.close()
        return
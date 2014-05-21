#-*- coding: utf-8 -*-
import re
from gzip import GzipFile
from urlparse import urlparse


class ParseError(Exception):
    pass


class Parser():

    def __init__(self, file_name):
        self.file_name = file_name
        self.probability_tree = {'pl': {}}
        self.fd = ''
        self.url_in_text = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

    @staticmethod
    def pop_qs(url):
        parse = urlparse(url)
        parse = parse.geturl().split('?')[0]
        return parse

    @staticmethod
    def is_selected_tld(parse):
        parse = urlparse(parse)
        domain = parse.netloc.split('.')[-1]
        if domain == 'pl':
            return True
        return False

    def _regexp(self, line):
        regexp = self.url_in_text.findall(line)
        return regexp

    def get_url(self, line):
        regexp = self._regexp(line)
        if regexp:
            return regexp[0][0]
        return ''

    def _open_file(self):
        try:
            if self.file_name.endswith('.gz'):
                self.fd = GzipFile(self.file_name, 'r')
            else:
                self.fd = open(self.file_name, 'r')
        except Exception as e:
            raise ParseError(e)

    def _close_file(self):
        print 'Close file!'
        self.fd.close()

    def run_parser(self):
        self._open_file()
        files = self.fd.readlines()
        for line in files:
            line = line.replace('(', '')
            url = self.get_url(line)
            if not url:
                continue
            parse_url = self.pop_qs(url)
            if not self.is_selected_tld(parse_url):
                continue
            self._create_probability_tree(parse_url)
        self._close_file()
        return

    def _create_probability_tree(self, parse_url):
        parse_url = urlparse(parse_url)
        before_domain = parse_url.netloc.split('.')[-2]
        if not self.probability_tree['pl'].get(before_domain):
            self.probability_tree['pl'][before_domain] = []
        self.probability_tree['pl'][before_domain].append(parse_url)
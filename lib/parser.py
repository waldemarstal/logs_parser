#-*- coding: utf-8 -*-
import re
from gzip import GzipFile
from urlparse import urlparse


class ParseError(Exception):
    pass


class Parser():

    def __init__(self, file_name):
        self.file_name = file_name
        self.probability_tree = {'pl': {'url_list': []}}
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
        self.calculate_probability()
        return

    def _create_probability_tree(self, parse_url):
        parse_url = urlparse(parse_url)
        before_domain = parse_url.netloc.split('.')[-2]
        if not self.probability_tree['pl'].get(before_domain):
            self.probability_tree['pl'][before_domain] = {}
        self.probability_tree['pl']['url_list'].append(parse_url.geturl())
        value = self.probability_tree['pl'][before_domain]
        path_list = self.create_path_list(parse_url.path)
        for elem in path_list:
            if elem not in value:
                value[elem] = {}
                value = value[elem]
            else:
                value = value[elem]
        if not self.probability_tree['pl'][before_domain].get('path_list'):
            self.probability_tree['pl'][before_domain]['path_list'] = []
        self.probability_tree['pl'][before_domain]['path_list'].append(
            parse_url.path
        )

    @staticmethod
    def create_path_list(parse_url):
        if parse_url == '/':
            return []
        if parse_url[0] == '/':
            parse_url = parse_url[1:]
        if parse_url[-1] == '/':
            parse_url = parse_url[:-1]
        return parse_url.split('/')

    def calculate_probability(self):
        divisor = len(self.probability_tree['pl'])
        for k, v in self.probability_tree['pl'].iteritems():
            if type(v) is not dict:
                continue
            for path in v['path_list']:
                if path == '/':
                    continue
                path_list = self.create_path_list(path)
                for i in range(1, len(path_list) + 1):
                    count = self.find_count_of_member(path_list[:i], k)
                    print '/%s - %s %f' % (
                        '/'.join(path_list[:(i - 1)]),
                        path_list[i - 1],
                        round(count / float(divisor), 3)
                    )

    def find_count_of_member(self, param, bdom):
        count = 0
        for k, v in self.probability_tree['pl'].iteritems():
            last = '###@'
            if k == bdom:
                continue
            value = self.probability_tree['pl'][k]
            for elem in param:
                if elem not in value:
                    break
                else:
                    last = elem
                    value = value[elem]
            if last == param[-1]:
                count += 1
        return count
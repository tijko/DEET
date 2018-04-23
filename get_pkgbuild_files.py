#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import requests
import sys


def scrap_urls(pkg):
    base = 'https://git.archlinux.org/svntogit/packages.git/tree/{}/trunk'
    req = requests.get(base.format(pkg))
    if not req.ok:
        print('Error requesting :: <{}'.format(pkg))
    soup = BeautifulSoup(req.text, "html.parser")
    a_tags = soup.findAll('a')
    hrefs = {a_tags[i]['href'] for i in range(len(a_tags))}
    hrefs = {ref for ref in hrefs if '/tree/{}/trunk/'.format(pkg) in ref}
    base = 'https://git.archlinux.org{}'
    for url in hrefs:
        req = requests.get(base.format(url.replace('tree', 'plain')))
        filename = url.split('/')[-1]
        with open(filename, 'w+') as fh:
            fh.write(req.text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Pass a package-name')
        sys.exit(0)
    pkg = sys.argv[1]
    pkg_urls = scrap_urls(pkg)

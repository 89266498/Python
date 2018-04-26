# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib

import os
import requests
import time
from lxml import etree



def spider():
    curr=os.getcwd()
    target_dir=os.path.join(curr,'data')
    target_dir="D:\Download\data"
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    for i in range(600, 800, 10):
        url = 'http://www.lrts.me/ajax/playlist/2/598/%d' % i
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        s = requests.get(url=url, headers=headers)
        tree = etree.HTML(s.text)
        print(tree)
        nodes = tree.xpath('//*[starts-with(@class,"clearfix section-item section")]')
        print(len(nodes))
        for node in nodes:
            filename = node.xpath('.//div[@class="column1 nowrap"]/span/text()')[0]
            link = node.xpath('.//input[@name="source" and @type="hidden"]/@value')[0]

            print('link:'+link)
            post_fix=link.split('.')[-1]
            print(post_fix)
            full_path= filename+'.'+post_fix
            print('full_path:'+full_path)
            urllib.request.urlretrieve(link, filename=os.path.join(target_dir,full_path))
            time.sleep(1)


if __name__ == '__main__':
    spider()
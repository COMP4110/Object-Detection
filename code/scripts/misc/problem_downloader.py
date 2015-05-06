__author__ = 'mitchell'

import urllib.request
import codecs
import os

from bs4 import BeautifulSoup as Soup


def make_dirs_for_image(img):
    dirs = img.attrs['src'].split("/")
    dirs.pop()
    path = ""
    for d in dirs:
        path += d + "/"
    os.makedirs(path, exist_ok=True)


def save_problem_page(problem_number):
    f = urllib.request.urlopen("http://projecteuler.net/problem={}".format(problem_number))
    soup = Soup(f)

    with codecs.open("problem_pages/problem{}.html".format(problem_number), 'w', 'utf-8') as text_file:
        text_file.write(str(soup))

    # Download images:
    images = soup.select("img")
    for img in images:
        make_dirs_for_image(img)

        url = 'http://projecteuler.net/' + img.attrs['src']
        urllib.request.urlretrieve(url, img.attrs['src'])


for n in range(1, 438):
    print(n)
    save_problem_page(n)



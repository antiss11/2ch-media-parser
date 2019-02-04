# -*- coding: utf-8 -*-
""" Functions for parsing, processing and downloading media content from 2ch.hk """

import requests
from bs4 import BeautifulSoup
import re
import os

VIDEO_PATTERN = "mp4$|webm$"            # Regular expression patterns for
PICS_PATTERN = "png$|jpg$|gif$"         # video and image formats


def get_page(url):
    """ Function gets page by thread url and returns Error if status code is bad """
    page = requests.get(url)
    if page.status_code < 400:
        return page
    else:
        pass


def get_links(page, content_type):
    """ Parse page by content type"""
    soup = BeautifulSoup(page.text, features="lxml")
    if content_type == "pics":
        image_blocks = soup.findAll("a", {"class": "post__image-link", "href": re.compile(PICS_PATTERN)})
    elif content_type == "videos":
        image_blocks = soup.findAll("a", {"class": "post__image-link", "href": re.compile(VIDEO_PATTERN)})
    elif content_type == "all":
        image_blocks = soup.findAll("a", {"class": "post__image-link"})
    cutted_links = (i.get("href") for i in image_blocks)                                                    # get short url
    full_links = ['https://2ch.hk' + i for i in cutted_links]                                               # restore full url
    return full_links


def get_names(links):
    """Function cuts off file names and returns it"""
    names_list = (i.split("/")[-1] for i in links)
    return names_list


def download_image(link, folder, name):
    """Funtions downloads images in binary mode"""
    os.chdir(folder)
    with open(name, 'wb') as handle:
        responce = requests.get(link, stream=True)
        for block in responce.iter_content():
            handle.write(block)


def parse_page(page, folder_to_save, content_type):
    """ Main function, requiers page url (2ch thread) and content type -
    'pics', 'videos' and 'all' """
    page = get_page(page)
    links = get_links(page, content_type)
    names = get_names(links)
    for link in links:
        download_image(link, folder_to_save, next(names))

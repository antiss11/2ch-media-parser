# -*- coding: utf-8 -*-
""" Functions for parsing, processing and downloading media content from 2ch.hk """

import requests
from bs4 import BeautifulSoup
import re
import os
import threading

VIDEO_PATTERN = "mp4$|webm$"            # Regular expression patterns for
PICS_PATTERN = "png$|jpg$|gif$"         # video and image formats


class PageParser:

    def __init__(self, url, folder_to_save):
        self.url = url
        self.folder_to_save = folder_to_save

    def get_page(self):
        """ Function gets page by thread url and returns Error if status code is bad """
        page = requests.get(self.url)
        if page.status_code < 400:
            page = page.text
            return page
        else:
            raise Exception("Page error!")

    def get_links(self, page, content_type):
        """ Parse page by content type"""
        soup = BeautifulSoup(page, features="lxml")
        if content_type == "pics":
            image_blocks = soup.findAll("a", {"class": "post__image-link", "href": re.compile(PICS_PATTERN)})
        elif content_type == "videos":
            image_blocks = soup.findAll("a", {"class": "post__image-link", "href": re.compile(VIDEO_PATTERN)})
        elif content_type == "all":
            image_blocks = soup.findAll("a", {"class": "post__image-link"})
        cutted_links = (i.get("href") for i in image_blocks)                                                    # get short url
        full_links = ['https://2ch.hk' + i for i in cutted_links]                                               # restore full url
        return full_links

    def get_links_count(self, links):
        num_images = len(links)
        return num_images

    def get_names(self, links):
        """Function cuts off file names and returns it"""
        names_list = (i.split("/")[-1] for i in links)
        return names_list


class MainActions:

    @staticmethod
    def parse_page(url, folder, content_type, label):
        parser = PageParser(url, folder)
        page = parser.get_page()
        links = parser.get_links(page, content_type)
        num_links = parser.get_links_count(links)
        names = parser.get_names(links)
        handler = StatusHandler(label)
        links_dict = list(zip(links, names))
        set_folder(folder)
        images_ready = 0
        for link, name in links_dict:
            handler.message("{0}/{1}".format(images_ready, num_links))
            download_image(link, name)
            images_ready += 1


    @classmethod
    def parse_page_thread(cls, url, folder, content_type, label):
        thread = threading.Thread(target=MainActions.parse_page, args=(url, folder, content_type, label))
        thread.start()


class StatusHandler:
    def __init__(self, label):
        self.label = label

    def message(self, message):
        self.label['text'] = message


def download_image(link, name):
    """Funtions downloads images in binary mode"""
    with open(name, 'wb') as handle:
        responce = requests.get(link, stream=True)
        for block in responce.iter_content():
            handle.write(block)


def set_folder(path):
    os.chdir(path)



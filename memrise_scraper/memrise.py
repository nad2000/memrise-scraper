#!/usr/bin/env python

COURSE_URL = "/course/977288/korean-grammar-in-use-11/"
CARD_COLUMNS = ("col_a", "col_b")

import codecs, sys
import re
import requests
from bs4 import BeautifulSoup


def lazy_property(fn):
    """Decorator that makes a property lazy-evaluated.
    """
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


def get_soup(url):
    # TODO: it works actually w/o cookies:
    res = requests.get(
        url if url.strip().startswith("http") else "http://www.memrise.com" + url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup

class Course(object):

    def __init__(self, course_url):
        match = re.match(r'^(.*)/(\d+)/?$', course_url)
        if match:
            course_url, level = match.groups()
        else:
            level = None

        self.course_url = course_url
        # a sligle level if it was included in the URL
        self.level = level

    @lazy_property
    def soup(self):
        return get_soup(self.course_url)

    @property
    def name(self):
        el = self.soup.find("h1", class_="course-name")
        return el.text if el else self.course_url.split('/')[-1]

    @property
    def levels(self):

        #levels = soup.find(lambda tag: tag.name == "div" and "levels" in tag.attrs.get("class"))
        levels = self.soup.find_all("a", class_="level")

        for l in levels:
            url = l.attrs.get("href")
            if self.level and not url.endswith(self.level + '/'):
                continue  ## skip lelevel not requested

            title = l.find("div", class_="level-title").text.strip()
            yield (url, title)


    def cards(self, *, level_url : str):
        """
        :level_url:   level URL
        """
        def get_text(value):
            return '' if value is None else value.text

        soup = get_soup(level_url)

        for thing in soup.find_all(lambda tag: tag.has_attr("data-thing-id")):

            try:
                cols = (get_text(thing.find("div", class_=col_name).find("div", class_="text"))
                    for col_name in CARD_COLUMNS)
            except:
                continue

            yield cols


def dump_course(*, course_url : str):
    """
    :course_url:   course URL
    """
    course = Course(course_url=course_url)

    for level_url, title in course.levels:
        print("*** %s (%s)" % (title, level_url))
        for card in course.cards(level_url=level_url):
            print('\t'.join(card))


def main():
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    course_url = COURSE_URL if len(sys.argv) < 2 else sys.argv[1]
    dump_course(course_url=course_url)


if __name__ == "__main__":
    main()

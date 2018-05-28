#!/usr/bin/env python

import os, re, codecs, sys
from .memrise import Course, COURSE_URL
from gtts import gTTS
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from shutil import copyfileobj


def try_krdict(word : str, output_filename: str):
    # import pdb; pdb.set_trace()

    with requests.get("https://krdict.korean.go.kr/dicSearch/search?mainSearchWord=" + quote(word)) as res:
        if res.status_code != 200:
            return
        soup = BeautifulSoup(res.text, "html.parser")
    el = soup.find("img", dict(alt="", title=""))
    if not el:
        return
    match = re.search("http.*mp3", el.attrs["onclick"])
    if not match:
        return
    with requests.get(match[0], stream=True) as res:
        if res.status_code != 200:
            return
        try:
            output_filename = "(krdict)".join(os.path.splitext(output_filename))
            with open(output_filename, "wb") as o:
                copyfileobj(res.raw, o)
            return output_filename
        except:
            return


def dump_tts(*, course_url : str, no_audio : bool, lang : str = "ko"):
    """
    :course_url:   course URL
    :no_audio:     skip donwloading the audio
    :lang:         override the lanuage
    """

    course = Course(course_url=course_url)
    course_dir_name = course.name #.replace(' ', "\\ ")
    os.makedirs(course_dir_name, exist_ok=True)
    print(f"* {course.name}\n\n")

    for level_url, title in course.levels:
        print("*** %s (%s)" % (title, level_url), flush=True)
        if sys.platform.startswith("win"):
            # replace illegal symbols in the windows file name
            title = title.replace(':', '-')

        output_dir = os.path.join(course_dir_name, title)
        if not no_audio:
            os.makedirs(output_dir, exist_ok=True)

        with codecs.open(os.path.join(course.name, title) + ".csv", "w", encoding="utf-8") as level_file:
            for card in course.cards(level_url=level_url):
                card = list(card)
                word = card[0]
                level_file.write('\t'.join(card))
                level_file.write('\n')
                file_name = os.path.join(output_dir, word.replace('/', "|")) + ".mp3"
                if (not no_audio and not (os.path.exists(file_name) or
                        os.path.lexists("(krdict)".join(os.path.splitext(file_name))))):
                    if lang != "ko" or not try_krdict(word, file_name):
                        tts = gTTS(word, lang=lang)
                        tts.save(file_name)


def main():
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    no_audio = ("--no-audio" in sys.argv)
    if no_audio:
        sys.argv.pop(sys.argv.index("--no-audio"))
    course_url = COURSE_URL if len(sys.argv) < 2 else sys.argv[1]
    dump_tts(course_url=course_url, no_audio=no_audio)


if __name__ == "__main__":
    main()

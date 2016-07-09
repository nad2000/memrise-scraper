import os
import sys
from memrise import Course, COURSE_URL
from gtts import gTTS

def dump_tts(*, course_url : str):
    """
    :course_url:   course URL
    """

    course = Course(course_url=course_url)
    os.makedirs(course.name, exist_ok=True)

    for level_url, title in course.levels:
        print("*** %s (%s)" % (title, level_url), flush=True)
        output_dir = os.path.join(course.name, title)
        os.makedirs(output_dir, exist_ok=True)

        for word, *_ in course.cards(level_url=level_url):
            file_name = os.path.join(output_dir, word) + ".mp3"
            tts = gTTS(word, lang="ko")
            tts.save(file_name)


if __name__ == "__main__":
    course_url = COURSE_URL if len(sys.argv) < 2 else sys.argv[1]
    dump_tts(course_url=course_url)

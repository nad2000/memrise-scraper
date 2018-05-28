"""Memrise flashcar scraping."""
__version__ = "0.3.0"

# flake8: noqa
import click
from .memrise import *
from .memrise2tts import *

@click.command()
@click.option("--tts", is_flag=True, help="Get Google TTS generated sound files.")
@click.option("--lang", default="ko", help="Source language (need to be given for TTS).")
@click.option("--no-audio", is_flag=True, help="Skip donwloading audio.")
@click.argument("url", default=COURSE_URL)
def scrape(url, tts, lang, no_audio):
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    if tts:
        dump_tts(course_url=url, no_audio=no_audio)
        pass
    else:
        dump_course(course_url=url)

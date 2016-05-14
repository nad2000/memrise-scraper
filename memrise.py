COURSE_URL = "/course/977288/korean-grammar-in-use-11/"
CARD_COLUMNS = ("col_a", "col_b")
    
import codecs, sys
import requests
from bs4 import BeautifulSoup

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def get_soup(url):
    # TODO: it works actually w/o cookies:
    res = requests.get(
        url if url.strip().startswith("http") else "http://www.memrise.com" + url)
    soup = BeautifulSoup(res.text, "html.parser", from_encoding="utf-8")
    return soup

    
def levels(*, course_url : str):
    """
    :course_url:   course URL
    """
    soup = get_soup(course_url)
    #levels = soup.find(lambda tag: tag.name == "div" and "levels" in tag.attrs.get("class"))
    levels = soup.find_all("a", class_="level")
    
    for l in levels:
        yield l.attrs.get("href")


def cards(*, level_url : str):
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
    for level_url in levels(course_url=course_url):
        print("***", level_url)
        for card in cards(level_url=level_url):
            print('\t'.join(card))
        
if __name__ == "__main__":
    course_url = COURSE_URL if len(sys.argv) < 2 else sys.argv[1]
    dump_course(course_url=course_url)
    
    
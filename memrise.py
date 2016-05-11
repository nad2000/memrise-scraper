DEFAULT_COURSE = "/course/977288/korean-grammar-in-use-11/"
    
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

    
def dump_course(url):
    soup = get_soup(url)
    #levels = soup.find(lambda tag: tag.name == "div" and "levels" in tag.attrs.get("class"))
    levels = soup.find_all("a", class_="level")
    
    for l in levels:
        url = l.attrs.get("href")
        dump_level(url)


def dump_level(url):
    soup = get_soup(url)
    
    for l in soup.find_all(lambda tag: tag.has_attr("data-thing-id")):
        
        try:
            cols = [l.find("div", class_=col_name).find("div", class_="text").text
                for col_name in ["col_a", "col_b"]
            ]
            print('\t'.join(cols))
        except:
            pass
    

if __name__ == "__main__":
    url = DEFAULT_COURSE if len(sys.argv) < 2 else sys.argv[1]
    dump_course(url)
    
    
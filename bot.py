from sys import argv as argv
import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import time




pyautogui.FAILSAFE = True

if len(argv) == 2:
    set_code = argv[1]
else:
    set_code = "203143222"

# read through terms and get info
def parse_for_data():
    term_child_lines = [x.children for x in vocab_html.find_all("div", class_="SetPageTerm-wordText")]
    terms = []
    for children in term_child_lines:
        for child in children:
            terms.append(child.string)
    definition_child_lines = [x.children for x in vocab_html.find_all("div", class_="SetPageTerm-definitionText")]
    definitions = []
    for children in definition_child_lines:
        for child in children:
            definitions.append(child.string)

    term_def = []

    for index in range(len(terms)):
        term_def.append((terms[index], definitions[index]))
    return term_def

vocab_html = soup(requests.get("https://quizlet.com/" + set_code).content, "lxml")

term_def_list = parse_for_data()

#### at this point ALL term def info is connected as tuples in term_def_list




#initialize selenium chrome web
chrome_options = Options()
chrome_options.add_argument("--window-size=980,1080")
browser = webdriver.Chrome(chrome_options=chrome_options)

def log_in():
    pass

def parse_match_space(source):
    tile_html = soup(source, "lxml")
    tiles =[x.string for x in tile_html.find_all("div", style="display: block;")]
    return tiles

def find_related_tile(original):
    for pair in term_def_list:
        if pair[0] == original:
            return pair[1]
        elif pair[1] == original:
            return pair[0]


def match_tiles():
    browser.get("https://quizlet.com/" + set_code + "/match")
    browser.find_element_by_css_selector('.UIButton.UIButton--hero').click()
    time.sleep(2)
    tiles = parse_match_space(browser.page_source)

    for pair_index in range(6):
        first_tile = tiles[0]
        print("\n\nfirst_tile", first_tile, "\n\n")
        #browser.find_element_by_xpath("//*[contains(text(), \"" + first_tile + "\")]").click()
        #browser.find_element_by_xpath("//*[codepoint-equal(string-to-codepoints(text()), strin g-to-codepoints(\"{}\"))]".format(first_tile)).click()
        browser.find_element_by_xpath("//*[contains(text(), \"" + first_tile + "\")]").click()

        second_tile = find_related_tile(first_tile)
        print("\n\nsecond_tile", second_tile, "\n\n")
        #browser.find_element_by_xpath("//*[contains(text(),\"" + second_tile + "\")]").click()
        #browser.find_element_by_xpath("//*[codepoint-equal(string-to-codepoints(text()), string-to-codepoints(\"{}\"))]".format(second_tile)).click()
        browser.find_element_by_xpath("//*[contains(text(), \"" + first_tile + "\")]").click()

        tiles.remove(first_tile)
        tiles.remove(second_tile)






    time.sleep(6)
    browser.quit()


match_tiles()

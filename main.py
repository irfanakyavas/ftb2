import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def html_to_matchids(elem):
    return elem.get_attribute("id")[4:]


driver = webdriver.Firefox()
driver.get("https://www.flashscore.com/football/england/premier-league/results/")
assert "Premier League 2020/2021 Results" in driver.title
time.sleep(3)

trust_banner = driver.find_element_by_xpath('//*[@id="onetrust-banner-sdk"]')
driver.execute_script("arguments[0].style.visibility='hidden'", trust_banner)

all_matches_box = driver.find_element_by_class_name("sportName.soccer")
show_more_button = driver.find_element_by_class_name("event__more.event__more--static")

num_pages = 1
while show_more_button is not None:
    show_more_button.click()
    time.sleep(1.5)
    try:
        show_more_button = driver.find_element_by_class_name("event__more.event__more--static")
        num_pages = num_pages + 1
    except selenium.common.exceptions.StaleElementReferenceException:
        print(f"Number of Match Pages is {num_pages}")
        show_more_button = None
        break
    except selenium.common.exceptions.NoSuchElementException:
        print(f"Number of Match Pages is {num_pages}")
        show_more_button = None
        break

all_matches_elements = all_matches_box.find_elements_by_class_name("event__match.event__match--static.event__match--oneLine")

all_match_ids = list(map(html_to_matchids, all_matches_elements))

print(all_match_ids)

# https://www.flashscore.com/match/[matchid]/#match-summary

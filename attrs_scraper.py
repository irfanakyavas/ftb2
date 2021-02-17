from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get("https://fmdataba.com/21/l/2613/premier-league/best-players/1")
time.sleep(2.5) #2.5 saniye sayfanın yüklenmesini bekle

table = (driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/table/tbody"))
rows = table.find_elements_by_tag_name("tr")

for row in rows:
    elements = row.find_elements_by_tag_name("td")
    for index, element in enumerate(elements):
        if index == 2:
            player_name = element.find_element_by_tag_name("a")
            print(player_name.find_element_by_tag_name("strong").text)
        if index == 3:
            club_name = element.find_element_by_tag_name("a")
            print(club_name.find_element_by_tag_name("strong").text)
        # getting attributes except overall
        if index > 6:
            print(element.text)

        print(element.text)

driver.quit()

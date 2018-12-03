from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

driver = webdriver.Chrome(executable_path="/Users/takuya/PycharmProjects/web_scraping/chromedriver")
driver.get("https://www.ticket.co.jp/")
driver.find_element_by_id("js-search_word_input").send_keys("BUMP OF CHICKEN")  # 検索欄アーティスト名を入力
driver.find_element_by_class_name("form-keyword-search-btn").click()  # 検索実行

# 対象の日付のページのURLを生成 　
url = driver.current_url
url = url.split("?")[0]
print(url)
targetDate = "20181229"
target_url = url + "?st=" + targetDate
driver.get(target_url)
except_link = driver.find_element_by_link_text("除く")
except_link.click()
#driver.close()
#driver.quit()
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import sys
from time import sleep

target_date = "20181229"
target_price = 11000

driver = webdriver.Chrome(executable_path="/Users/takuya/PycharmProjects/web_scraping/chromedriver")
driver.get("https://www.ticket.co.jp/")
driver.find_element_by_id("js-search_word_input").send_keys("BUMP OF CHICKEN")  # 検索欄アーティスト名を入力
driver.find_element_by_class_name("form-keyword-search-btn").click()  # 検索実行

# 対象の日付のページのURLを生成し、遷移　
url = driver.current_url
url = url.split("?")[0]
parsed_url = urlparse(url)
target_url = url + "?st=" + target_date
driver.get(target_url)

# 取引中のものは除く
except_link = driver.find_element_by_link_text("除く")
except_link.click()

# 「安い順」を選択
order = driver.find_element_by_name('order')
order_select = Select(order)
value_path = parsed_url.path + "?st=" + target_date + '&orderable=1&order=price'
order_select.select_by_value(value_path)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
cheapest_ticket_price = int(soup.find(class_='ticket-price').get_text().replace('￥', '').replace(',', ''))
print(cheapest_ticket_price)
# 最安金額が設定金額以下だった場合、ラインに通知
if cheapest_ticket_price <= target_price:
    url = "https://notify-api.line.me/api/notify"
    token = '3bmXn7c7x6VZ2iF83RANGMiOyfOjgjOfMAEHMW6ytBa'
    headers = {"Authorization": "Bearer " + token}
    payload = {"message": driver.current_url}

    try:
        response = requests.post(url, headers=headers, params=payload)
    except Exception as e:
        print(e)

#driver.close()
#driver.quit()
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import csv

# リンク文字列
hiragana_list = [
    "あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ", "さ", "し", "す", "せ", "そ",
    "た", "ち", "つ", "て", "と", "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ",
    "ま", "み", "む", "め", "も", "や", "ゆ", "よ", "ら", "り", "る", "れ", "ろ", "わ", "を", "ん"
]
driver = webdriver.Chrome(executable_path="/Users/takuya/PycharmProjects/web_scraping/chromedriver")
driver.get("https://anime.dmkt-sp.jp/animestore/c_all_pc?initialCollectionKey=1")
results = {}
for hiragana in hiragana_list:
    # 最初のアクセス時以外、五十音順にクリックで遷移
    if hiragana != "あ":
        continue_link = driver.find_element_by_link_text(hiragana)
        continue_link.click()

    html01 = driver.page_source
    # 最後までページスクロール
    while 1:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        html02 = driver.page_source
        if html01 != html02:
            html01 = html02
        else:
            break

    soup = BeautifulSoup(html01, "html.parser")
    titleAndFavoriteCounts = soup.find_all(class_='textContainerIn')

    # {アニメタイトル: ファボ数}
    for titleAndFavoriteCount in titleAndFavoriteCounts:
        title = titleAndFavoriteCount.find(class_='ui-clamp webkit2LineClamp').get_text()
        favoriteCount = int(titleAndFavoriteCount.find(class_='favoriteCount').get_text())
        results[title] = favoriteCount

driver.close()
driver.quit()

sorted_results = {}
# 降順にソート
for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True):
    sorted_results[k] = v

print(sorted_results)
field_names = ['anime_title', 'favorite_count']

# csv出力
with open("anime_ranking.csv", "w") as f:
    writer = csv.writer(f, delimiter=';')

    # ヘッダー
    writer.writerow(field_names)

    # 各行
    for anime_title, favorite_count in sorted_results.items():
        writer.writerow((anime_title, favorite_count))


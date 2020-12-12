# can get restaurant url on ifoodie

import requests
from bs4 import BeautifulSoup

# user_search 是欲搜尋的餐廳名稱，如"巷子口食堂"
def ifoodie_url(user_search: str) -> str:
  
  # 搜尋'台北公館站'附近的餐廳
  search_url = "https://ifoodie.tw/explore/list/" + \
               user_search + \
               "?poi=%E5%8F%B0%E5%8C%97%E5%85%AC%E9%A4%A8%E7%AB%99"

  response = requests.get(search_url)
  response.encoding = "utf-8"
  soup = BeautifulSoup(response.text, "html.parser")
  sel = str(soup.select("div.title a")).split(" ")
  for i in range(len(sel)):
      if "href=" in sel[i]:
          temp = sel[i].split("=")
          fragment_url = temp[1].strip("\"")
          break

  restaurant_url = "https://ifoodie.tw" + fragment_url
  return (restaurant_url)


import requests 
import json

def getDoubanMovies():
    url = 'https://movie.douban.com/j/chart/top_list'
    params = {
        'type': 24,
        'interval_id': '100:90',
        'action': '',
        'start': 0,
        'limit': 20,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    url = 'https://movie.douban.com/j/chart/top_list'
    response = requests.get(url=url, params=params, headers=headers)
    list_data = response.json()
    fp = open('./unused/douban.json','w',encoding='utf-8')
    json.dump(list_data,fp=fp,ensure_ascii=False)
    print("success")
getDoubanMovies()
#https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start=0&limit=20
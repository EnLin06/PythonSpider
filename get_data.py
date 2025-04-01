import requests
import json
import time
import data_set
import get_school_list
from bs4 import BeautifulSoup as bs
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html",
    "Referer": "https://www.google.com"
}
database = {}
queue = Queue()

def getdata(name, id):
    url = f"https://www.cac.edu.tw/CacLink/apply114/114appLy_3Hd_SieVe_QueRy_9dS4cqa1g_Kp3z/html_sieve_114_Ja9z51F/ColPost/web/common/{id}.htm"
    req = requests.get(url, headers=headers)
    time.sleep(0.01)

    data = bs(req.text, "html.parser")
    num = data.find_all(class_= 'rlt1')
    num2 = data.find_all(class_ = 'rlt2')
    for item in num + num2:
        if item.text.strip():
            queue.put((item.text.strip(), name))
    
def data_comsume():
    global database, queue
    while not queue.empty():
        id, name = queue.get()
        if id not in database:
            database[id] = []
        database[id].append(name)

def update():
    start_time = int(time.time())
    try:
        with open('For_Fun/json/school_list.json', 'r', encoding='utf-8') as f:
            school_list = json.load(f)
    except:
        get_school_list.get_school_list()
        with open('For_Fun/json/school_list.json', 'r', encoding='utf-8') as f:
            school_list = json.load(f)

    furtures = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        for _, sub_list in school_list.items():
            for name, id in sub_list.items():
                print(f"開始執行 {name} 校系")
                furtures.append(executor.submit(getdata, name, id))
        yield "任務派發完成"

    for waiting in furtures:
        waiting.result()
    yield "子序列執行完成"

    data_comsume()
    yield "資料整理完成"
    data_set.data_set(database)
    yield "校系錄取統計完成"
    end_time = int(time.time())
    lasting = end_time - start_time
    yield f"消耗時間 : {lasting} 秒"

if __name__ == '__main__':
    steps = update()
    for step in steps:
        print(step)
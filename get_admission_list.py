import requests
import json
import time
from bs4 import BeautifulSoup as bs
school_list = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '011', '012', '013', '014', '015',
                '016', '017', '018', '019', '020', '021', '022', '023', '026', '027', '028', '030', '031', '032',
                  '033', '034', '035', '036', '038', '039', '040', '041', '042', '043', '044', '045', '046', '047',
                    '050', '051', '056', '058', '059', '060', '063', '065', '079', '099', '100', '101', '108', '109',
                      '110', '112', '113', '130', '134', '150', '151', '152', '153', '154']

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html",
    "Referer": "https://www.google.com"
}
database = {}

def get():
    for key in school_list:
        url = f"https://www.cac.edu.tw/cacportal/apply_his_report/113/113_entrance_standard/standard_{key}.html"

        req = requests.get(url , headers = headers)
        req.encoding = "utf-8"
        html = bs(req.text, "html.parser")

        def get_school_name(html):
            name = html.find("div", style="text-align:left; font-size:18px; padding-bottom:5px; padding-left:5px; font-weight:bold;")
            return name.text.split(":")[-1].strip()


        data = html.find_all("tr", bgcolor="#B4E0FF", style="font-size:16px;height:25px;")
        data2 = html.find_all("tr", bgcolor="#FBE0FB", style="font-size:16px;height:25px;")
        schname = get_school_name(html)
        if schname not in database:
            database[schname] = {}

        for item in data + data2:    
            name = item.find_all("td")
            if item and name:
                if name[1].text.strip() != "":
                    subname = name[1].text.strip()

                    if subname not in database[schname]:
                        database[schname][subname] = []

                if name[3].text.strip() != '--':
                    database[schname][subname].append(f"{name[2].text.strip()}({name[3].text.strip()}) - {name[5].text.strip()}")
                else:
                    database[schname][subname].append(f"{name[2].text.strip()} - {name[5].text.strip()}")

    with open('For_Fun/json/admission.json', 'w', encoding='utf-8') as f:
            json.dump(database, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get()
import requests
import json
import time
from bs4 import BeautifulSoup as bs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html",
    "Referer": "https://www.google.com"
}

data_ = {}

school_list = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '026', '027', '028', '030', '031', '032', '033', '034', '035', '036', '038', '039', '040', '041', '042', '043', '044', '045', '046', '047', '050', '051', '056', '058', '059', '060', '063', '065', '079', '099', '100', '101', '108', '109', '110', '112', '113', '130', '134', '150', '151', '152', '153', '154']
school_code = '001'

def get_school_list():
    for i in range(len(school_list)):
        school_code = school_list[i]
        url = f"https://www.cac.edu.tw/CacLink/apply114/114appLy_3Hd_SieVe_QueRy_9dS4cqa1g_Kp3z/html_sieve_114_Ja9z51F/ColPost/web/{school_code}.htm"
        req = requests.get(url, headers=headers)
        time.sleep(0.01)
        req.encoding = 'utf-8'
        data = bs(req.text, "html.parser")

        sub = data.find_all('tr', height="30px")
        data_[f'{school_code}'] = {}

        def get_school_name(data):
            find = data.find('tr', height="50px")
            finding = find.find('td', align="center", colspan="5")
            result = finding.find('font',  size="6").text.strip()
            return result

        schoolname = get_school_name(data)

        for item in sub:
            name = item.find('td', align="left", width="530px", id="gsdcols")
            num = item.find('a')
            if name and num:
                data_[f'{school_code}'][f'{schoolname}-{name.text.strip()}'] = str(num.text.strip())

    with open('For_Fun/json/school_list.json', 'w', encoding='utf-8') as f:
        json.dump(data_, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    get_school_list()

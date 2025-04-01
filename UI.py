import json
import get_data
import get_admission_list
import get_school_list

if __name__ == '__main__':

    try:
        with open('For_Fun/json/database.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
        with open('For_Fun/json/passcount.json', 'r', encoding='utf-8') as f:
            passcount = json.load(f)
    except:
        get_data.update()
        with open('For_Fun/json/database.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
        with open('For_Fun/json/passcount.json', 'r', encoding='utf-8') as f:
            passcount = json.load(f)


    try:
        with open('For_Fun/json/admission.json', 'r', encoding='utf-8') as f:
            adm_list = json.load(f)
    except:
        get_admission_list.get()
        with open('For_Fun/json/admission.json', 'r', encoding='utf-8') as f:
            adm_list = json.load(f)

    try:
        with open('For_Fun/json/school_list.json', 'r', encoding='utf-8') as f:
            school_list = json.load(f)
    except:
        get_school_list.get_school_list()
        with open('For_Fun/json/school_list.json', 'r', encoding='utf-8') as f:
            school_list = json.load(f)



    while True:
        id = str(input("請輸入想查詢的准考證號碼或校系名稱(輸入/off退出) : "))

        #准考證號碼
        if id in database:
            result = []
            print(f"\n准考證號碼 {id} 錄取 : ")
            for i in range(len(database[f'{id}'])):
                result.append(
                    {"錄取校系" : database[f'{id}'][i], "錄取人數" : passcount[database[f'{id}'][i]][0]}
                )
                print(f"{database[f'{id}'][i]}，該科系錄取 {passcount[database[f'{id}'][i]][0]} 人", end = "\n")
                
            print("\n====================\n")

        #退出
        elif id == "/off":
            print("感謝使用 !")
            break

        #更新資料
        elif id == '/update':
            print("更新中...這可能需要幾分鐘")
            steps = get_data.update()
            for step in steps:
                print(step)

        #校系名稱
        elif id in passcount:
            print(f"\n該校系一階通過人數 : {passcount[f'{id}'][0]} 人")
            print("通過名單(准考證號碼) : ")
            lst = ''
            for Id in passcount[f'{id}']:
                if int(Id) > 1000:
                    if int(Id) > 1000:
                        lst += Id
                        lst += ' '
            print(lst, end = '\n')
            print("錄取標準請參考", end = " : ")
            key = ""
            for code, deps in school_list.items():
                if id in deps:
                    key = code
                    break
            print(f"https://www.cac.edu.tw/CacLink/apply114/114appLy_3Hd_SieVe_QueRy_9dS4cqa1g_Kp3z/html_sieve_114_Ja9z51F/Standard/report/{key}.htm")

            
            try:
                info = id.split('-')
                print("去年(113)錄取狀況 : ")
                for data in adm_list[info[0].strip()][info[1].strip()]:
                    print(data)
            except:
                print("本科系沒有錄取資料 !")
            print("\n====================\n")

        #預期外輸入
        else:
            print("無效的輸入或沒有錄取紀錄 ! ", end = '')
            print("\n\n====================\n")

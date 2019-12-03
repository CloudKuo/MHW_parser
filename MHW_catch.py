from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import urllib3
import csv

def main_web():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    rs = requests.session()
    res = rs.get(url_first, headers=headers)
    soup = BeautifulSoup(res.text)
    # print(res.text)
    # print(len(soup.select('a.dropdown-item')))
    weapons_and_armors_url = []
    for entry in soup.select('a.dropdown-item'):
        # print(entry, entry['href'])
        if not re.search('https', entry['href']):
            if re.search('weapons', entry['href']) or re.search('armors', entry['href']):
                weapons_and_armors_url.append("https://mhw.poedb.tw"+entry['href'])
    # print(weapons_and_armors_url)
    for u in weapons_and_armors_url:
        sp = u.split('/')
        if re.search('weapons', u):
            deeper_web(u, 'weapons', sp[-1])
        else:
            deeper_web(u, 'armor', sp[-1])


def deeper_web(url, category, thing):
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    # rs = requests.session()
    # res = rs.get(url, headers=headers)
    source = urllib.request.urlopen(url).read()
    # soup = BeautifulSoup(res.text, 'lxml')
    soup2 = BeautifulSoup(source, 'lxml')
    # 一定要有lxml 不然會怪怪的
    # print(res.text)
    weapon_and_armor_dict = {}
    table = soup2.table
    print(table)
    table_rows = table.find_all('tr')
    all_list = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        # print(row)
        # print('-' * 10)
        temp_list = []
        for t in td:
            # print('-'*10)
            # print(t.text)
            span = t.find_all('span', style=True)
            # print(len(span))
            Sharpness = []
            allfull_Sharpness = []
            if len(span) > 0:
                count = 0
                for s in span:
                    cleantext = re.sub('width: ', '', s['style'])
                    cleantext = re.sub(';', '', cleantext)
                    if count <= 5:
                        Sharpness.append(cleantext)
                    else:
                        allfull_Sharpness.append(cleantext)
                    count += 1
                temp_list.append(Sharpness)
                temp_list.append(allfull_Sharpness)
                # print(s['style'])
            if not re.search('\xa0', t.text):
                temp_list.append(t.text)
        all_list.append(temp_list)
    # print(all_list)
    with open('test'+thing+'.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if category == "weapons":
            writer.writerow(['\ufeff武器', '數值', '屬性技能', '會心', '防禦', '洞數', '斬味', '有匠的斬味'])
        else:
            writer.writerow(['\ufeff防具', '數值', '屬性技能', '會心', '防禦', '洞數', '斬味', '有匠的斬味'])
        for i in all_list:
            # print(i)
            writer.writerow(i)

if __name__ == '__main__':
    url_first = "https://mhw.poedb.tw/cht/"
    main_web()
    test_url = "https://mhw.poedb.tw/cht/weapons/l_sword"
    lo_url = "http://www.lottery.gov.cn/historykj/history.jspx?_ltype=plw"
    # deeper_web(test_url)

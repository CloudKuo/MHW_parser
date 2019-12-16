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
            armor_url_get(u, 'armor', sp[-1])


def armor_url_get(url, category, thing):
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, 'lxml')
    table = soup.table
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        for t in td:
            a = t.find_all('a', style=True)
            for aa in a:
                # print(aa['href'])
                # 每個防具細部的url
                each_armor_url = "https://mhw.poedb.tw/" + aa['href']
                # print(each_armor_url)
                armor_get(each_armor_url)


def armor_get(url):
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, 'lxml')
    table = soup.table
    table_rows = table.find_all('tr')
    save_list = []
    icon_dict = {'224': "頭盔", '225': "鎧甲", '226': "腕甲", '227': "腰甲", '228': "護腿"
        , '066': '一級洞', '067': '二級洞', '068': '三級洞'}
    for tr in table_rows:
        td = tr.find_all('td')
        tmp_list = []
        for t in td:
            # print(t.text)
            # print(td.index(t))
            span = t.find_all('span')
            icon_text = ''
            if span:
                for content in span:
                    # print(type(''.join(content['class'])))
                    img = content.find_all('img')
                    for img_text in img:
                        # print(img_text)
                        # print(''.join(img_text['style']))
                        icon = ''.join(re.findall("icon/(.+).png", ''.join(img_text['style'])))
                        # print(icon_dict[icon])
                        icon_text = icon_dict[icon]
            if td.index(t) == 0 or td.index(t) == 8:
                tmp_list.append(icon_text)
            else:
                trans = re.sub("&dash;", "~", t.text)
                tmp_list.append(trans)
            # print()
            # tmp_list[0][0] = icon_text
        if tmp_list:
            save_list.append(tmp_list)
    name = url.split('/')[-1]
    # print(save_list)
    save(name, 'armors', save_list)


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
    table = soup2.table
    # print(table)
    table_rows = table.find_all('tr')
    all_list = []
    for tr in table_rows:
        td = tr.find_all('td')
        # row = [i.text for i in td]
        # print(tr.contents)
        # print(row)
        temp_list = []
        # 暫時存所有一個tr的原件
        for t in td:
            # print('-'*10)
            # print(t.text)
            span = t.find_all('span', style=True)
            # img = t.find_all('img', style=True)
            # for i in img:
            #     print(i['style'])
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
    # save(thing, category, all_list)


def save(thing, category, your_list):
    with open(thing+'.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if category == "weapons":
            writer.writerow(['\ufeff武器', '數值', '屬性技能', '會心', '防禦', '洞數', '斬味', '有匠的斬味'])
        else:
            writer.writerow(['\ufeff防具圖片', '防具', '防禦', '火屬性防禦', '水屬性防禦', '電屬性防禦', '冰屬性防禦', '龍屬性防禦', '洞數', '技能'])
        for i in your_list:
            # print(i)
            writer.writerow(i)


if __name__ == '__main__':
    url_first = "https://mhw.poedb.tw/cht/"
    # main_web()
    test_url = "https://mhw.poedb.tw/cht/weapons/l_sword"
    # deeper_web(test_url)
    armor_url_get("https://mhw.poedb.tw/cht/armors/8", "armor", "1")

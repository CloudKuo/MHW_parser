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
            if re.search('bow', u):
                bow_get(u, 'weapons', sp[-1])
            elif re.search('bg', u):
                bg_get(u, 'weapons', sp[-1])
            else:
                weapon_get(u, 'weapons', sp[-1])
        else:
            armor_url_get(u, 'armor', sp[-1])


def bg_get(url, category, thing):
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, 'lxml')
    table = soup.table


def bow_get(url, category, thing):
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, 'lxml')
    table = soup.table


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
                armor_get(each_armor_url, thing)


def armor_get(url, thing):
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, 'lxml')
    table = soup.table
    table_rows = table.find_all('tr')
    save_list = []

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
    save(thing, 'armors', save_list)


def weapon_get(url, category, thing):
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    # rs = requests.session()
    # res = rs.get(url, headers=headers)
    source = urllib.request.urlopen(url).read()
    soup2 = BeautifulSoup(source, 'lxml')
    # 一定要有lxml 不然會怪怪的
    table = soup2.table
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
            # span = t.find_all('span', style=True)
            Sharpness = []
            allfull_Sharpness = []
            icon_text = ''
            all_span = t.find_all('span')
            count = 0
            for content in all_span:
                try:
                    print(td.index(t), content['style'])
                    # print(count)
                    cleantext = re.sub('width: ', '', content['style'])
                    cleantext = re.sub(';', '', cleantext)
                    if count <= 5:
                        Sharpness.append(cleantext)
                    else:
                        allfull_Sharpness.append(cleantext)
                    count += 1
                except KeyError:
                    img = content.find_all('img')
                    for img_text in img:
                        # print(img_text)
                        # print(''.join(img_text['style']))
                        icon = ''.join(re.findall("icon/(.+).png", ''.join(img_text['style'])))
                        # print(icon_dict[icon])
                        try:
                            icon_text = icon_dict[icon]
                        except KeyError as m:
                            print(m)
                            # 如果找不到icon圖片就印出
            if Sharpness and allfull_Sharpness:
                temp_list.append(Sharpness)
                temp_list.append(allfull_Sharpness)
                # print(s['style'])
            if td.index(t) == 0:
                temp_list.append(icon_text)
                temp_list.append(t.text)
            elif td.index(t) == 5:
                temp_list.append(icon_text)
            elif not re.search('\xa0', t.text):
                temp_list.append(t.text)
        all_list.append(temp_list)
    # print(all_list)
    del all_list[0]
    save(thing, category, all_list)


def save(thing, category, your_list):
    with open(thing+'.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if category == "weapons":
            writer.writerow(['\ufeff武器圖片', '武器', '數值', '屬性技能', '會心', '防禦', '洞數', '斬味', '有匠的斬味'])
        else:
            writer.writerow(['\ufeff防具圖片', '防具', '防禦', '火屬性防禦', '水屬性防禦', '電屬性防禦', '冰屬性防禦', '龍屬性防禦', '洞數', '技能'])
        for i in your_list:
            # print(i)
            writer.writerow(i)


if __name__ == '__main__':
    icon_dict = {'224': "頭盔", '225': "鎧甲", '226': "腕甲", '227': "腰甲", '228': "護腿"
        , '066': '一級洞', '067': '二級洞', '068': '三級洞', '241': '大劍', '242': '太刀',
                 '240': '單手劍', '243': '雙手劍', '246': '大錘',
                 '247': '狩獵笛', '244': '長槍', '245': '銃槍', '248': '斬擊斧',
                 '249': '充能斧', '250': '操蟲棍', '251': '輕弩', '252': '重弩', '253': '弓'}
    url_first = "https://mhw.poedb.tw/cht/"
    # 首頁
    # main_web()
    test_url = "https://mhw.poedb.tw/cht/weapons/l_sword"

    weapon_get(test_url, "weapons", "2")
    # armor_url_get("https://mhw.poedb.tw/cht/armors/8", "armor", "1")

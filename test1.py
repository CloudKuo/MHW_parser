import tkinter
import re
from bs4 import BeautifulSoup
import urllib.parse
import requests
import urlparser
import threading


def get_result(keyword):
    # keyword = urllib.parse.quote(('"' + input("你要的關鍵字\n") + '"').encode())
    keyword = urllib.parse.quote(keyword.encode())
    print(keyword)
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    # keyword = urllib.parse.quote("mos".encode())
    # quote 用意是quoting special characters and appropriately encoding non-ASCII text.
    # 加雙引號可以精準搜尋
    # url = "https://www.google.com.tw/search?num=50&q=" + keyword + "&oq=" + keyword + "&dcr=0&tbas=0&source=lnt&tbs=qdr:d&tbs=qdr:d"
    # 上面的會限時24小時內的
    url = "https://www.google.com.tw/search?num=50&q=" + keyword
    # 這個會搜尋全部
    # url = "https://www.google.com.tw/search?num=50&q="+keyword+"&oq="+keyword+"&dcr=0&tbm=nws&source=lnt&tbs=qdr:d"
    # 上面的話就是只搜尋新聞頁面 差在有&tbm=nws
    title_list = []
    url_list = []
    con_list = []
    print(url)
    res = requests.get(url, headers=user_agent)
    if res.status_code == 200:
        # print(res.content)
        content = res.content
        # print(content)
        soup = BeautifulSoup(content, "html.parser")
        # print(soup.find_all('div'))
        items = soup.findAll("div", {"class": "g"})
        # print(items)
        for item in items:
            # title
            try:
                title = item.find("div", {"class": "r"}).find("h3").text
                print(title)
                title_list.append(title)
                #     所有搜尋結果的標題
                href = item.find("div", {"class": "r"}).find("a").get("href")
                # 所有結果的url
                url_list.append(href)
                # print(href)
                condition = item.find("span", {"class": "st"}).text
                # print(condition)
                con_list.append(condition)
                #           結果的狀態表
            except AttributeError:
                pass
    listbox = tkinter.Listbox(F, width= 50)
    for i in title_list:
        listbox.insert(title_list.index(i)+1, i)
    listbox.pack()


def search_thread():
    s_thr = threading.Thread(target=get_result(query_st.get()))
    s_thr.start()


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title('EZ Google query')
    root.geometry('500x500')
    F = tkinter.Frame(root, background='black')
    query_st = tkinter.StringVar(F)
    search_entry = tkinter.Entry(F, textvariable=query_st)
    search_btn = tkinter.Button(F, text="Search Now!", command=search_thread)
    search_entry.pack()
    search_btn.pack()
    F.pack(fill="both", expand=True)
    # root.resizable(0, 0)
    root.mainloop()





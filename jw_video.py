#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from datetime import datetime
import re,os,sys
from distutils.util import strtobool

print("請輸入語言：\n(1)繁體中文\n(2)日本語")
language=input("您輸入的語言為：")
if language=="1":
    language="CH"
elif language=="2":
    language="J"
else:
    sys.exit("程式關閉：語言輸入錯誤！")

category_dic={
    "StudioMonthlyPrograms":"JW電視網-每月節目",
    "StudioTalks":"JW電視網-演講",
    "StudioNewsReports":"新聞與宣布",
    "VODPgmEvtMorningWorship":"早晨崇拜",
    "VODPgmEvtSpecial":"特別節目",
    "VODPgmEvtGilead":"基列學校畢業典禮",
    "VODPgmEvtAnnMtg":"年會"
}
category_list=["StudioMonthlyPrograms","StudioTalks","StudioNewsReports","VODPgmEvtMorningWorship","VODPgmEvtSpecial",
              "VODPgmEvtGilead","VODPgmEvtAnnMtg"]
print("\n目錄：")
for cat in category_list:
    print("(",category_list.index(cat),")",category_dic[cat])

try:
    _input=int(input("請輸入你想查詢的類別："))
except:
    sys.exit("輸入錯誤！只可以輸入數字")
if _input> len(category_list):
    sys.exit("輸入錯誤！你輸入的數字不在選項內")
print("\n查詢日期範圍：")
search_start_date=input("開始日期 start date (yyyy-mm-dd):")
search_start_date=datetime.strptime(search_start_date, "%Y-%m-%d")
search_end_date=input("截止日期 end date (yyyy-mm-dd):")
search_end_date=datetime.strptime(search_end_date, "%Y-%m-%d")
date=[]
try:
    subtitle_download=bool(strtobool(input("是否需要下載字幕？（Y/n）:")))
except:
    sys.exit("輸入錯誤！請輸入Y或N")
print("\n")
timestamp="[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
regex=re.compile(timestamp)


url="https://b.jw-cdn.org/apis/mediator/v1/categories/"+language+"/"+category_list[_input]+"?detailed=1&clientType=www"
result=requests.get(url).json()

for media in result["category"]["media"]:
    highest=len(media["files"])-1
    publish_data=media["firstPublished"][:10]
    publish_data=datetime.strptime(publish_data, "%Y-%m-%d")
    if search_start_date<=publish_data <= search_end_date:
        date.append(publish_data)
        print("影片名稱：",media["title"])
        print("影片日期：",media["firstPublished"][:10])
        print("影片下載：",media["files"][highest]["progressiveDownloadURL"])
        if "subtitles" in media["files"][highest].keys():
            print("是否有字幕檔案：True","\n")
        else:
            print("是否有字幕檔案：False","\n")
        if subtitle_download is True:
            if "subtitles" in media["files"][highest].keys():
                download_url=media["files"][highest]["subtitles"]["url"]
                subtitle_file=requests.get(download_url).text.splitlines()
                subtitle=""
                for sub in subtitle_file:
                    if regex.search(sub) is None and sub!="" and sub!="WEBVTT":
                        subtitle=subtitle+"\n"+sub                    
                with open (media["title"]+".txt","w") as f:
                    f.write(subtitle[1:])
            else:
                print(media["title"],"沒有字幕")
if date !=[]:       
    if subtitle_download is True :
        print("字幕已全部下載完成！檔案已存放在以下位置：",os.getcwd())
else:
    print("搜尋範圍沒有任何影片")


# In[ ]:





# In[ ]:





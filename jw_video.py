import requests,readline
from datetime import datetime
import re,os,sys
from distutils.util import strtobool
# 選擇語言
os.system("clear")
print("請輸入您想使用的語言：\n(1)繁體中文\n(2)日本語\n(3)English")
language=input("您輸入的語言為：")
if language=="1":
    language="CH"
elif language=="2":
    language="J"
elif language=="3":
    language="E"
else:
    sys.exit("程式關閉：語言輸入錯誤！")
# 第一層目錄
os.system("clear")
key1=""
url="https://b.jw-cdn.org/apis/mediator/v1/categories/"+language+"/VideoOnDemand?detailed=1&clientType=www"
category_list_1=requests.get(url).json()["category"]["subcategories"]
while key1 != "q":
    for sub_category in category_list_1:
        print("("+str(category_list_1.index(sub_category))+")",sub_category["name"])
    print("(q)結束程式")
    key1=input("請選擇：")
    if key1=="q":
        quit()
    os.system("clear")
    key1=int(key1)
    url="https://b.jw-cdn.org/apis/mediator/v1/categories/"+language+"/"+category_list_1[key1]["key"]+"?detailed=1&clientType=www"
    category_list_2=requests.get(url).json()["category"]["subcategories"]
    key2=""
    # 第二層目錄
    while key2!="q":
        for sub_category in category_list_2:
            print("("+str(category_list_2.index(sub_category))+")",sub_category["name"])
        print("(q)回上一層")
        key2=input("請選擇：")
        if key2=="q":
            break
        os.system("clear")
        key2=int(key2)

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

        timestamp="[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
        regex=re.compile(timestamp)
        url="https://b.jw-cdn.org/apis/mediator/v1/categories/"+language+"/"+category_list_2[key2]["key"]+"?detailed=1&clientType=www"
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
                print("字幕已全部下載完成！檔案已存放在以下位置：",os.getcwd(),"\n")
        else:
            print("搜尋範圍沒有任何影片\n")
    os.system("clear")

#for study purposes only

import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from youtube_search import YoutubeSearch
from pytube import YouTube

argv = sys.argv[1:]
folder = os.getcwd()
downloadFolder = folder + "/spotifydl"
driver = folder + '/chromedriver'
url = input("What's the link: ")
i = 1
p = 0
w = 1
q = 0
m = 0
b = 0
counter = 0
originalLink = "https://www.youtube.com"
# 打开网页，并自动下滑（不下滑有数量限制)，去拿到规定数量的所有网站链接
ser = Service(driver)
driver = webdriver.Chrome(service=ser)
driver.get(url)
time.sleep(2)
name_list = []
while w < 100:
    try:
        page = driver.find_element(
            By.XPATH,
            "/html/body/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div/section/div[2]/div[3]/div/div[2]/div[2]/div[{}]/div/div[2]/div/a/div".format(
                w
            ),
        )
        driver.execute_script("arguments[0].scrollIntoView();", page)
        time.sleep(1)
        info = driver.page_source
        # print(info)
        newinfo = BeautifulSoup(info, "html.parser")
        # print(newinfo)
        names = newinfo.find_all(
            "div",
            class_="Type__TypeElement-goli3j-0 gwYBEX t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line",
        )
        for i in names:
            nam = i.get_text()
            if nam not in name_list:
                name_list.append(nam)
        time.sleep(1)
    except:
        print("Working")
    w += 2
    q += 1
# print(w)
print(name_list)
# print(q)
new_links = []
for name in name_list:
    # print(name)
    result = YoutubeSearch(name, max_results=1).to_dict()
    result = result[0]
    # print(result)
    for key, value in result.items():
        if key == "url_suffix":
            new_link = originalLink + value
            # print(new_link)
            new_links.append(new_link)
for link in new_links:
    print("Start Downloading!")
    yt = YouTube(link)
    try:
        ys = yt.streams.get_by_itag(251)
    except:
        ys = yt.streams.get_by_itag(140)
    print("")
    print("Now Downloading: " + name_list[p])
    try:
        download = ys.download(downloadFolder)
        for filename in os.listdir(downloadFolder):
            n = filename.split(".")[0]
            filename = downloadFolder + "/" + filename
            n = downloadFolder + "/" + n
            if filename.endswith(".webm"):  # or .avi, .mpeg, whatever.
                os.system(
                    'ffmpeg -i "{}" -vn -ab 128k -ar 44100 -y "{}.mp3"'.format(
                        filename, n
                    )
                )
                os.remove(download)
            # print("Changing done")
            elif filename.endswith("mp4"):
                os.system('ffmpeg -i "{}"" "{}.mp3"'.format(filename, n))
            else:
                continue
    except:
        print("Song not find")
    p += 1
print("Download Finished!")


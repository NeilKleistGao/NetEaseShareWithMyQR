#!/usr/bin/python2.7  
# -*- coding: utf-8 -*-  
import os
import urllib2
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from MyQR import myqr
from NetEaseMusicApi import search_album_id_by_name, search_song_id_by_name

music_link = "http://music.163.com/m/song?id="
album_link = "http://music.163.com/album/"

def createQR(link, cover, name):
    version, level, qr_name = myqr.run(
	link,
    version=1,
    level='H',
    picture=cover,
    colorized=True,
    contrast=1.0,
    brightness=1.0,
    save_name=name,
    save_dir=os.getcwd()
	)
    print("网易云音乐分享二维码%s已经被保存至 %s" % (name, os.getcwd()))

def getLink(name, sharing_type):
    if sharing_type == '1':
        id = search_song_id_by_name(name)
        if not id == None:
            return music_link + str(id)
    else:
        id = search_album_id_by_name(name)
        if not id == None:
            return album_link + str(id)
        
def downloadImage(link, name):
    request = urllib2.Request(link)
    request.add_header("Cookie", "appver=1.5.0.75771")
    request.add_header("Referer", "http://music.163.com")
    response = urllib2.urlopen(request)
    fp = open(name, "wb")
    fp.write(response.read())
    fp.close()

def getImageUrl(link):
    drive = webdriver.PhantomJS()
    drive.get(link)
    drive.switch_to.frame("g_iframe")
    html = drive.page_source
    soup = BeautifulSoup(html, "lxml")
    src = soup.find(type="application/ld+json").string
    pt = r'"images": \["(.*)"\]'
    return re.search(pt, soup.find(type="application/ld+json").string).group(1)

def tempDelete():
    os.remove("temp.jpg")

if __name__ == "__main__":
    print("我想要分享：\n[1]单曲\n[2]专辑\n")
    while True:
        sharing_type = raw_input("")
        if sharing_type == '1' or sharing_type == '2':
            name = raw_input("歌曲名 or 专辑名：")
            link = getLink(name, sharing_type)
            if link == None:
                print("woops!未找到相关内容...")
                break
            #print getImageUrl(link)
            downloadImage(getImageUrl(link), "temp.jpg")
            createQR(link, "temp.jpg", name + ".png")
            break
        else:
            print("woops!输入不符合要求，请重新输入...")
    tempDelete()
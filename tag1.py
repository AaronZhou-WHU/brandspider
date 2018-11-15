#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author : zhoubin
# @datetime: 18/11/14 13:39
# @description : 抓取每个品牌下所有的标签 https://i.paizi.com/
import threading
from urllib import request
import os
import re
from bs4 import BeautifulSoup            #Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库

'''
获取所有商标的链接a-z，以及其他
'''
def getAllLinks():
    url = "https://i.paizi.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url, headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody
    soup = BeautifulSoup(page_info, 'html.parser')
    links = soup.find_all(name='a', text=re.compile("更多"))
    print("所有的链接")
    urlLink = []
    for link in links:
        urlLink.append(link['href'])
    return urlLink

'''
获取每一个商标链接中所有的商标及其tag链接
'''
def getEveryLinkInfo(url,index):
    preurl = "https://i.paizi.com"
    uurl = "https:" + url
    print(uurl)

    getinfofromurl(uurl,index)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(uurl, headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody
    soup = BeautifulSoup(page_info, 'html.parser')
    next_page_soup = soup.find(class_='pages clear')
    next_page_soup_find_all = next_page_soup.find_all(name='a')
    next_page_link_list = []

    for next_link in next_page_soup_find_all:
        if (str(next_link.get('href')) == 'None'):
            continue
        if (next_link.string == '下一页'):
            continue
        next_page_link_list.append(next_link.get('href'))

    if (len(next_page_link_list) > 0):
        first_link = next_page_link_list[0]
        last_index = (str(next_page_link_list[-1])[-1])
        next_page_link_list = []
        # next_page_link_list.append(first_link)
        for index in range(2, int(last_index) + 1):
            next_page_link_list.append(str(first_link) + '-' + str(index))
        for link in next_page_link_list:
            next_page_url = preurl + '/' + str(link)
            getinfofromurl(next_page_url,index)

'''
爬取uurl中的商标名称，存入txtname文件中
'''
def getinfofromurl(uurl,index):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(uurl, headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody
    soup = BeautifulSoup(page_info, 'html.parser')
    ul_soup = soup.find(class_="c03-3-1")
    ul_soup_find_all = ul_soup.find_all(name='a')
    #print(ul_soup_find_all)
    for contnt in ul_soup_find_all:
        tmpurl = contnt.get('href')
        brandurl = "https:" + tmpurl
        if('dp' in brandurl):
            writeTaginfo(brandurl,contnt.string,index)

'''
爬取url中的商标所对应的标签，存入以商标名字为txtname的文件中
'''
def writeTaginfo(url,brandname,index):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url, headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody
    soup = BeautifulSoup(page_info, 'html.parser')
    ul_soup = soup.find(class_="c02-1-3")
    ul_soup_find_all = ul_soup.find_all(name='a')
    if('/' in brandname):
        brandname=brandname.replace('/','-')
    newtxtname = str(index)+"/"+brandname + '.txt'
    print(newtxtname)
    folder_path = str(index)+"/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for contnt in ul_soup_find_all:
        if(contnt.string=='更多+'):
            continue
        #print(contnt)
        with open(newtxtname, "a") as file:  # 在磁盘以只写的方式打开/创建一个名为 articles 的txt文件
            file.write(contnt.string + '\n')
            print(contnt.string)



if __name__ == '__main__':
    if (not os.path.exists('tag')):
        os.mkdir('tag')
        os.chdir("tag")
    allLinks = getAllLinks()
    threads = []
    index =0
    for link in allLinks:
        index += 1
        #print(link)
        # if (link != '//i.paizi.com/dp-r'):
        #     continue
        t = threading.Thread(target=getEveryLinkInfo, args=(link,index,))
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()


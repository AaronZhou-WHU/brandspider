#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author : zhoubin
# @datetime: 18/11/5 14:44
# @description : https://i.paizi.com/ 爬下品牌名称存为txt
from urllib import request

import re
from bs4 import BeautifulSoup            #Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库

#构造头文件，模拟浏览器访问
url="https://i.paizi.com"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
page = request.Request(url,headers=headers)
page_info = request.urlopen(page).read().decode('utf-8')#打开Url,获取HttpResponse返回对象并读取其ResposneBody

# print(page_info)

# 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
soup = BeautifulSoup(page_info, 'html.parser')
# 以格式化的形式打印html
#print(soup.prettify())
#获取所有的链接
links = soup.find_all(name='a',text=re.compile("更多"))
print ("所有的链接")
urlLink =[]
for link in links:
    # if(link.string.find("更多")):
    #print(link.string)
    urlLink.append(link['href'])
    print(link.name,link['href'],link.get_text())

print(len(urlLink))

'''
爬取uurl中的商标名称，存入txtname文件中
'''
def getinfofromurl(uurl,txtname):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(uurl, headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody
    soup = BeautifulSoup(page_info, 'html.parser')
    ul_soup = soup.find(class_="c03-3-1")
    ul_soup_find_all = ul_soup.find_all(name='a')
    for contnt in ul_soup_find_all:
        with open(txtname, "a") as file:  # 在磁盘以只写的方式打开/创建一个名为 articles 的txt文件
            file.write(contnt.string + '\n')
            print(contnt.string)


ii=1
for uurl in urlLink:
    uurl="https:"+uurl
    print(uurl)
    txtname = str(ii) + '.txt'
    ii += 1
    getinfofromurl(uurl,txtname)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(uurl, headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody
    soup = BeautifulSoup(page_info, 'html.parser')
    next_page_soup = soup.find(class_='pages clear')
    next_page_soup_find_all = next_page_soup.find_all(name='a')
    next_page_link_list = []

    for next_link in next_page_soup_find_all:
        if(str(next_link.get('href'))=='None'):
            continue
        if(next_link.string=='下一页'):
            continue
        next_page_link_list.append(next_link.get('href'))

    if(len(next_page_link_list)>0):
        first_link = next_page_link_list[0]
        last_index = (str(next_page_link_list[-1])[-1])
        next_page_link_list = []
        #next_page_link_list.append(first_link)
        for index in range(2,int(last_index)+1):
            next_page_link_list.append(str(first_link)+'-'+str(index))
        for link in next_page_link_list:
            print(link)
            next_page_url = url + '/' + str(link)
            getinfofromurl(next_page_url, txtname)

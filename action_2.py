# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page_content(request_url):
    # 得到页面的内容
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers=headers, timeout=10)
    content = html.text
    # print(content)

    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup


# 分析当前页面的投诉
def analysis(soup):
    # 找到完整的投诉信息框
    temp = soup.find('div', class_="tslb_b")
    # 创建DataFrame
    df = pd.DataFrame(columns=['投诉编号', '投诉品牌', '投诉车系', '投诉车型', '问题简述', '典型问题', '投诉时间', '投诉状态'])
    tr_list = temp.find_all('tr')
    for tr in tr_list[1:]:
        # ToDo：提取汽车投诉信息
        dic = {}
        td_list = tr.find_all('td')
        dic['投诉编号'] = td_list[0].text
        dic['投诉品牌'] = td_list[1].text
        dic['投诉车系'] = td_list[2].text
        dic['投诉车型'] = td_list[3].text
        dic['问题简述'] = td_list[4].text
        dic['典型问题'] = td_list[5].text
        dic['投诉时间'] = td_list[6].text
        dic['投诉状态'] = td_list[7].find('em').string
        df = df.append(dic,ignore_index=True)
    return df


page_num = 20
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'

result = pd.DataFrame(columns=['投诉编号', '投诉品牌', '投诉车系', '投诉车型', '问题简述', '典型问题', '投诉时间', '投诉状态'])
for i in range(page_num):
    request_url = base_url + str(i + 1) + '.shtml'
    soup = get_page_content(request_url)
    #print(request_url)
    df = analysis(soup)
    #print(df)
    result = result.append(df)

result.to_csv('car_complain.csv', index=False)

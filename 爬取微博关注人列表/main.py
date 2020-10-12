from lxml import etree
import requests
import re
import pandas as pd
import time
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'cookie': '换上你自己的id',
}
def get_parse(url,id):
    html = requests.get(url,headers=headers)
    if html.status_code ==200:
        get_html(html,id)
    else:
        print(html.status_code)
def get_html(html,id):
    content = html.text
    yeshus = re.compile('type="hidden" value="(\d+)"')
    yeshu = yeshus.findall(content)
    if int(yeshu[0]) >5:
        for i in range(1, 6, 1):
            url = 'https://weibo.cn/{}/follow?page={}'.format(id,i)
            html = requests.get(url, headers=headers)
            content1 = html.text
            name_list = []
            href_list = []
            soup = etree.HTML(content1.encode('utf-8'))
            name = soup.xpath("//td[@valign ='top']/a/text()")
            href = soup.xpath("//td[@valign ='top']/a/@href")
            for n in name[::2]:
                name_list.append(n)
            for h in href[::3]:
                h = h.replace('https://weibo.cn/u/', '').replace('https://weibo.cn/', '')
                href_list.append(h)
            time.sleep(1)
            print(href_list, name_list)
            dowload(name_list, href_list, id)
    elif int(yeshu[0]) <=5:
        for i in range(1,int(yeshu[0])+1,1):
            url = 'https://weibo.cn/{}/follow?page={}'.format(id,i)
            html = requests.get(url, headers=headers)
            content2 = html.text
            name_list = []
            href_list = []
            soup = etree.HTML(content2.encode('utf-8'))
            name = soup.xpath("//td[@valign ='top']/a/text()")
            href = soup.xpath("//td[@valign ='top']/a/@href")
            for n in name[::2]:
                name_list.append(n)
            for h in href[::3]:
                h = h.replace('https://weibo.cn/u/', '').replace('https://weibo.cn/', '')
                href_list.append(h)
            time.sleep(1)
            print(href_list, name_list)
            dowload(name_list, href_list, id)
def dowload(name_list,href_list,id):
    df = pd.DataFrame()
    df['name'] = name_list
    df['id'] = href_list
    try:
        df.to_csv("{}.csv".format(id), mode="a+", header=None, index=None, encoding="gbk")
        print("写入成功")
    except:
        print("当页数据写入失败")
if __name__ == '__main__':
    id = pd.read_excel('gaoguan_name_id.xlsx')
    for i in id['id'][0:5]:
        url = 'https://weibo.cn/{}/follow'.format(i)
        get_parse(url,i)
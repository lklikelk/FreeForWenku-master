import requests
import re
import argparse
import sys
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("url", help="Target Url,你所需要文档的URL", type=str)
parser.add_argument('type', help="Target Type,你所需要文档的的类型(DOC|PPT|TXT|PDF)", type=str)
args = parser.parse_args()

url = args.url
type = args.type

# 根据文件决定函数
y = 0

headers = {
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/72.0.3626.121 Safari/537.36',

    }

def DOC(url):
    doc_id = re.findall('view/(.*).html', url)[0]
    html = requests.get(url).text
    lists = re.findall('(https.*?0.json.*?)\\\\x22}', html)
    lenth = (len(lists) // 2)
    NewLists = lists[:lenth]
    filename=getfilename(url)+'.doc'
    for i in range(len(NewLists)):
        NewLists[i] = NewLists[i].replace('\\', '')
        txts = requests.get(NewLists[i]).text
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),', txts)

        for i in range(0, len(txtlists)):
            global y
            print(txtlists[i][0].encode('utf-8').decode('unicode_escape', 'ignore'))
            if y != txtlists[i][1]:
                y = txtlists[i][1]
                n = '\n'
            else:
                n = ''
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(n + txtlists[i][0].encode('utf-8').decode('unicode_escape', 'ignore').replace('\\', ''))
        print("文档保存在" + filename)


def PPT(url):
    doc_id = re.findall('view/(.*).html', url)[0]
    url2 = "https://wenku.baidu.com/browse/getbcsurl?doc_id=" + doc_id + "&pn=1&rn=99999&type=ppt"
    html = requests.get(url2).text
    lists = re.findall('{"zoom":"(.*?)","page"', html)
    filename = getfilename(url)
    for i in range(0, len(lists)):
        lists[i] = lists[i].replace("\\", '')
    try:
        os.mkdir(filename)
    except:
        pass
    for i in range(0, len(lists)):
        img = requests.get(lists[i]).content
        with open(filename + '\img' + str(i) + '.jpg', 'wb') as m:
            m.write(img)
    print("PPT图片保存在" + filename + "文件夹")


def TXT(url):
    doc_id = re.findall('view/(.*).html', url)[0]
    url2 = "https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=" + doc_id
    html = requests.get(url2).text
    md5 = re.findall('"md5sum":"(.*?)"', html)[0]
    pn = re.findall('"totalPageNum":"(.*?)"', html)[0]
    rsign = re.findall('"rsign":"(.*?)"', html)[0]
    NewUrl = 'https://wkretype.bdimg.com/retype/text/' + doc_id + '?rn=' + pn + '&type=txt' + md5 + '&rsign=' + rsign
    txt = requests.get(NewUrl).text
    jsons = json.loads(txt)
    texts = re.findall("'c': '(.*?)',", str(jsons))
    print(texts)
    filename = getfilename(url)
    filename = filename + '.txt'
    with open(filename, 'a', encoding='utf-8') as f:
        for i in range(0, len(texts)):
            texts[i] = texts[i].replace('\\r', '\r')
            texts[i] = texts[i].replace('\\n', '\n')

            f.write(texts[i])
    print("文档保存在" + filename)


def PDF(url):
    doc_id = re.findall('view/(.*).html', url)[0]
    url2 = "https://wenku.baidu.com/browse/getbcsurl?doc_id=" + doc_id + "&pn=1&rn=99999&type=ppt"
    html = requests.get(url2).text
    filename = getfilename(url)
    lists = re.findall('{"zoom":"(.*?)","page"', html)
    for i in range(0, len(lists)):
        lists[i] = lists[i].replace("\\", '')
    try:
        os.mkdir(filename)
    except:
        pass
    for i in range(0, len(lists)):
        img = requests.get(lists[i]).content
        with open(filename + '\img' + str(i) + '.jpg', 'wb') as m:
            m.write(img)
    print("FPD图片保存在" + filename + "文件夹")


def getfilename(url):
    response = requests.get(url,headers=headers)
    from lxml import etree
    html = etree.HTML(response.text)
    # 使用text提取文本,ppt,txt
    if type.upper() in 'PPT,TXT':
        file_name = html.xpath('//*[@id="doc-tittle-2"]/text()')[0]
        print(file_name)
    # pdf,doc
    else:
        file_name = html.xpath('//*[@id="doc-tittle-0"]/text()')[0]
        print(file_name)
    # doc

    # txt
    print(file_name)
    return file_name


if __name__ == "__main__":
    try:
        print(url)
        print(type.upper())
        eval(type.upper())(url)
    except:
        print("获取出错，可能URL错误\n使用格式wenkudownload url type\n请使用--help查看帮助")

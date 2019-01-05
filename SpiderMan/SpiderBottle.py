# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 下午7:27
# @Author  : shaopengwei@baidu.com
# @File    : SpiderBottle.py
# -------------------------------------------------

import requests
from bs4 import BeautifulSoup
import wechatsogou
import time
import urllib2
import urllib
import re
import json

class SpiderBottle:

    """
    spider1:从百度搜索爬取数据
    """
    def spiderBaiduSearch(self, keyWord, pageSize):
        if (keyWord == '') or (pageSize < 0):
            return False

        result = []
        url = "http://www.baidu.com/s"
        for i in range(0, pageSize):
            try:
                requestData = {
                    'wd': "%s" % (keyWord),
                    'pn': str(i * 10),
                    'tn': 'baidurt',
                    'ie': 'utf-8',
                    'bsst': '1'
                }
                ret = requests.get(url, params=requestData)
                soup = BeautifulSoup(ret.text, 'html.parser')
                for h3 in soup.find_all("h3", class_='t'):
                    result.append(h3.find('a').get('href'))
                time.sleep(3)
            except Exception as err:
                print(err)

        return result

    """
    spider2:搜狗微信检索接口
    """
    def spiderSogoWeixinSearch(self, identifyCodeTime, keyWord, pageSize):
        if (keyWord == '') or (pageSize < 0):
            return False

        if identifyCodeTime <= 0:
            identifyCodeTime = 1

        ws_api = wechatsogou.WechatSogouAPI(identifyCodeTime)
        result = []
        for i in range(0, pageSize):
            try:
                pageInfo = ws_api.search_article(keyWord, i+1)
                for j in range(0, len(pageInfo)):
                    result.append(pageInfo[j]['article']['url'])
                time.sleep(3)
            except Exception as err:
                print(err)

        return result

    """
    spider3:搜狐美食多个页面的解析（目前只支持一种解析）
            http://chihe.sohu.com
    """
    def spiderSohuMeishi(self, urlList):
        if len(urlList) <= 0:
            return False

        result = []
        for i in range(0, len(urlList)):
            try:
                content = {}
                r = requests.get(urlList[i])
                soup = BeautifulSoup(r.text, "html.parser")
                # title
                content['title'] = soup.find(class_='text-title').h1.contents[0]
                # content
                content['content'] = ""
                for string in soup.find(class_='article').stripped_strings:
                    content['content'] = content['content'] + string + "\n"

                # 将文章内容保存到结果
                result.append(json.dumps(content, ensure_ascii=False))
                # 休眠3s
                time.sleep(3)
            except Exception as err:
                print(err)

        return result

    """
    spider4:美食杰网站内容多个页面的解析（目前只支持一种解析）
            http://www.meishij.net
    """
    def spiderMeshij(self, urlList):
        if len(urlList) < 0:
            return False

        result = []
        for i in range(0, len(urlList)):
            try:
                content = {}
                r = requests.get(urlList[i])
                soup = BeautifulSoup(r.text, "html.parser")
                # title
                content['title'] = soup.find(class_='info1').h1.a.contents[0]
                # content
                content['content'] = ""
                for string in soup.find(class_='edit edit_class_0 edit_class_13').stripped_strings:
                    content['content'] = content['content'] + string + "\n"

                # 将文章内容保存到结果
                result.append(json.dumps(content, ensure_ascii=False))
                # 休眠3s
                time.sleep(3)
            except Exception as err:
                print(err)

        return result

    """
    spider5:美食天下网站内容多个页面的解析（目前只支持一种解析）
            http://www.meishichina.com
    """
    def spiderMeshiChina(self, urlList):
        if len(urlList) < 0:
            return False

        result = []
        for i in range(0, len(urlList)):
            try:
                content = {}
                r = requests.get(urlList[i])
                soup = BeautifulSoup(r.text, "html.parser")
                # title
                content['title'] = soup.find(class_='arTitle').contents[0]
                # content
                content['content'] = ""
                for string in soup.find(class_='content').stripped_strings:
                    content['content'] = content['content'] + string + "\n"

                # 将文章内容保存到结果
                result.append(json.dumps(content, ensure_ascii=False))
                # 休眠3s
                time.sleep(3)
            except Exception as err:
                print(err)

        return result

    """
    spider6:新浪博客网站内容多个页面的解析（目前只支持一种解析）
            http://blog.sina.com.cn
    """
    def spiderBlogSina(self, urlList):
        if len(urlList) < 0:
            return False

        result = []
        for i in range(0, len(urlList)):
            try:
                content = {}
                page = urllib.urlopen(urlList[i])
                soup = BeautifulSoup(page.read(), "html5lib")
                # title
                content['title'] = soup.find(class_='titName').contents[0]
                # content
                content['content'] = ""
                for string in soup.find(class_='articalContent').stripped_strings:
                    content['content'] = content['content'] + string + "\n"

                # 将文章内容保存到结果
                result.append(json.dumps(content, ensure_ascii=False))
                # 休眠3s
                time.sleep(3)
            except Exception as err:
                print(err)

        return result

    """
    spider7:网易图文单个页面内容的抓取
    """
    def spiderNeteaseArticle(self, strUrl):
        content = urllib2.urlopen(strUrl).read()
        formatContext = content.decode('gbk').encode('utf8')
        res_div = r'<div class="post_text" id="endText">(.*?)</div>'
        m_context = re.findall(res_div, formatContext, re.S | re.M)
        article = ""
        for line in m_context:
            res_p = r'<p>(.*?)</p>'
            m_p = re.findall(res_p, line, re.S | re.M)
            for p_con in m_p:
                re_h = re.compile('</?\w+[^>]*>')
                p_con = re_h.sub('', p_con)
                article += p_con
        return article

    """
    spider8:网易图集内容的抓取
    """
    def spiderNeteasePic(self, strUrl):
        content = urllib2.urlopen(strUrl).read()
        formatContext = content.decode('gbk').encode('utf8')
        res_div = r'<textarea name="gallery-data" style="display:none;">(.*?)</textarea>'
        m_context = re.findall(res_div, formatContext, re.S | re.M)
        article = ""
        for line in m_context:
            hjson = json.loads(line)
            listInfo = hjson["list"]
            for i in range(len(listInfo) - 1):
                noteInfo = listInfo[i]["note"]
                article += noteInfo
        return article

    """
    spider9:青网图文单个页面内容的抓取
            http://www.qing5.com/
    """
    def spiderQing5Article(self, strUrl):
        content = urllib2.urlopen(strUrl).read()
        res_div = r'<p>(.*?)</p>'
        m_context = re.findall(res_div, content, re.S | re.M)
        article = ""
        for line in m_context:
            re_h = re.compile('</?\w+[^>]*>')
            p_con = re_h.sub('', line)
            article += p_con
        return article

    """
    spider10:青网图集内容的抓取
    """
    def spiderQing5Pic(self, strUrl):
        content = urllib2.urlopen(strUrl).read()
        article = ""
        res_div = r'photos.push((.*?));'
        m_context = re.findall(res_div, content, re.S | re.M)
        for line in m_context:
            article +=line[0].replace("(", "").replace(")", "").split('note:')[1].replace("\"", "")\
                                .replace("}", "").decode('unicode_escape')
        return article


# -*- coding: utf-8 -*-
# @Time    : 2017/8/26 下午3:04
# @Author  : shaopengwei@hotmail.com
# @File    : Lession1.py
# -------------------------------------------------

import urllib2
import urllib

if __name__ == "__main__":
    #抓取的url
    url = "http://python.jobbole.com/81341/"
    #请求头（header）信息，用于模拟浏览器访问
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    referer = "http://python.jobbole.com/81336/"
    headers = {'User-Agent':user_agent, 'Referer':referer}

    #如果网站限制了IP的访问次数，可以通过设置代理的方式避免，网上搜一些匿名代理的IP，然后定时替换用来请求
    proxies = ['101.68.73.54:53281']
    proxy_handler = urllib2.ProxyHandler({"http":proxies[0]})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

    #构造请求
    request = urllib2.Request(url, None, headers)
    try:
        #执行请求并获取返回结果对象，timeout时间单位是秒
        response = urllib2.urlopen(request, None, 10)
    except urllib2.HTTPError, e:
        print e.code
        print e.reason
    except urllib2.URLError, e:
        print e.reason
    else:
        print response.read()

exit(0)
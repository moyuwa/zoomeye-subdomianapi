#!/usr/bin/env python3
# coding=utf-8
# python version 3.7 by 6time
# zoomeye api查询子域名

import os, sys, requests, json

requests.packages.urllib3.disable_warnings()  # 关闭警告


class zoomeye_subdomain():
    def __init__(self):
        self.url_timeout = 10
        self.head_timeout = 4

    def http_get(self, url, apikey):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            }
            headers['API-KEY'] = apikey
            res = requests.get(url=url,
                               headers=headers,
                               # proxies=proxies,
                               timeout=self.url_timeout,
                               verify=False)
            return res
        except Exception as e:
            print(e)
        return None

    def init_apikey(self, apikey=""):
        zoomeyeapikey = os.getenv("APPDATA") + "\\zoomeyeapikey.txt"
        if os.path.exists(zoomeyeapikey):
            with open(zoomeyeapikey, "r+") as f:
                apikey = f.readline()
        elif apikey is not "":
            with open(zoomeyeapikey, "w+") as f:
                f.write(apikey)
            print("write apikey:{} to path:{}".format(apikey, zoomeyeapikey))
        return apikey.strip().rstrip()

    def www_run(self, www):
        # 初始化和保存apikey
        apikey = self.init_apikey()
        if apikey == "":
            apikey = input("no apikey,input your zoomeye apikey:")
            self.init_apikey(apikey)
        # 构造api请求
        api_url = "https://api.zoomeye.org/domain/search?q={}&type={}&page=1&s=500"  # 一般情况下目标子域名都在500以内
        # type = [0, 1]  # 0-关联域名；1-子域名
        qurl = api_url.format(www, 1)
        res = self.http_get(qurl, apikey)
        if res is None:
            print("http_get res is None")
            return
        domiansjson = json.loads(res.text)
        print("status:{},total:{},msg:{}".format(domiansjson["status"], domiansjson["total"], domiansjson["msg"]))
        # 如果子域名超过500进行提示
        if domiansjson["total"] > 500:
            print("subdomains total>500!!!!!!")
        # 输出结果到csv文件
        num = 1
        outpath = os.getcwd() + "\\{}_{}_{}.csv".format(www, 1, domiansjson["total"])
        print("{}->{}".format(www, outpath))
        with open(outpath, "w+") as f:
            for sub in domiansjson["list"]:
                f.write("{},{},{},{}\n".format(num, sub["name"], sub["ip"], sub["timestamp"]))
                num += 1

    def www_list_run(self, www_txt):
        with open(www_txt, "r+") as f:
            for www in f.readlines():
                print("search api for:{}".format(www.strip().rstrip()))
                self.www_run(www.strip().rstrip())


if __name__ == '__main__':
    print(u'zoomeye api查询子域名,支持批量 by 6time')
    print("""v1.0
    [1] python3 py3zoomeye_subdomainapi.py baidu.com
    [2] python3 py3zoomeye_subdomainapi.py -l domains.txt
    """)
    # print(os.getcwd())
    zm_subdom_api = zoomeye_subdomain()
    if len(sys.argv) == 2:
        zm_subdom_api.www_run(sys.argv[1])
    elif len(sys.argv) == 3:
        zm_subdom_api.www_list_run(sys.argv[2])

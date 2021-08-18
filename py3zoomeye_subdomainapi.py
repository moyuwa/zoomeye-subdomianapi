#!/usr/bin/env python3
# coding=utf-8
# python version 3.7 by 6time
# zoomeye api查询子域名

import os, requests, json
import argparse
import platform

requests.packages.urllib3.disable_warnings()  # 关闭警告
parser = argparse.ArgumentParser(description=u'zoomeye api查询子域名,支持批量 by 6time')


def init_apikey(apikey=""):
    sys1 = platform.system()
    if sys1 == "Windows":
        zoomeyeapikey = os.getenv("APPDATA") + "\\zoomeyeapikey.txt"
    elif sys1 == "Linux":
        zoomeyeapikey = "~/zoomeyeapikey.txt"
    else:
        print("Unsupported system")
    if os.path.exists(zoomeyeapikey):
        with open(zoomeyeapikey, "r+") as f:
            apikey = f.readline()
    elif apikey is not "":
        with open(zoomeyeapikey, "w+") as f:
            f.write(apikey)
        print("write apikey:{} to path:{}".format(apikey, zoomeyeapikey))
    return apikey.strip().rstrip()


class zoomeye_subdomain():
    def __init__(self, www, type, apikey):
        self.url_timeout = 10
        self._www = www
        self._type = type
        self._apikey = apikey

    def http_get(self, url, apikey, url_timeout):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            }
            headers['API-KEY'] = apikey
            res = requests.get(url=url,
                               headers=headers,
                               # proxies=proxies,
                               timeout=url_timeout,
                               verify=False)
            return res
        except Exception as e:
            print(e)
        return None

    def api_search_type(self, www, apikey, type=1):
        # 构造api请求
        api_url = "https://api.zoomeye.org/domain/search?q={}&type={}&page=1&s=500"  # 一般情况下目标子域名都在500以内
        qurl = api_url.format(www, type)
        res = self.http_get(qurl, apikey, self.url_timeout)
        if res is None:
            print("http_get res is None")
            return
        domainsjson = json.loads(res.text)
        print("status:{},total:{},msg:{}".format(domainsjson["status"], domainsjson["total"], domainsjson["msg"]))
        # 如果子域名超过500进行提示
        if domainsjson["total"] > 500:
            print(www + "subdomains total>500!!!!!!")
        return domainsjson

    def domainjson_out_csv(self, www, domiansjson=json):
        # 输出结果到csv文件
        num = 1
        outpath = os.getcwd() + "\\{}_{}_{}.csv".format(www, self._type,domiansjson["total"])
        print("{}->{}".format(www, outpath))
        with open(outpath, "w+") as f:
            for sub in domiansjson["list"]:
                f.write("{},{},{},{}\n".format(num, sub["name"], sub["ip"], sub["timestamp"]))
                num += 1

    # 存活探测有别的工具
    # def domain_scan(self, domainsjson):
    #     for sub in domainsjson["list"]:
    #         http = "http://" + sub["name"]
    #         res1 = self.http_get(http, "", 5)
    #         if res1 is not None:
    #             title1 = re.findall('<title>(.+)</title>', res1.text)
    #             print("{}->{}".format(title1, http))
    #         https = "https://" + sub["name"]
    #         res2 = self.http_get(https, "", 5)
    #         if res2 is not None:
    #             title2 = re.findall('<title>(.+)</title>', res2.text)
    #             print("{}->{}".format(title2, https))
    #     pass

    def www_run(self):
        print("search api for: {}".format(self._www))
        domainsjson = self.api_search_type(self._www, self._apikey, self._type)
        # if args.scan:
        #     self.domain_scan(domainsjson)
        #     pass
        # else:
        self.domainjson_out_csv(self._www, domainsjson)


if __name__ == '__main__':
    print("""
    [1] python3 py3zoomeye_subdomainapi.py -d baidu.com    #单个域名查询
    [2] python3 py3zoomeye_subdomainapi.py -l domains.txt  #批量域名查询
    [3] python3 py3zoomeye_subdomainapi.py -t 0 -d baidu.com    #查询指定类型
    """)
    # [4] python3 py3zoomeye_subdomainapi.py -s baidu.com    #http探测
    #########################################################
    parser.add_argument('-v', '--version', action='version', version='v2.0', help='v2.0')
    parser.add_argument('-d', '--domains', default="baidu.com", help='单个域名查询')
    parser.add_argument('-l', '--list', default=None, help='批量域名查询')
    parser.add_argument('-t', '--type', default=1, help='0-关联域名；1-子域名')
    # parser.add_argument('-s', '--scan', default=False, help='启用存活探测')
    args = parser.parse_args()
    # 初始化和保存apikey
    apikey = init_apikey()
    if apikey == "":
        apikey = input("no apikey,input your zoomeye apikey:")
        init_apikey(apikey)
    if args.list is None:
        zm_subdom_api = zoomeye_subdomain(args.domains.strip().rstrip(), args.type, apikey)
        zm_subdom_api.www_run()
    else:
        with open(args.list, "r+") as f:
            for www in f.readlines():
                zm_subdom_api = zoomeye_subdomain(www.strip().rstrip(), args.type, apikey)
                zm_subdom_api.www_run()

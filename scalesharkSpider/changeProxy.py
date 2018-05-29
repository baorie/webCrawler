# -*- coding:utf-8 -*-

import requests
import urllib2
from bs4 import BeautifulSoup
from multiprocessing import Pool
import copy_reg
import types

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)

class ChangeProxy(object):
    
    def __init__(self):
        self.num = 300
        self.url = "https://free-proxy-list.net/"
        self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        self.file = open("proxy.py", "w")
        self.file.write("PROXIES = [\n]")
        self.tmp_proxies = []

    def get_ip(self):
        del self.tmp_proxies [:]
        res = requests.get(self.url, headers=self.header)
        soup = BeautifulSoup(res.text, 'lxml')
        tr_list = soup.find_all('tbody')[0].find_all('tr')
        count = 0
        for each in tr_list:
            if count < self.num: # 一共300个ip
                ips = each.find_all('td')
                if ips[6].getText() == 'yes':
                    prtcl = "https"
                else:
                    prtcl = "http"
                ip_port = str(ips[0].contents[0]) + ":" + str(ips[1].contents[0])
                # self.f.write("\t\t\t{" + "'prtcl':'" + prtcl + "', 'ip_port':'" + ip_port + "'},\n")
                self.tmp_proxies.append({'prtcl': prtcl, 'ip_port': ip_port})
                count += 1
        print("ip got!")
        # self.file.write("]\n")
        # f.close()

    # 失败了在程序中删吧...
    def verify_ip(self, prtcl_ip_port):
        proxy = {prtcl_ip_port['prtcl']:prtcl_ip_port['ip_port']}

        proxy_support = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

        test_url = "https://www.google.com/"
        req = urllib2.Request(test_url, headers = self.header)
        try:
            resp = urllib2.urlopen(req, timeout = 1) #proxy delay 1s

            if resp.code == 200:
                return "\t\t\t{" + "'prtcl':'" + prtcl_ip_port['prtcl'] + "', 'ip_port':'" + prtcl_ip_port['ip_port'] + "'},\n]"

        except:
            pass

    def mycallback(self, x):
        if x != None:
            self.file.seek(-1,2)
            self.file.write(x)
            self.file.flush()

    def main(self):
        self.get_ip()
        p = Pool(4)

        for i in range(len(self.tmp_proxies)):
            handler = p.apply_async(self.verify_ip, args=(self.tmp_proxies[i],), callback=self.mycallback)
            print(handler.get())

        p.close()
        p.join()
        self.file.close()

    # def changeProxy(self, request):
    #     request.meta["proxy"] = self.ip_list[self.count-1]["prtcl"] + "://" + self.ip_list[self.count-1]["ip_port"]
    #
    # def verify(self):
    #     requests.get(url=self.temp_url, proxies={self.ip_list[self.count-1]["prtcl"]: self.ip_list[self.count-1]["ip_port"]}, timeout=5)
    #
    # def ifUsed(self, request):
    #     try:
    #         self.changeProxy(request)
    #         self.verify()
    #     except:
    #         if self.count == 0 or self.count == 10:
    #             self.getIPData()
    #             self.count = 1
    #         self.evecount = 0
    #         self.count = self.count + 1
    #         self.ifUsed(request)
    #
    # def process_request(self, request, spider):
    #     if self.count == 0 or self.count == 10:
    #         self.getIPData()
    #         self.count = 1
    #
    #     if self.evecount == 3:
    #         self.count = self.count + 1
    #         self.evecount = 0
    #     else:
    #         self.evecount = self.evecount + 1
    #
    #     self.ifUsed(request)

if __name__ == "__main__":
    changeProxy = ChangeProxy()
    changeProxy.main()

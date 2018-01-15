# coding=utf-8

import urllib2
import urllib
import re
import thread
import time
import json


class SpiderModel(object):
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False

    def get_page(self, page):
        """
        获得所有段子，添加到列表并返回
        :return:
        """
        my_url = "http://m.qiushibaike.com/hot/page/" + page
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent' : user_agent}
        req = urllib2.Request(my_url, headers=headers)
        my_response = urllib2.urlopen(req)
        my_page = my_response.read()
        unicode_page = my_page.decode('utf-8')
        my_items = re.findall('<div.*?class="content">\n+<span>(.*?)</span>\n+</div>', unicode_page, re.S)
        return my_items

    def load_page(self):
        """
        加载新段子
        :return:
        """
        while self.enable:
            if len(self.pages) < 2:
                try:
                    my_page = self.get_page(str(self.page))
                    self.page += 1
                    self.pages.append(my_page)
                except Exception as e:
                    print e
            else:
                time.sleep(1)

    def show_page(self, now_page, page):
        """
        显示段子
        :param now_page:
        :param page:
        :return:
        """
        i = 0
        for i in range(len(now_page)):
            if i < len(now_page):
                one_story = '\n'+now_page[i].replace('\n', '').replace('<br/>', '\n')+'\n'
                print u'第%d页,第%d个故事' % (page, i+1), one_story
                i += 1
            else:
                break

        my_inupt = str(raw_input(u'回车键看下一页，按quit退出:\n'))
        if my_inupt == 'quit':
            self.enable = False

    def start(self):
        """
        启动函数
        :return:
        """
        self.enable = True
        page = self.page
        print u'正在加载中请稍候......'
        thread.start_new_thread(self.load_page,())
        while self.enable:
            if self.pages:
                now_page = self.pages[0]
                del self.pages[0]
                self.show_page(now_page, page)
                page += 1


if __name__ == '__main__':
    print u'请按下回车浏览今日的糗百内容：'
    raw_input(' ')
    my_model = SpiderModel()
    my_model.start()

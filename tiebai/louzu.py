# coding=utf-8
import re
import urllib2
import sys

# 获取系统默认的编码
print sys.getdefaultencoding()
reload(sys)
# 修改系统的默认编码
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()


class HtmlTool(object):
    """
    处理页面上的各种标签
    """
    # \t \n 空格 超链接 图片
    begin_char_rex = re.compile("(\t|\n| |<a.*?>)|<img.*?>")
    # 任意标签<>
    end_char_rex = re.compile("<.*?>")
    # <p>
    begin_part_rex = re.compile("<p.*?>")
    char_to_new_line_rex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    char_to_next_tab_rex = re.compile("<td>")
    # 将html符号转变成原始符号
    replace_tab = [("<", "<"), (">", ">"), ("&", "&"), ("&", "\""), (" ", " ")]

    def replace_char(self, x):
        """
        查找替换html标签
        :return:
        """
        x = self.begin_char_rex.sub("",x)
        x = self.begin_part_rex.sub("\n ",x)
        x = self.char_to_new_line_rex.sub("\n",x)
        x = self.char_to_next_tab_rex.sub("\t",x)
        x = self.end_char_rex.sub("",x)

        for t in self.replace_tab:
            x = x.replace(t[0], t[1])
        return x


class BaiduSpider(object):
    """
    贴吧爬虫
    """
    def __init__(self, url):
        self.my_url = url + "?see_lz=1"
        self.datas = []
        self.my_tool = HtmlTool()
        print u"爬虫已启动"

    def baidu_tieba(self):
        """
        初始化加载页面并转码储存
        :return:
        """
        # 转码
        my_page = urllib2.urlopen(self.my_url).read().decode("utf-8")
        # 计算页数
        end_page = self.page_counter(my_page)
        # 获取标题
        title = self.find_title(my_page)
        print title
        # 提取数据
        self.save_data(self.my_url, title, end_page)

    def page_counter(self, my_page):
        """
        计算页数
        :param my_page:
        :return:
        """
        # 匹配 "共有<span class="red">12</span>页" 来获取一共有多少页
        # my_match = re.search(r'<a href="/p/(\d+?)?pn=(\d+?)">(\d+?)</a>', my_page, re.S)
        my_match = re.search(r'<span class="tP">(\d+?)</span>', my_page, re.S)
        if my_match:
            end_page = int(my_match.group(1))
            print u'发现楼主共有%d页的原创内容' % end_page
        else:
            end_page = 0
            print u'无法计算楼主发布内容有多少页！'
        return end_page

    def find_title(self, my_page):
        """
        寻找该帖标题
        :param my_page:
        :return:
        """
        # 匹配 <h1 class="core_title_txt" title="">xxxxxxxxxx</h1> 找出标题
        my_match = re.search(r'<h3.*?>(.*?)</h3>', my_page, re.S)
        title = u"暂无标题"
        if my_match:
            title = my_match.group(1)
        else:
            print u'爬虫报告：无法加载文章标题！'
        # 文件名不能包含以下字符： \ / ： * ? " < > |
        title = title.replace('\\', '').replace(':','').replace('*','').replace('?','').replace('"','')\
            .replace('>','').replace('<','').replace('|','')
        return title

    def save_data(self, url, title, end_page):
        """
        用来存储楼主发布的内容
        :param url:
        :param title:
        :param end_page:
        :return:
        """
        self.get_data(url, end_page)
        f = open(title+'.txt','w+')
        f.writelines(self.datas)
        f.close()
        print u'打包成txt文件'
        print u'请按任意键退出'
        raw_input()

    def get_data(self, url, end_page):
        """
        获取页面源码并肩齐存储到列表中
        :param url:
        :param end_page:
        :return:
        """
        url = url + '&pn='
        for i in range(1, end_page+1):
            print u'爬虫%d号正在加载' % i
            my_page = urllib2.urlopen(url + str(i)).read()
            # 将my_page html 存储到datas
            self.deal_data(my_page.decode('utf-8'))

    def deal_data(self, my_page):
        """
        将内容从页面代码中提取出来
        :param my_page:
        :return:
        """
        my_items = re.findall('id="post_content.*?">(.*?)</div>', my_page, re.S)
        for item in my_items:
            data = self.my_tool.replace_char(item.replace('\n', '').encode('utf-8'))
            self.datas.append(data+'\n')


if __name__ == "__main__":
    #  天影吧
    # bdurl = 'https://tieba.baidu.com/p/5360841997?see_lz=1'
    print u"请输入贴吧的地址最后的数字串："
    # baidu_url = "http://tieba.baidu.com/p/" + str(raw_input(u"http://tieba.baidu.com/p/"))
    baidu_url = "http://tieba.baidu.com/p/5360841997"
    my_spider = BaiduSpider(baidu_url)
    my_spider.baidu_tieba()

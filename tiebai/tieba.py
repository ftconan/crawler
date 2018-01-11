# coding=utf-8
import os
import urllib2


def baidu_tieba(title, url, begin_page, end_page):
    """
    定义百度贴吧函数
    :param url:
    :param begin_page:
    :param end_page:
    :return:
    """
    # 判断文件夹是否存在
    if os.path.exists(title) is not True:
        os.mkdir(title)
    new_path = os.path.abspath(title)

    for i in range(begin_page, end_page + 1):
        full_url = url + '?pn='+ str(i)
        print u'正在下载第' + str(i) + u'个网页，并将其存储为' + full_url + '......'
        html_name = title + str(i) + '.html'
        # 打开新文件中html写入数据
        file_path = os.path.join(new_path, html_name)
        f = open(file_path, 'w+')
        m = urllib2.urlopen(full_url).read()
        f.write(m)
        f.close()


# 这个是长草颜的百度贴吧中某一个帖子的地址
# https://tieba.baidu.com/p/4118229969?pn=1
# title = '长草颜'
# bdurl = 'https://tieba.baidu.com/p/4118229969'
# begin_page = 1
# end_page = 6

if __name__ == '__main__':
    title = str(raw_input('title: \n'))
    bdurl = str(raw_input('bdurl: \n'))
    begin_page = int(raw_input(' begin_page: \n'))
    end_page = int(raw_input('end_page: \n'))

    baidu_tieba(title, bdurl, begin_page, end_page)
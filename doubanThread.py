"""
    多线程抓取豆瓣剧情下的所有电影
"""
import requests
from fake_useragent import UserAgent
from queue import Queue
from threading import Thread,Lock

class DoubanThreadSpider:
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start={}&limit=20'
        # URL队列
        self.q = Queue()
        # 锁
        self.lock = Lock()

    # 1.先让URL地址入队列
    def url_in_queue(self):
        for start in range(0, 699, 20):
            page_url = self.url.format(start)
            # URL地址入队列
            self.q.put(page_url)

    # 2.线程事件函数 : 请求+解析+数据处理
    def get_html(self):
        while True:
            # 加锁
            self.lock.acquire()
            if not self.q.empty():
                url = self.q.get()
                # 释放锁
                self.lock.release()
                headers = {'User-Agent':UserAgent().random}
                html = requests.get(url=url,headers=headers).json()
                self.parse_html(html)
            else:
                # 释放锁
                self.lock.release()
                break

    # 解析提取数据函数
    def parse_html(self, html):
        for one_film_dict in html:
            item = {}
            item['rank'] = one_film_dict['rank']
            item['name'] = one_film_dict['title']
            item['score'] = one_film_dict['score']
            item['time'] = one_film_dict['release_date']

            print(item)

    def run(self):
        # 1.先让URL地址入队列
        self.url_in_queue()
        # 2.创建多线程执行爬虫程序
        t_list = []
        for i in range(2):
            t = Thread(target=self.get_html)
            t_list.append(t)
            t.start()

        for t in t_list:
            t.join()

if __name__ == '__main__':
    spider = DoubanThreadSpider()
    spider.run()

































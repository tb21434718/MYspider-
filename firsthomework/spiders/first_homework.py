import  scrapy
from firsthomework.items import FirsthomeworkItem
class FirstHomework(scrapy.Spider):
    name='firsthomework1'
    allowed_domains = ["http://cae.nuaa.edu.cn"]

    # 建立需要爬取信息的url列表
    start_urls = ['http://cae.nuaa.edu.cn/list/136']
    teacherurl_list=[]
    def parse(self, response):
        # 找到院中各个系的研究生导师所有名单链接.//table[@class="table-01"]
        collegeteachers= response.xpath('.//table[@class="table-01"]')
        links = collegeteachers.xpath('.//tr')
        for link in links:
           teacherurls=link.xpath('.//td/a[contains(@href, "showSz")]/@href').extract()#获取这个td下的所有的老师的超链接
           for teacherurl in teacherurls:
               url='http://cae.nuaa.edu.cn'+teacherurl
               self.teacherurl_list.append(url)
                # 简单的去重
        self.teacherurl_list = list(set(self.teacherurl_list))


        item = FirsthomeworkItem()
        for t1 in self.teacherurl_list:
            print(t1)
            yield scrapy.http.Request(t1, callback=self.get_text,dont_filter = True)#在 Request 请求参数中，设置 dont_filter = True ,Request 中请求的 URL 将不通过 allowed_domains 过滤。


    def get_text(self, response):
        '''进入每个老师的具体简介页面，进行item处理'''
        #先建立一个列表，用来保存
        items=[]
        item = FirsthomeworkItem()#'.//div[@class="main"]/table[@class="steacher"]/tr[1]/td/table/tr[1]/td[2]/text()'
        try:
            item['teachername'] = response.xpath( './/div[@class="main"]/table/tr[1]/td/table/tr[1]/td[@style="width:120px;"]/text()').extract()[0] #
        except Exception as error:
            print(error)
            item['teachername'] = '空'
        try:
           item['technicalpost'] = response.xpath('.//div[@class="main"]/table/tr[1]/td/table/tr[2]/td[1]/text()').extract()[0]
        except Exception as error:
            print(error)
            item['technicalpost'] =  '空'
        try:
            item['researchdirection'] = ''.join(response.xpath('.//div[@class="main"]/table/tr[1]/td/table/tr[3]/td[@colspan="5"]/text()').extract()).strip().replace('\u3000', '')
        except Exception as error:
            print(error)

            item['researchdirection'] =  '空'
        try:
          #  item['teachername'] = response.xpath( './/div[@class="main"]/table/tr[1]/td/table/tr[1]/td[@style="width:120px;"]/text()').extract()[0] #
          #  item['technicalpost'] = response.xpath('.//div[@class="main"]/table/tr[1]/td/table/tr[2]/td[1]/text()').extract()[0]
          #  item['researchdirection'] = response.xpath('.//div[@class="main"]/table/tr[1]/td/table/tr[3]/td[@colspan="5"]/text()').extract()[0]
            item['email']=response.xpath('.//div[@class="main"]/table/tr[1]/td/table/tr[4]/td[2]/text()').extract()[0]

        except Exception as error:
            print(error)
            item['email'] = '空'
        item['age'] = '空'  # response.xpath('.//div[@class="main"]/table/tr[1]/td/table/tr[4]/td[2]/text()').extract()[0]
        item[ 'college'] = '自动化'  # response.xpath('.//div[@class="main"]/table/tr[1]/td/table/tr[1]/td[1]/text()').extract()[0]
        item['degree'] = '博士'  # response.xpath('.//div[@class="main"]/table/tr[1]/td/table/tr[1]/td[1]/text()').extract()[0]
        return item
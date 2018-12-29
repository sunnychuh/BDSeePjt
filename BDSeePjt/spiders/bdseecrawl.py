# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

import urllib.request
from urllib.request import quote, unquote
from BDSeePjt.items import BdseepjtItem
from BDSeePjt.items import BdseepjtItemDetail

from bs4 import BeautifulSoup

class BdseecrawlSpider(CrawlSpider):
    name = 'bdseecrawl'
    allowed_domains = ['www.bdsee.cn']
    start_urls = ['http://www.bdsee.cn/page/1/']

    rules = (
        #Rule for movie list pages like: https://www.bdsee.cn/page/2/
        Rule(LinkExtractor(allow=('www.bdsee.cn/page/[1-9][0-9]*/'), allow_domains=('www.bdsee.cn')),
            callback='parse_item', follow=True),
        
        #Rule for movie detail pages like: https://www.bdsee.cn/%e9%a3%8e%e5%91%b3%e4%ba%ba%e9%97%b4/
        Rule(LinkExtractor(allow=('www.bdsee.cn(/.*?/)?'), 
            deny=('www.bdsee.cn/category/.*','www.bdsee.cn/yonghu/.*', 
                'www.bdsee.cn/denglu/.*', 'www.bdsee.cn/tag/.*', 
                'www.bdsee.cn/forum/.*', 'www.bdsee.cn/pf/.*'),
            allow_domains=('www.bdsee.cn')),
        callback='parse_item_detail', follow=False),

        )
        
    def parse_item(self, response):
        print(">>>>>>>>>>>>>>>>>>>>>Start to parse URL(Movie List)<<<<<<<<<<<<<<<<<<<<<<")
        print("Parse URL:"+ response.url)
        
        i = BdseepjtItem()  #{'title':[], 'link':[]}

        i["title"]=response.xpath('//a[@itemprop="mainEntityOfPage"]/text()').extract()
        i['description']=response.xpath('//div[@itemprop="description"]/p/text()').extract()
        i['link']=response.xpath('//a[@itemprop="mainEntityOfPage"]/@href').extract()
        i['comments_num']=response.xpath('//a[@itemprop="discussionURL"]/text()').extract()
        i['published_date']=response.xpath('//time[@itemprop="datePublished"]/text()').extract()
        i['category']=response.xpath('//a[@rel="category tag"]/@href').extract()
        for j in range(0, len(i["category"])):
            category = unquote(str(i["category"][j]), encoding='utf-8')
            i["category"][j]= category.split('/')[-3]
        i['category_tag']=response.xpath('//a[@rel="category tag"]/text()').extract()
        i['image_url']=response.xpath('//img[@itemprop="url"]/@src').extract()
        i['score']=response.xpath('//span[@class="edit-link icon-metas"]/a/text()').extract()
        
        return i

    def parse_item_detail(self, response):
        print(">>>>>>>>>>>>>>>>>>>>>Start to parse URL(Movie Detail)<<<<<<<<<<<<<<<<<<<<<<")
        print("Parse URL:"+ response.url)

        i = BdseepjtItemDetail()  #{'title':'', 'published_date':'', 'descriptions':[]}

        bsObj = BeautifulSoup(response.body,'html.parser')
        
        i["title"] = bsObj.find('h1',{'class':'entry-title'}).get_text()
        i["link"] = response.url
        i["published_date"] = bsObj.find('time',{'class':'updated'}).get_text()
        i["category"]=bsObj.find('nav',{'id':'breadcrumbs-nav'}).find_all('a')[1].get_text()
        i["category_tag"]=bsObj.find('nav',{'id':'breadcrumbs-nav'}).find_all('a')[2].get_text()
        i['image_url'] = bsObj.find('div',{'class':'entry-content'}).find('img')['src']

        descriptions = []
        nodes = bsObj.find('div',{'class':'entry-content'}).find_all()
        for node in nodes:
            if node.name == 'p':
                res = node.find_all(text=True)
                for str in res:
                    descriptions.append(str)
            elif node.name == 'hr':
                break
        i['descriptions'] = descriptions

        contents = []
        content_imgs = []
        hr1 = bsObj.find('div',{'class':'entry-content'}).find('hr')
        for slib in hr1.find_next_siblings():
            if slib.name == 'p':
                contents.append(slib.get_text())
                a_imgs = slib.find_all('a')
                if a_imgs is not None:
                    for a_img in a_imgs:
                        content_imgs.append(a_img['href'])
            elif slib.name == 'hr':
                break
        i['contents'] = contents
        i['content_imgs'] = content_imgs

        links = []
        lis = bsObj.find('div',{'class':'entry-content'}).find('ul').find_all('li')
        for li in lis:
            link_name = li.get_text().replace("[www.bdsee.cn]", "")
            link_details = []
            for a in li.find_all('a'):
                link_type = a.get_text()
                link_href = a['href']

                link_detail = {'link_type':link_type, 'link_href':link_href}
                link_details.append(link_detail)
            link = {'link_name': link_name, 'link_details':link_details}
            links.append(link)
        i['download_links'] = links

        return i
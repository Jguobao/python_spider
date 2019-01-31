# -*- coding: utf-8 -*-
import scrapy
import json
from copy import deepcopy


class JdComputerSpider(scrapy.Spider):
    name = 'jd_computer'
    allowed_domains = ['jd.com', "p.3.cn","list"]
    start_urls = ['https://list.jd.com/list.html?cat=670,671,672']

    def parse(self, response):
        # with open("test.html",'w',encoding="utf-8") as f:
        #     f.write(response.body.decode())
        li_list = response.xpath(".//ul[@class='gl-warp clearfix']/li")
        for li in li_list:
            item = {}
            item["title"] = li.xpath(".//div[@class='p-name']//em/text()").extract_first().strip()
            item["href"] = "https:" + li.xpath(".//div[@class='p-img']//a/@href").extract_first()
            # item["img"] = li.xpath(".//div[@class='p-img']//a/img/@src")

            # item["img"] = urljoin(item["img"], response.url)
            item["data_sku"] = li.xpath(".//div[@class='gl-i-wrap j-sku-item']/@data-sku").extract_first()
            # print(item)
            yield scrapy.Request(
                "https://p.3.cn/prices/mgets?&ext=11101000&pin=&type=1&area=13_2900_2908_0&skuIds=J_{}".format(
                    item["data_sku"]),
                callback=self.parse_notebook_price,
                meta={"item": deepcopy(item)}
            )
        next_url = response.xpath(".//div[@class='page clearfix']//a[@class = 'pn-next']/@href").extract_first()
        if next_url is not None:
            print("="*30)
            next_url = "https://list.jd.com" + next_url
            print(next_url)
            yield scrapy.Request(next_url,callback=self.parse,)

    def parse_notebook_price(self, response):
        item = response.meta["item"]
        result = json.loads(response.body.decode())
        item["价格"] = result[0]["p"]
        print(item)

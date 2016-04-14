# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser

keyword = raw_input('Keyword: ')
url = 'http://www.lkqpickyourpart.com/DesktopModules/pyp_vehicleInventory/getVehicleInventory.aspx?store=224&page=0&filter=%s&sp=&cl=&carbuyYardCode=1224&pageSize=1000&language=en-US' % (keyword,)
class Cars(scrapy.Item):
    Make = scrapy.Field()
    Model = scrapy.Field()
    Year = scrapy.Field()
    Entered_Yard = scrapy.Field()
    Section = scrapy.Field()
    Color = scrapy.Field()


class LkqSpider(scrapy.Spider):
    name = "lkq"
    allowed_domains = ["lkqpickyourpart.com"]
    start_urls = (
        url,
    )

    def parse(self, response):
        section_color = response.xpath(
            '//div[@class="pypvi_notes"]/p/text()').extract()
        info = response.xpath('//td["pypvi_make"]/text()').extract()
        for element in range(0, len(info), 4):
            item = Cars()
            item["Make"] = info[element]
            item["Model"] = info[element + 1]
            item["Year"] = info[element + 2]
            item["Entered_Yard"] = info[element + 3]
            item["Section"] = section_color.pop(
                0).replace("Section:", "").strip()
            item["Color"] = section_color.pop(0).replace("Color:", "").strip()
            yield item

        #open_in_browser(response)
        #inspect_response(response, self)

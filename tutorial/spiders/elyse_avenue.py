# -*- coding: utf-8 -*-
"""

@author: Daniel Royer
"""
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest, Request
from scrapy.item import Item, Field
#from robots_immo.items import AnnonceItem

class ElyseAvenueSpider(scrapy.Spider):

    name = "elyse_avenue"
    allowed_domains = ["elyseavenue.com"] # i fixed this
    start_urls = ["http://www.elyseavenue.com/"] # i added this

    def parse(self, response):
        yield FormRequest.from_response(response, formname='moteurRecherche', formdata={'recherche_distance_km_0':'20', 'recherche_type_logement':'9'}, callback=self.parseAnnonces)

    def parseAnnonces(self, response):
        hxs = HtmlXPathSelector(response)
        annonces = hxs.select('//div[@id="contenuCentre"]/div[@class="blocVignetteBien"]')
        items = []
        for annonce in annonces:
            item = AnnonceItem()
            item['nom'] = annonce.select('span[contains(@class,"nomBienImmo")]/a/text()').extract()
            item['superficie'] = annonce.select('table//tr[2]/td[2]/span/text()').extract()
            item['prix'] = annonce.select('span[@class="prixVignette"]/span[1]/text()').extract()
            items.append(item)
        return items
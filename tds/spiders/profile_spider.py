# -*- coding: utf-8 -*-
PATH = "./raw_data/articles/"

import os
import scrapy
import json
import pandas as pd
from datetime import datetime

class UserSpider(scrapy.Spider):
    name = 'user'

    def start_requests(self):
        # read file
        df = pd.read_json(os.path.join(PATH, filename))

        profile_urls = []

        # get `user_id`
        user_id = df['linkOfAuthorProfile'].apply(lambda x: x.split('?')[0].split('@')[-1])
        for u in user_id:
            # generate possible profile urls
            if '.' not in u and '_' not in u:
                profile_urls.append("https://" + u + ".medium.com/about")
            profile_urls.append("https://medium.com/@" + u + "/about")

        for url in profile_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for profile in response.xpath("//body"):
            yield {
                'user_name': profile.xpath(".//descendant::h2/text()[2]").get(),
                'desc': profile.xpath(".//h2//following::div[1]/p/text()").get(),
                'followers': profile.xpath(".//descendant::div[@class='n t']/descendant::div[@class='dp dq t']/a[@class='dr ds by bz ca cb cc cd ce bk dt du cf dv dw']/text()").get()
            }

# -*- coding: utf-8 -*-
import scrapy
import datetime
from datetime import date

START_MONTH = 8
START_YEAR = 2016
URL_PREFIX = 'https://towardsdatascience.com/archive/'

class ArticleSpider(scrapy.Spider):
    name = 'article'

    def start_requests(self):

        # Generate the end dates to scrape from 02/2016
        today = date.today()
        lastDay_in_lastMonth = today - datetime.timedelta(days = 1)
        end_month = lastDay_in_lastMonth.month
        end_year = lastDay_in_lastMonth.year

        # Function to generate month and year from start date to end date
        def month_year_iter(start_month, start_year, end_month, end_year):
            ym_start= 12 * start_year + start_month - 1
            ym_end= 12 * end_year + end_month - 1
            for ym in range(ym_start, ym_end):
                y, m = divmod(ym, 12)
                yield y, m+1

        generator = month_year_iter(START_MONTH, START_YEAR, end_month, end_year)

        urls = []
        for y, m in generator:
            m = str(m)
            if len(m) == 1:
                m = '0' + m  # Add '0' to months that are from Jan to Sep
            # The url looks like 'https://towardsdatascience.com/archive/yyyy/mm'
            urls.append(URL_PREFIX + str(y) + '/' + m)

        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        links_by_date = response.xpath("//div[@class='col u-inlineBlock u-width265 u-verticalAlignTop u-lineHeight35 u-paddingRight0']/descendant::div[@class='timebucket u-inlineBlock u-width35']/a/@href")
        for link in links_by_date:
            yield scrapy.Request(link.get(), callback=self.parse_story)

    def parse_story(self, response):
        stories = response.xpath("//div[@class='streamItem streamItem--postPreview js-streamItem']")
        for story in stories:
            yield {
                'author': story.xpath(".//descendant::div[@class='postMetaInline postMetaInline-authorLockup ui-captionStrong u-flex1 u-noWrapWithEllipsis']/a[@class='ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken']/text()").get(),
                'linkOfAuthorProfile': story.xpath(".//descendant::div[@class='postMetaInline postMetaInline-authorLockup ui-captionStrong u-flex1 u-noWrapWithEllipsis']/a[@class='ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken']/@href").get(),
                'articleTitle': story.xpath(".//descendant::div[@class='section-inner sectionLayout--insetColumn']/h3[1]/text()").get(),
                'articleLink': story.xpath(".//descendant::div[@class='ui-caption u-fontSize12 u-baseColor--textNormal u-textColorNormal js-postMetaInlineSupplemental']/a/@href").get(),
                'postingTime': story.xpath(".//descendant::div[@class='ui-caption u-fontSize12 u-baseColor--textNormal u-textColorNormal js-postMetaInlineSupplemental']/a/time/text()").get(),
                'minToRead': story.xpath(".//descendant::div[@class='ui-caption u-fontSize12 u-baseColor--textNormal u-textColorNormal js-postMetaInlineSupplemental']/span[2]/@title").get(),
                'recommendations': story.xpath(".//descendant::span[@class='u-relative u-background js-actionMultirecommendCount u-marginLeft5']/button/text()").get(),
                'responses': story.xpath(".//descendant::div[@class='buttonSet u-floatRight']/a/text()").get()
            }

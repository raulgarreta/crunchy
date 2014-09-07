import json

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from techcrunch.items import TechcrunchItem


class TechCrunchSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['techcrunch.com']
    start_urls = ['http://techcrunch.com/',
                  'http://techcrunch.com/startups/',
                  'http://techcrunch.com/mobile/',
                  'http://techcrunch.com/gadgets/',
                  'http://techcrunch.com/enterprise/',
                  'http://techcrunch.com/social/',
                  'http://techcrunch.com/europe/',
                  'http://techcrunch.com/asia/',
                  'http://techcrunch.com/crunchgov/'

                  ]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('/page/1$', '/page/2$', '/page/3$', '/page/4$', '/page/5$'))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('/2014/\d\d/\d\d/',)), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        item = TechcrunchItem()
        item['url'] = response.url
        item['title'] = " ".join(response.xpath('//h1//text()').extract())
        item['content'] = " ".join(
            response.xpath('//div[@class="article-entry text"]//p//text()').extract())
        item['url_image'] = " ".join(
            response.xpath('//div[@class="article-entry text"]//img/@src').extract())
        item['tags'] = json.dumps([text.strip() for text in
            response.xpath('//div[@class="accordion recirc-accordion"]//a//text()').extract()][:-1])
        return item

import scrapy
from scalesharkSpider.items import ScalesharkspiderItem
from scrapy_redis.spiders import RedisCrawlSpider

class CrunchbaseSpider(RedisCrawlSpider):
    name = 'crunchbaseSpider'
    allowed_domains = ['crunchbase.com']
    # start_urls = ('https://www.crunchbase.com/search/organization.companies', )
    redis_key = 'crunchbaseSpider:start_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(CrunchbaseSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        for each in response.xpath("//grid-row[@class='ng-star-inserted']"):
            item = ScalesharkspiderItem()
            item['organizationName'] = each.xpath(".//grid-cell[@class='column-id-identifier ng-star-inserted']//div[@class='flex cb-overflow-ellipsis identifier-label']/text()").extract()[0].strip()
            item['categories'] = ", ".join([x.strip() for x in each.xpath(".//grid-cell[@class='column-id-categories ng-star-inserted']//a[@class='cb-link ng-star-inserted']/text()").extract()])
            item['headquartersLocation'] = ", ".join([x.strip() for x in each.xpath(".//grid-cell[@class='column-id-location_identifiers ng-star-inserted']//a[@class='cb-link ng-star-inserted']/text()").extract()])
            item['description'] = each.xpath(".//grid-cell[@class='column-id-short_description ng-star-inserted']//span[@class='component--field-formatter field-type-text_long ng-star-inserted']/text()").extract()[0].strip()
            yield item

import scrapy

from scrapy.loader import ItemLoader

from ..items import LegendbankItem
from itemloaders.processors import TakeFirst


class LegendbankSpider(scrapy.Spider):
	name = 'legendbank'
	start_urls = ['https://www.legend.bank/about-us/bank-news']

	def parse(self, response):
		urls = response.xpath('(//article[@class="span8"]//a/@href)').getall()
		dates = response.xpath('(//article[@class="span8"]//strong/text())').getall()
		dates = [date for date in dates if len(date) > 1]
		for counter in range(len(dates)):
			url = urls[counter]
			date = dates[counter]
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		if 'files' in response.url:
			return
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@data-content-block="bodyCopy"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=LegendbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

import scrapy


class TikiSpider(scrapy.Spider):
    name = 'tiki'
    crawled_page_number = 2
    crawl_page_number = 10
    start_urls = ['https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner']
    #start_urls = ['https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&fst=as%3Aoff&qid=1596769816&rnid=1250225011&ref=lp_283155_nr_p_n_publication_date_0']
    def parse(self, response):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_link)
        #price = response.css('span.a-price-whole::text').get()
        #name_a = response.xpath('//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[1]/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a/span/text()').get()
    def parse_link(self,response):
        links = response.css('div.product-item a')
        for link in links:
            yield {
                'name': link.css('::attr(title)').get(),
                'price' : link.css('span.final-price::text').get().strip(),
                'discount': link.css('span.sale-tag::text').get(default='Khong giam'),
                'link_product': link.css('::attr(href)').get()
            }
        next_page = 'https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner&page='+ str(TikiSpider.crawled_page_number)
        if TikiSpider.crawled_page_number < TikiSpider.crawl_page_number:
            TikiSpider.crawled_page_number+=1
            yield response.follow(next_page, callback= self.parse_link)




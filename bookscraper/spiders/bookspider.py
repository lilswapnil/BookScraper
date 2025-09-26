import scrapy

class BookspiderSpider(scrapy.Spider):
    # Spider's unique name, used to run it.
    name = 'bookspider'
    # Restricts crawling to this domain.
    allowed_domains = ['books.toscrape.com']
    # The URL where the spider will begin crawling.
    start_urls = ['http://books.toscrape.com/']

    # This method is called to handle the response downloaded for each of the start_urls.
    def parse(self, response):
        # Select all book containers on the page.
        books = response.css('article.product_pod')

        # Iterate through each book and extract the required data.
        for book in books:
            # Yield a dictionary with the extracted data. Scrapy will collect these.
            yield{
                'title': book.css('h3 a::text').get(),
                'price': book.css('p.price_color::text').get(),
                'url': book.css('h3 a').attrib['href'],
            }

        # Find the relative URL for the next page.
        next_page = response.css('li.next a::attr(href)').get()

        # If a "next page" link exists, follow it and call this same parse method.
        if next_page is not None:
            # The site has inconsistent relative URLs, this logic handles both cases.
            if 'catalogue/' in next_page:
                next_page_url = 'http://books.toscrape.com/' + next_page
            else:
                next_page_url = 'http://books.toscrape.com/catalogue/' + next_page
            # Schedule the next page to be downloaded and parsed.
            yield response.follow(next_page_url, callback=self.parse)
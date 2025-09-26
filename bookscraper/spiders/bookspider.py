import scrapy

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    # This method is Scrapy's main callback for processing downloaded pages.
    def parse(self, response):
        # Find all book containers on the current page.
        books = response.css('article.product_pod')

        # Extract data from each book and yield it as a dictionary.
        for book in books:
            yield{
                'title': book.css('h3 a::text').get(),
                'price': book.css('p.price_color::text').get(),
                'url': book.css('h3 a').attrib['href'],
            }

        # Find the link to the next page.
        next_page = response.css('li.next a::attr(href)').get()

        # If a next page exists, create a new request to follow it,
        # and set this same method as the callback to process that page.
        if next_page is not None:
            # The site has inconsistent relative URLs, this logic handles both cases.
            if 'catalogue/' in next_page:
                next_page_url = 'http://books.toscrape.com/' + next_page
            else:
                next_page_url = 'http://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)
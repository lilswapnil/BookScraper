# 🕷️📚 BookScraper

A web scraping project built with Scrapy.

## Installation

1.  **Clone the repository**
    ```sh
    git clone <your-repository-url>
    cd bookscraper
    ```

2.  **Create and activate a virtual environment (recommended)**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies**
    This project requires Scrapy.
    ```sh
    pip install Scrapy
    ```

## Example: Scraping `books.toscrape.com`

This guide walks through the process of creating a spider that extracts detailed book information by first crawling the catalogue and then following the link for each book.

### 1. Create the Spider

First, from the project's root directory, generate a new spider.

```sh
scrapy genspider bookspider books.toscrape.com
```

This creates `bookscraper/spiders/bookspider.py`.

### 2. Find CSS Selectors with Scrapy Shell

Use the Scrapy shell to find the correct selectors. First, find the links on the main page, then enter a book's detail page to find the selectors for the data you want.

```sh
# Start the shell on the main page
scrapy shell 'http://books.toscrape.com/'

# Find the link to the next page
>>> response.css('li.next a::attr(href)').get()
'catalogue/page-2.html'

# Find the link to the first book
>>> response.css('article.product_pod h3 a::attr(href)').get()
'catalogue/a-light-in-the-attic_1000/index.html'

# Now, let's inspect a book's detail page
>>> fetch('http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')

# Get the book title from the detail page
>>> response.css('.product_main h1::text').get()
'A Light in the Attic'

# Get the book category
>>> response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
'Poetry'

# Get the product description
>>> response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
'...some of the most brilliant and funny poems...'
```

### 3. Write the Spider Logic

Update `bookscraper/spiders/bookspider.py` with a two-step process. The `parse` method will handle catalogue pages and pagination, while the `parse_book_page` method will extract data from each book's detail page.

```python
# filepath: bookscraper/spiders/bookspider.py
import scrapy

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # Find all book containers on the current page.
        books = response.css('article.product_pod')

        # For each book, follow the link to its detail page.
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            # Use response.follow to handle relative URLs and schedule the request.
            # The callback specifies which method will parse the book's page.
            yield response.follow(relative_url, callback=self.parse_book_page)

        # Find the link to the next page of listings.
        next_page = response.css('li.next a::attr(href)').get()

        # If a next page exists, follow it and use this same parse method as the callback.
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    # This method parses the individual book pages.
    def parse_book_page(self, response):
        table_rows = response.css('table tr')
        # Yield a dictionary containing all the extracted book details.
        yield {
            'url': response.url,
            'title': response.css('.product_main h1::text').get(),
            'product_type': table_rows[1].css('td::text').get(),
            'price_excl_tax': table_rows[2].css('td::text').get(),
            'price_incl_tax': table_rows[3].css('td::text').get(),
            'tax': table_rows[4].css('td::text').get(),
            'availability': table_rows[5].css('td::text').get(),
            'number_of_reviews': table_rows[6].css('td::text').get(),
            'stars': response.css('p.star-rating').attrib['class'],
            'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price': response.css('p.price_color::text').get()
        }
```

### 4. Run the Spider and Save Data

Execute the spider using the `crawl` command. Use the `-o` flag to save the detailed output to a file (e.g., `bookdata.csv`).

```sh
scrapy crawl bookspider -o bookdata.csv
```

This will run the spider, collecting detailed information from every book across all pages and saving the results into a `bookdata.csv` file.

## Troubleshooting

If you encounter an `AttributeError: module 'OpenSSL.SSL' has no attribute 'SSLv3_METHOD'`, it likely indicates a dependency conflict. This can happen if you have multiple Python environments (like Conda and a standard venv) active or if you have corrupted cached packages.

To resolve this, perform a clean installation:

1.  **Deactivate all environments.** Run these commands until no environment name (like `(base)` or `(venv)`) appears in your terminal prompt.
    ```sh
    conda deactivate
    deactivate
    ```

2.  **Activate the project's virtual environment.**
    ```sh
    source venv/bin/activate
    ```

3.  **Force a clean re-installation of Scrapy.** This command clears the cache and installs the latest compatible versions of Scrapy and its dependencies.
    ```sh
    pip install --no-cache-dir --upgrade Scrapy
    ```

After completing these steps, your Scrapy commands should execute correctly.

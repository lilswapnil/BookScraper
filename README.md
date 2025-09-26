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

This guide walks through the process of creating a spider that extracts book information from all pages of [books.toscrape.com](http://books.toscrape.com/).

### 1. Create the Spider

First, from the project's root directory, generate a new spider.

```sh
scrapy genspider bookspider books.toscrape.com
```

This creates `bookscraper/spiders/bookspider.py`.

### 2. Find CSS Selectors with Scrapy Shell

Use the Scrapy shell to inspect the website and find the correct selectors for the data you want.

```sh
scrapy shell 'http://books.toscrape.com/'
```

Inside the shell, run these commands to test selectors:

```python
# Select all book containers
>>> books = response.css('article.product_pod')

# Get the title of the first book
>>> books[0].css('h3 a::text').get()
'A Light in the ...'

# Get the price of the first book
>>> books[0].css('p.price_color::text').get()
'£51.77'

# Get the relative URL of the first book
>>> books[0].css('h3 a').attrib['href']
'catalogue/a-light-in-the-attic_1000/index.html'

# Find the link to the next page
>>> response.css('li.next a').attrib['href']
'catalogue/page-2.html'
```

### 3. Write the Spider Logic

Now, update `bookscraper/spiders/bookspider.py` with the logic to extract data and follow pagination links.

```python
# filepath: bookscraper/spiders/bookspider.py
import scrapy

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # Select each book's container
        books = response.css('article.product_pod')

        # Loop through each book and extract data
        for book in books:
            yield {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('p.price_color::text').get(),
                'url': response.urljoin(book.css('h3 a').attrib['href']),
            }

        # Find the "next" page link and follow it
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)
```

### 4. Run the Spider and Save Data

Execute the spider using the `crawl` command. Use the `-o` flag to save the output to a file (e.g., `books.json`).

```sh
scrapy crawl bookspider -o books.json
```

This will run the spider, starting from the `start_urls`, extract the data from each book, follow the "next" page link until there are no more pages, and save all the results into a `books.json` file.

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

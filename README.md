# BookScraper

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

## Usage

1.  **Create a spider**
    To create a new spider, run the `genspider` command from the project's root directory:
    ```sh
    scrapy genspider <spider_name> <domain_to_scrape>
    ```
    Example:
    ```sh
    scrapy genspider bookspider books.toscrape.com
    ```
    This will generate a new spider file in `bookscraper/spiders/`.

2.  **Run the spider**
    Execute the `crawl` command followed by your spider's name:
    ```sh
    scrapy crawl <spider_name>
    ```
    Example:
    ```sh
    scrapy crawl bookspider
    ```

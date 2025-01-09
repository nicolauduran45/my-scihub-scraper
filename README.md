# SciHub Scraper 👩‍🔬🎣

A simple Python script that uses Selenium to scrape papers from SciHub based on DOI or PMID.

## Installation

To use this script, you need Python 3.6 or higher and the following dependencies:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/scihub-scraper.git
    cd scihub-scraper
    ```

2. **Install dependencies:**

    You can use `pip` to install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. **Download ChromeDriver:**

    Selenium requires a web driver (ChromeDriver) to interact with the browser. Download the appropriate version of ChromeDriver for your version of Google Chrome from:  
    [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/).

    Make sure to place `chromedriver` in the same directory as your script or update the script to point to the correct path.

## Usage

To use the scraper, run:

```bash
python scraper/scraper.py --doi "10.1038/s41586-019-0913-7"
